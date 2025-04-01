# Sistema de Gestão de Biblioteca Digital

## Grupo: Cauã Assunção, Catarina, Brenda, Cassio, Gustavo

## Disciplina: Novas Tecnologias (Python)

### Tema do Projeto: Sistema de Gestão de Biblioteca Digital

### Objetivo:
Desenvolver um sistema de gestão de biblioteca digital simples, que permita o cadastro de livros, usuários, empréstimos e gere relatórios de estatísticas. A aplicação foi desenvolvida utilizando Python e suas boas práticas de programação, incluindo estruturas de dados e manipulação de arquivos.

---

## Funcionalidades do Sistema:

### 1. Cadastro de Livros
O sistema permite o cadastro de livros com as seguintes informações:
- Título
- Autor
- Ano de publicação
- ISBN
- Categoria

Os livros são armazenados em uma lista de dicionários, onde cada livro é um dicionário com essas informações. O sistema também permite a listagem e a busca de livros por título, autor ou categoria.

### 2. Cadastro de Usuários
Cada usuário tem um ID único, nome, e-mail e tipo (aluno, professor, visitante). A adição de usuários é feita em um dicionário, onde a chave é o ID do usuário e o valor é outro dicionário com as informações do usuário. O sistema evita e-mails duplicados e IDs repetidos.

### 3. Sistema de Empréstimos
O sistema permite o empréstimo de livros para usuários, associando um livro a um usuário e registrando a data do empréstimo. O sistema verifica se o livro já foi emprestado antes de realizar um novo empréstimo. Também é possível devolver livros e registrar o histórico de devoluções.

### 4. Estatísticas e Relatórios
O sistema gera as seguintes estatísticas:
- Quantidade de livros por categoria.
- Quantidade de empréstimos por tipo de usuário.
- Lista dos livros mais emprestados.

Essas informações são exibidas como relatórios JSON que podem ser utilizados para análise do uso da biblioteca.

### 5. Persistência de Dados
Os dados de livros, usuários, empréstimos e histórico de empréstimos são salvos em arquivos CSV. Ao reiniciar o sistema, os dados são carregados automaticamente desses arquivos, garantindo a persistência das informações.

### 6. Interface Web com Flask
Foi implementado uma interface web utilizando **Flask**, com páginas em **HTML**, **CSS** e **JavaScript**. A interface permite que o usuário interaja de forma intuitiva e visual com o sistema, realizando as operações de cadastro, empréstimo, devolução e consulta de estatísticas.

---

## Como Funciona

### Arquivo Principal: `app.py`

O código é estruturado em um servidor **Flask** que disponibiliza rotas para as diferentes funcionalidades. As principais funcionalidades são:
- **Cadastro de livros** (`/cadastrar_livro`)
- **Cadastro de usuários** (`/cadastrar_usuario`)
- **Empréstimos de livros** (`/emprestar_livro`)
- **Devolução de livros** (`/devolver_livro`)
- **Estatísticas** (`/estatisticas` e `/estatisticas/dados`)

Os dados são carregados ao iniciar o sistema, e ao fazer modificações, as informações são salvas automaticamente nos arquivos CSV.

---

## Exemplo de Uso

### Menu Textual:
Ao rodar o sistema em modo textual, o usuário será apresentado ao menu com opções.

**Exemplo de execução do menu:**

```
=== Biblioteca ===

1. Listar livros
2. Listar usuários
3. Listar empréstimos
4. Cadastrar livro
5. Cadastrar usuário
6. Emprestar livro
7. Devolver livro
8. Estatísticas
9. Sair
Escolha uma opção:
```

Quando o usuário escolhe uma opção, o sistema pede os dados necessários, como título e autor para cadastrar um livro, ou nome e tipo para cadastrar um usuário.

### Exemplo de Execução no Flask:

A interface do Flask permite que o usuário realize operações como cadastro de livros e usuários, empréstimos, devoluções e visualização das estatísticas de forma mais amigável, através de páginas **HTML**.

**Exemplo de Cadastro de Livro:**
- Quando acessado a URL `/cadastrar_livro`, o usuário preenche um formulário com as informações do livro. Caso o livro já exista (verificando o ISBN), o sistema retornará um erro.
  
**Exemplo de Cadastro de Usuário:**
- A URL `/cadastrar_usuario` permite que o administrador cadastre novos usuários, garantindo que o e-mail e o ID sejam únicos.

**Exemplo de Empréstimo:**
- O empréstimo de um livro ocorre quando o usuário fornece o ISBN do livro e o ID do usuário. O sistema valida se o livro já está emprestado e, caso não esteja, registra o empréstimo.

---

## Exemplo de Dados Salvos (Arquivos CSV)

Os dados são persistidos em arquivos CSV. O sistema salva as informações em quatro arquivos principais:
- **livros.csv**: Contém todos os livros cadastrados.
- **usuarios.csv**: Contém todos os usuários cadastrados.
- **emprestimos.csv**: Contém todos os empréstimos ativos.
- **historico_emprestimos.csv**: Contém o histórico de empréstimos e devoluções.

---

## Tecnologias Utilizadas
- **Python 3**: Linguagem utilizada para o desenvolvimento.
- **Flask**: Framework para a criação da interface web.
- **HTML, CSS e JavaScript**: Para o design e funcionalidades da interface web.
- **CSV**: Arquivos para persistência de dados.

---

## Membros do Grupo

- **Cauã Assunção**: Responsável pela estruturação do código e implementação das rotas principais do Flask.
- **Catarina**: Responsável pela implementação do sistema de persistência de dados e manipulação de arquivos CSV.
- **Brenda**: Responsável pelo design e implementação da interface de menu textual.
- **Cassio**: Responsável pela implementação das funções de empréstimos e devoluções de livros.
- **Gustavo**: Responsável pela implementação das estatísticas e relatórios de uso da biblioteca.

---

## Desafios Enfrentados
- **Manipulação de arquivos CSV**: Inicialmente, tivemos dificuldades para garantir que os dados fossem carregados e salvos corretamente, especialmente com a leitura e escrita simultânea nos arquivos CSV.
- **Gerenciamento de empréstimos**: Garantir que um livro não fosse emprestado mais de uma vez ao mesmo tempo foi uma parte importante para garantir a integridade dos dados.
- **Integração entre funcionalidades**: Integrar a interface Flask com o menu textual de maneira eficiente foi um desafio de design para manter a flexibilidade de ambos os modos de operação.

---

## Conclusão

Este sistema de gestão de biblioteca digital foi desenvolvido para gerenciar livros, usuários e empréstimos de maneira simples e eficiente. A utilização de **Flask** possibilitou a criação de uma interface **web** para o sistema, enquanto as funcionalidades de menu textual facilitaram a interação com usuários que preferem utilizar o sistema em modo console.

---

## Como Rodar o Sistema

1. Clone o repositório:
   ```
   git clone https://github.com/https://github.com/kantxlx/Sistema_Gestao_Biblioteca_Digital.git
   ```

2. Instale as dependências necessárias:
   ```
   pip install -r requirements.txt
   ```

3. Execute o sistema:
   ```
   python app.py
   ```


O sistema estará disponível na URL `http://127.0.0.1:5000` para ser acessado através do navegador.

---
