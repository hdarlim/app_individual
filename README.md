# Sistema de Biblioteca

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=flat-square&logo=sqlite)

Um gerenciador de biblioteca em Python com banco de dados SQLite, permitindo gerenciar autores, categorias e livros através de uma interface de terminal interativa.

## Funcionalidades

- **Gerenciar Autores**: Adicionar, listar, editar e deletar autores
- **Gerenciar Categorias**: Adicionar, listar, editar e deletar categorias
- **Gerenciar Livros**: Adicionar, listar, editar e deletar livros com relacionamento a autores e categorias
- **Banco de Dados Relacional**: SQLite com suporte a chaves estrangeiras

## Como usar

1. **Execute o programa:**
   ```bash
   python app.py
   ```

2. **Menu Principal:**
   - Opção 1: Gerenciar Autores
   - Opção 2: Gerenciar Categorias
   - Opção 3: Gerenciar Livros
   - Opção 0: Sair

3. **Menu CRUD** (para cada tabela):
   - Opção 1: Adicionar novo registro
   - Opção 2: Listar todos os registros
   - Opção 3: Editar um registro (informe o ID)
   - Opção 4: Deletar um registro (informe o ID)
   - Opção 0: Voltar ao menu principal

## Estrutura

- `app.py` - Ponto de entrada da aplicação
- `classes.py` - Definição das classes (ConexaoBD, RepositorioBase, InterfaceTerminal)
- `biblioteca.db` - Banco de dados SQLite (criado automaticamente)

## Requisitos

- Python 3.x
- SQLite3 (incluído no Python)