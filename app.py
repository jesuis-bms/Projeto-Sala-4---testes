import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "q0d10v31."

def get_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    return conn, cursor


def create_table():
    conn, cursor = get_db()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS atividades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        materia TEXT NOT NULL,
        sala TEXT NOT NULL 
    );
    """)

    conn.commit()
    conn.close()


create_table()

@app.route("/")
def home():
    conn, cursor = get_db()

    cursor.execute("SELECT * FROM atividades ORDER BY id DESC")
    atividades = cursor.fetchall()

    conn.close()

    logado = "usuario" in session
    return render_template("index.html", atividades=atividades, logado=logado)

@app.route("/criar-admin")
def criar_admin():
    conn, cursor = get_db()
    cursor.execute(
        "INSERT INTO users (usuario, senha) VALUES (?, ?)",
        ("Deadlife", "67889")
    )
    conn.commit()
    conn.close()
    return "Usuário criado."

@app.route("/login", methods=["POST"])
def logar():
    usuario = request.form.get("user", "").strip()
    senha = request.form.get("senha", "").strip()

    conn, cursor = get_db()

    cursor.execute("SELECT id, usuario, senha FROM users")
    todos = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM users WHERE usuario = ? AND senha = ?",
        (usuario, senha)
    )
    usuario_encontrado = cursor.fetchone()

    conn.close()

    if usuario_encontrado:
        session["usuario"] = usuario
        return redirect(url_for("home"))
    else:
        return f"Login inválido. Recebi user={usuario!r}, senha={senha!r}, banco={todos!r}"

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("usuario", None)
    return redirect(url_for("home"))

def block():
    if "usuario" not in session:
        return True
    return False

@app.route("/sala/<sala>")
def filtroSala(sala):
    conn, cursor = get_db()
    cursor.execute(
        "SELECT * FROM atividades WHERE sala = ?",
        (sala,)
    )
    atividades = cursor.fetchall()

    conn.close()

    logado = "usuario" in session
    return render_template("index.html", atividades=atividades, logado=logado)

@app.route("/enviar", methods=["POST"])
def enviar():

    if block():
        return "Acesso negado."

    conn, cursor = get_db()

    titulo = request.form.get("titulo")
    descricao = request.form.get("descricao")
    sala = request.form.get("sala")
    materia = request.form.get("materia")

    if not titulo or titulo.strip() == "":
        return "Título inválido. Digite algo."
    elif not descricao or descricao.strip() == "":
        return "Descrição inválida. Digite algo."
    elif not sala or sala.strip() == "":
        return "Sala inválida. Tente novamente."
    elif not materia or materia.strip() == "":
        return "Matéria inválida. Tente novamente."
    
    cursor.execute(
        "INSERT INTO atividades (titulo, descricao, sala, materia) VALUES (?, ?, ?, ?)",
        (titulo, descricao, sala, materia)
    )
    
    conn.commit()
    conn.close()

    return redirect(url_for("filtroSala", sala=sala))
    

@app.route("/update/<int:id>", methods=["POST"])
def editar(id):

    if block():
        return "Acesso negado."
    
    novoTitulo = request.form.get("titulo")
    novaDescricao = request.form.get("descricao")
    novaMateria = request.form.get("materia")
    sala = request.form.get("sala")

    conn, cursor = get_db()

    cursor.execute(
        "UPDATE atividades SET titulo = ?, descricao = ?, materia = ? WHERE id = ?",
        (novoTitulo, novaDescricao, novaMateria, id)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("filtroSala", sala=sala))

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):

    if block():
        return "Acesso negado."
    
    conn, cursor = get_db()

    cursor.execute("DELETE FROM atividades WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
