import sqlite3

class ConexaoBD:
    """Classe responsável por gerenciar o banco de dados e as 3 tabelas relacionais."""
    def __init__(self, nome_banco="biblioteca.db"):
        self.conexao = sqlite3.connect(nome_banco)
        self.cursor = self.conexao.cursor()
        # Ativa o suporte a chaves estrangeiras no SQLite
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS Categoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS Autor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS Livro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor_id INTEGER NOT NULL,
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY (autor_id) REFERENCES Autor (id),
                FOREIGN KEY (categoria_id) REFERENCES Categoria (id)
            );
        ''')
        self.conexao.commit()

    def fechar(self):
        self.conexao.close()

class RepositorioBase:
    """Classe genérica que fornece operações CRUD para qualquer tabela."""
    def __init__(self, bd, tabela, colunas):
        self.bd = bd
        self.tabela = tabela
        self.colunas = colunas

    def criar(self, valores):
        try:
            placeholders = ", ".join(["?"] * len(valores))
            colunas_str = ", ".join(self.colunas)
            sql = f"INSERT INTO {self.tabela} ({colunas_str}) VALUES ({placeholders})"
            self.bd.cursor.execute(sql, valores)
            self.bd.conexao.commit()
            print("\n[Sucesso] Registro criado!")
        except Exception as e:
            print(f"\n[Erro] Não foi possível criar o registro: {e}")

    def ler(self):
        try:
            self.bd.cursor.execute(f"SELECT * FROM {self.tabela}")
            registros = self.bd.cursor.fetchall()
            print(f"\n--- Registros de {self.tabela} ---")
            if not registros:
                print("Nenhum registro encontrado.")
            for reg in registros:
                print(reg)
        except Exception as e:
            print(f"\n[Erro] Não foi possível ler os registros: {e}")

    def atualizar(self, id_registro, valores):
        try:
            set_str = ", ".join([f"{col} = ?" for col in self.colunas])
            sql = f"UPDATE {self.tabela} SET {set_str} WHERE id = ?"
            self.bd.cursor.execute(sql, (*valores, id_registro))
            self.bd.conexao.commit()
            print("\n[Sucesso] Registro atualizado!")
        except Exception as e:
            print(f"\n[Erro] Não foi possível atualizar o registro: {e}")

    def deletar(self, id_registro):
        try:
            sql = f"DELETE FROM {self.tabela} WHERE id = ?"
            self.bd.cursor.execute(sql, (id_registro,))
            self.bd.conexao.commit()
            print("\n[Sucesso] Registro deletado!")
        except Exception as e:
            print(f"\n[Erro] Não foi possível deletar o registro: {e}")

class InterfaceTerminal:
    """Classe que controla o menu interativo e as entradas do usuário."""
    def __init__(self):
        self.bd = ConexaoBD()
        # Mapeia as tabelas para seus respectivos repositórios
        self.repositorios = {
            '1': ('Autor', RepositorioBase(self.bd, 'Autor', ['nome'])),
            '2': ('Categoria', RepositorioBase(self.bd, 'Categoria', ['nome'])),
            '3': ('Livro', RepositorioBase(self.bd, 'Livro', ['titulo', 'autor_id', 'categoria_id']))
        }

    def exibir_menu_principal(self):
        print("\n=== SISTEMA DE BIBLIOTECA ===")
        print("1. Gerenciar Autores")
        print("2. Gerenciar Categorias")
        print("3. Gerenciar Livros")
        print("0. Sair do Sistema")

    def exibir_menu_crud(self, nome_tabela):
        print(f"\n--- Menu: {nome_tabela} ---")
        print("1. Adicionar (Create)")
        print("2. Listar (Read)")
        print("3. Editar (Update)")
        print("4. Excluir (Delete)")
        print("0. Voltar")

    def obter_inteiro(self, mensagem):
        """Previne que o programa quebre se o usuário digitar letras onde deve ser número."""
        while True:
            try:
                return int(input(mensagem))
            except ValueError:
                print("[Aviso] Entrada inválida. Por favor, digite um número inteiro.")

    def menu_crud(self, nome_tabela, repo):
        while True:
            self.exibir_menu_crud(nome_tabela)
            opcao = input("Escolha uma ação: ")

            if opcao == '1':
                valores = []
                for col in repo.colunas:
                    valor = input(f"Digite o valor para '{col}': ")
                    # Converte para inteiro se for id de Autor ou Categoria
                    if col in ['autor_id', 'categoria_id']:
                        try:
                            valor = int(valor)
                        except ValueError:
                            print(f"[Erro] {col} deve ser um número inteiro!")
                            continue
                    valores.append(valor)
                if len(valores) == len(repo.colunas):  # Verifica se todos foram inseridos com sucesso
                    repo.criar(valores)
            
            elif opcao == '2':
                repo.ler()
            
            elif opcao == '3':
                id_reg = self.obter_inteiro(f"Digite o ID do '{nome_tabela}' a ser editado: ")
                valores = []
                for col in repo.colunas:
                    valor = input(f"Digite o novo valor para '{col}': ")
                    # Converte para inteiro se for id de Autor ou Categoria
                    if col in ['autor_id', 'categoria_id']:
                        try:
                            valor = int(valor)
                        except ValueError:
                            print(f"[Erro] {col} deve ser um número inteiro!")
                            continue
                    valores.append(valor)
                if len(valores) == len(repo.colunas):  # Verifica se todos foram inseridos com sucesso
                    repo.atualizar(id_reg, valores)
            
            elif opcao == '4':
                id_reg = self.obter_inteiro(f"Digite o ID do '{nome_tabela}' a ser excluído: ")
                repo.deletar(id_reg)
            
            elif opcao == '0':
                break
            else:
                print("[Aviso] Opção inválida.")

    def iniciar(self):
        """Loop principal do sistema"""
        while True:
            self.exibir_menu_principal()
            opcao = input("Escolha uma tabela para gerenciar: ")

            if opcao in self.repositorios:
                nome_tabela, repo = self.repositorios[opcao]
                self.menu_crud(nome_tabela, repo)
            elif opcao == '0':
                print("\nEncerrando o sistema com segurança...")
                self.bd.fechar()
                break
            else:
                print("[Aviso] Opção inválida. Tente novamente.")