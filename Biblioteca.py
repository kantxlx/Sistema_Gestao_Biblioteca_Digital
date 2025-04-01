import os
import csv
from threading import Thread
from datetime import datetime
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Estruturas de dados
livros = []  # Lista de dicionários para armazenar livros
usuarios = {}  # Dicionário de usuários (ID único)
emprestimos = []  # Lista para armazenar empréstimos
emprestimos_contagem = defaultdict(int)  # Contagem de empréstimos por livro

# Tipos de usuários
TIPOS_USUARIOS = ("aluno", "professor", "visitante")

# Caminhos para os arquivos CSV
DIRETORIO_DADOS = "dados"
CAMINHO_LIVROS = os.path.join(DIRETORIO_DADOS, "livros.csv")
CAMINHO_USUARIOS = os.path.join(DIRETORIO_DADOS, "usuarios.csv")
CAMINHO_EMPRESTIMOS = os.path.join(DIRETORIO_DADOS, "emprestimos.csv")
CAMINHO_HISTORICO = os.path.join(DIRETORIO_DADOS, "historico_emprestimos.csv")

# Criar diretório se não existir
if not os.path.exists(DIRETORIO_DADOS):
    os.makedirs(DIRETORIO_DADOS)


def salvar_dados():
    """Salva os dados de livros, usuários e empréstimos, mantendo o histórico."""
    try:
        with open(CAMINHO_LIVROS, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["Título", "Autor", "Ano", "ISBN", "Categoria"])
            for livro in livros:
                escritor.writerow([livro["titulo"], livro["autor"], livro["ano"], livro["isbn"], livro["categoria"]])

        with open(CAMINHO_USUARIOS, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["ID", "Nome", "Email", "Tipo"])
            for usuario in usuarios.values():
                escritor.writerow([usuario["id"], usuario["nome"], usuario["email"], usuario["tipo"]])

        with open(CAMINHO_EMPRESTIMOS, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["Livro", "Usuário", "Data"])
            for emp in emprestimos:
                escritor.writerow([emp["livro"], emp["usuario"], emp["data"]])

        with open(CAMINHO_HISTORICO, "a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            if os.stat(CAMINHO_HISTORICO).st_size == 0:
                escritor.writerow(["Livro", "Usuário", "Data", "Status"])
            for emp in emprestimos:
                escritor.writerow([emp["livro"], emp["usuario"], emp["data"], "emprestado"])
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")

def carregar_dados():
    """Carrega os dados dos arquivos CSV."""
    global livros, usuarios, emprestimos, emprestimos_contagem

    try:
        if os.path.exists(CAMINHO_LIVROS):
            with open(CAMINHO_LIVROS, "r", encoding="utf-8") as f:
                leitor = csv.reader(f)
                next(leitor, None)
                livros = [{"titulo": linha[0], "autor": linha[1], "ano": linha[2], "isbn": linha[3], "categoria": linha[4]} for linha in leitor]

        if os.path.exists(CAMINHO_USUARIOS):
            with open(CAMINHO_USUARIOS, "r", encoding="utf-8") as f:
                leitor = csv.reader(f)
                next(leitor, None)
                for linha in leitor:
                    usuarios[linha[0]] = {"id": linha[0], "nome": linha[1], "email": linha[2], "tipo": linha[3]}

        if os.path.exists(CAMINHO_EMPRESTIMOS):
            with open(CAMINHO_EMPRESTIMOS, "r", encoding="utf-8") as f:
                leitor = csv.reader(f)
                next(leitor, None)
                for linha in leitor:
                    emprestimos.append({"livro": linha[0], "usuario": linha[1], "data": linha[2]})
                    emprestimos_contagem[linha[0]] += 1  # Atualizando a contagem de empréstimos

    except Exception as e:
        print(f"Erro ao carregar dados: {e}")


        

@app.route("/", methods=["GET", "POST"])
def index():
    # Pegando os parâmetros de busca
    busca = request.args.get("busca", "")  # Recebe a busca, padrão é uma string vazia

    # Filtrando os livros com base no parâmetro de busca
    livros_filtrados = [livro for livro in livros if
                        busca.lower() in livro["titulo"].lower() or
                        busca.lower() in livro["autor"].lower() or
                        busca.lower() in livro["categoria"].lower()]
    
    return render_template("index.html", livros=livros_filtrados, emprestimos=[emp['livro'] for emp in emprestimos])


@app.route("/livros", methods=["GET", "POST"])
def listar_livros():
    # Pegando os parâmetros de busca
    busca = request.args.get("busca", "")  # Recebe a busca, padrão é uma string vazia

    # Filtrando os livros com base no parâmetro de busca
    livros_filtrados = [livro for livro in livros if
                        busca.lower() in livro["titulo"].lower() or
                        busca.lower() in livro["autor"].lower() or
                        busca.lower() in livro["categoria"].lower()]

    return render_template("livros.html", livros=livros_filtrados)

@app.route("/usuarios")
def listar_usuarios():
    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/emprestimos")
def listar_emprestimos():
    return render_template("emprestimos.html", emprestimos=emprestimos)


@app.route("/cadastrar_livro", methods=["GET", "POST"])
def cadastrar_livro():
    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        ano = request.form["ano"]
        isbn = request.form["isbn"]
        categoria = request.form["categoria"]

        # Verifica se ISBN já existe
        if any(livro["isbn"] == isbn for livro in livros):
            return "Livro com esse ISBN já cadastrado.", 400

        livros.append({"titulo": titulo, "autor": autor, "ano": ano, "isbn": isbn, "categoria": categoria})
        salvar_dados()
        return redirect(url_for("listar_livros"))

    return render_template("cadastrar_livro.html")


@app.route("/cadastrar_usuario", methods=["GET", "POST"])
def cadastrar_usuario():
    if request.method == "POST":
        id_usuario = request.form["id"]
        nome = request.form["nome"]
        email = request.form["email"]
        tipo = request.form["tipo"]

        if tipo not in TIPOS_USUARIOS:
            return "Tipo de usuário inválido.", 400

        if email in {u["email"] for u in usuarios.values()}:
            return "Email já cadastrado.", 400

        if id_usuario in usuarios:
            return "ID de usuário já cadastrado.", 400

        usuarios[id_usuario] = {"id": id_usuario, "nome": nome, "email": email, "tipo": tipo}
        salvar_dados()
        return redirect(url_for("listar_usuarios"))

    return render_template("cadastrar_usuario.html")


@app.route("/emprestar_livro", methods=["GET", "POST"])
def emprestar_livro():
    if request.method == "POST":
        isbn = request.form["isbn"]
        id_usuario = request.form["id_usuario"]

        # Verifica se o livro existe
        livro = next((livro for livro in livros if livro["isbn"] == isbn), None)
        if not livro:
            return "Livro não encontrado.", 400

        # Verifica se o usuário existe
        usuario = usuarios.get(id_usuario)
        if not usuario:
            return "Usuário não encontrado.", 400

        # Verifica se o livro já está emprestado
        if any(emp["livro"] == isbn for emp in emprestimos):
            return "Livro já emprestado.", 400

        # Registra o empréstimo
        emprestimos.append({"livro": isbn, "usuario": id_usuario, "data": datetime.now().strftime("%d/%m/%Y")})
        emprestimos_contagem[isbn] += 1
        salvar_dados()
        return redirect(url_for("listar_emprestimos"))

    return render_template("emprestar_livro.html")

@app.route("/devolver_livro", methods=["GET", "POST"])
def devolver_livro():
    if request.method == "POST":
        isbn = request.form["isbn"]
        id_usuario = request.form["id_usuario"]

        livro = next((livro for livro in livros if livro["isbn"] == isbn), None)
        if not livro:
            return jsonify({"error": "Livro não encontrado."}), 400

        usuario = usuarios.get(id_usuario)
        if not usuario:
            return jsonify({"error": "Usuário não encontrado."}), 400

        emprestimo = next((emp for emp in emprestimos if emp["livro"] == isbn and emp["usuario"] == id_usuario), None)
        if not emprestimo:
            return jsonify({"error": "Este livro não foi emprestado para este usuário."}), 400

        emprestimos.remove(emprestimo)

        with open(CAMINHO_HISTORICO, "a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow([isbn, id_usuario, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "devolvido"])

        salvar_dados()
        return jsonify({"message": "Livro devolvido com sucesso!"}), 200

    return render_template("devolver_livro.html")

@app.route("/estatisticas")
def estatisticas():
    return render_template("estatisticas.html")

@app.route("/estatisticas/dados")
def estatisticas_dados():
    livros_por_categoria = defaultdict(int)
    for livro in livros:
        livros_por_categoria[livro["categoria"]] += 1

    emprestimos_por_usuario = defaultdict(int)
    livros_mais_emprestados = defaultdict(int)

    try:
        if os.path.exists(CAMINHO_HISTORICO):
            with open(CAMINHO_HISTORICO, "r", encoding="utf-8") as f:
                leitor = csv.reader(f)
                next(leitor, None)
                for linha in leitor:
                    isbn, usuario, _, status = linha
                    if status == "emprestado":
                        tipo = usuarios.get(usuario, {}).get("tipo", "desconhecido")
                        emprestimos_por_usuario[tipo] += 1
                        livros_mais_emprestados[isbn] += 1
    except Exception as e:
        print(f"Erro ao carregar histórico: {e}")

    # Ordenar e pegar os 5 livros mais emprestados
    top_livros = sorted(livros_mais_emprestados.items(), key=lambda x: x[1], reverse=True)[:5]

    # Criar a lista final com nome do livro
    livros_top = []
    for isbn, quantidade in top_livros:
        livro_info = next((livro for livro in livros if livro["isbn"] == isbn), None)
        if livro_info:
            livros_top.append({"titulo": livro_info["titulo"], "isbn": isbn, "quantidade": quantidade})

    return jsonify({
        "livros_por_categoria": dict(livros_por_categoria),
        "emprestimos_por_tipo": dict(emprestimos_por_usuario),
        "livros_mais_emprestados": livros_top
    })

def menu_textual():
    while True:
        print("\n=== Biblioteca ===")
        print("1. Listar livros")
        print("2. Listar usuários")
        print("3. Listar empréstimos")
        print("4. Cadastrar livro")
        print("5. Cadastrar usuário")
        print("6. Emprestar livro")
        print("7. Devolver livro")
        print("8. Estatísticas")
        print("9. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            busca = input("Digite um termo para busca (deixe em branco para listar todos): ").strip().lower()
            livros_filtrados = [livro for livro in livros if
                                busca in livro["titulo"].lower() or
                                busca in livro["autor"].lower() or
                                busca in livro["categoria"].lower()]

            if livros_filtrados:
                for livro in livros_filtrados:
                    print(f"{livro['titulo']} - {livro['autor']} ({livro['ano']})")
            else:
                print("Nenhum livro encontrado para a busca.")
        
        elif opcao == "2":
            if usuarios:
                for usuario in usuarios.values():
                    print(f"{usuario['id']} - {usuario['nome']} ({usuario['tipo']})")
            else:
                print("Não há usuários cadastrados.")
        
        elif opcao == "3":
            if emprestimos:
                for emp in emprestimos:
                    print(f"Livro ISBN: {emp['livro']} | Usuário: {emp['usuario']} | Data: {emp['data']}")
            else:
                print("Não há empréstimos registrados.")
        
        elif opcao == "4":
            titulo = input("Título: ")
            autor = input("Autor: ")
            ano = input("Ano: ")
            isbn = input("ISBN: ")
            categoria = input("Categoria: ")
            if any(l['isbn'] == isbn for l in livros):
                print("Erro: Livro com esse ISBN já cadastrado.")
            else:
                livros.append({"titulo": titulo, "autor": autor, "ano": ano, "isbn": isbn, "categoria": categoria})
                salvar_dados()
                print("Livro cadastrado com sucesso!")
        
        elif opcao == "5":
            id_usuario = input("ID(MATRICULA): ")
            nome = input("Nome: ")
            email = input("Email: ")
            tipo = input("Tipo (aluno, professor, visitante): ")
            if tipo not in TIPOS_USUARIOS:
                print("Erro: Tipo de usuário inválido.")
            elif id_usuario in usuarios:
                print("Erro: ID já cadastrado.")
            else:
                usuarios[id_usuario] = {"id": id_usuario, "nome": nome, "email": email, "tipo": tipo}
                salvar_dados()
                print("Usuário cadastrado com sucesso!")
        
        elif opcao == "6":
            isbn = input("ISBN do livro: ")
            id_usuario = input("ID do usuário: ")
            if any(emp["livro"] == isbn for emp in emprestimos):
                print("Erro: Livro já emprestado.")
            elif id_usuario not in usuarios:
                print("Erro: Usuário não encontrado.")
            else:
                emprestimos.append({"livro": isbn, "usuario": id_usuario, "data": datetime.now().strftime("%d/%m/%Y")})
                emprestimos_contagem[isbn] += 1
                salvar_dados()
                print("Livro emprestado com sucesso!")
        
        elif opcao == "7":
            isbn = input("ISBN do livro: ")
            id_usuario = input("ID do usuário: ")
            emprestimo = next((emp for emp in emprestimos if emp["livro"] == isbn and emp["usuario"] == id_usuario), None)
            if not emprestimo:
                print("Erro: Este livro não foi emprestado para este usuário.")
            else:
                emprestimos.remove(emprestimo)
                with open(CAMINHO_HISTORICO, "a", newline="", encoding="utf-8") as f:
                    escritor = csv.writer(f)
                    escritor.writerow([isbn, id_usuario, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "devolvido"])
                salvar_dados()
                print("Livro devolvido com sucesso!")
        
        elif opcao == "8":
            print("\n=== Estatísticas ===")
            print("Livros mais emprestados:")
            for isbn, contagem in sorted(emprestimos_contagem.items(), key=lambda x: x[1], reverse=True)[:5]:
                livro = next((l for l in livros if l["isbn"] == isbn), None)
                if livro:
                    print(f"{livro['titulo']} - {contagem} vezes")
        
        elif opcao == "9":
            print("Saindo...")
            break
        
        else:
            print("Opção inválida!")


# Função do Flask
def run_flask():
    app.run(debug=True, use_reloader=False)  # Usando use_reloader=False para evitar execução duplicada

if __name__ == "__main__":
    carregar_dados()

    # Rodando o Flask em um thread separado
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True  # Torna o thread "daemon", o que significa que o programa principal pode sair sem precisar esperar por ele
    flask_thread.start()

    # Chama o menu textual (onde o usuário escolhe a opção)
    menu_textual()
