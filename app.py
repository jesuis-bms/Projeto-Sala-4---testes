import os
import psycopg
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "troque-isso")

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    return psycopg.connect(DATABASE_URL)

def create_table():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    usuario TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS atividades (
                    id SERIAL PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    materia TEXT NOT NULL,
                    sala TEXT NOT NULL
                )
            """)
        conn.commit()

def seed_default_user():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM users WHERE usuario = %s",
                ("Juscelino Buarque Apesar de Todo Dia",)
            )
            existe = cursor.fetchone()

            if not existe:
                cursor.execute(
                    "INSERT INTO users (usuario, senha) VALUES (%s, %s)",
                    ("Juscelino Buarque Apesar de Todo Dia", "Scooby-doo")
                )
        conn.commit()

create_table()
seed_default_user()

@app.route("/")
def home():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, titulo, descricao, materia, sala
                FROM atividades
                ORDER BY id DESC
            """)
            atividades = cursor.fetchall()

    logado = "usuario" in session
    return render_template("index.html", atividades=atividades, logado=logado)

@app.route("/login", methods=["POST"])
def logar():
    usuario = request.form.get("user", "").strip()
    senha = request.form.get("senha", "").strip()

    if not usuario:
        return "Usuário inválido."
    if not senha:
        return "Senha inválida."

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM users WHERE usuario = %s AND senha = %s",
                (usuario, senha)
            )
            usuario_encontrado = cursor.fetchone()

    if usuario_encontrado:
        session["usuario"] = usuario
        return redirect(url_for("home"))
    return "Login inválido."

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("usuario", None)
    return redirect(url_for("home"))

def block():
    return "usuario" not in session

@app.route("/sala/<sala>")
def filtroSala(sala):
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, titulo, descricao, materia, sala
                FROM atividades
                WHERE sala = %s
            """, (sala,))
            atividades = cursor.fetchall()

    logado = "usuario" in session
    return render_template("index.html", atividades=atividades, logado=logado)

@app.route("/enviar", methods=["POST"])
def enviar():
    if block():
        return "Acesso negado."

    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    sala = request.form.get("sala", "").strip()
    materia = request.form.get("materia", "").strip()

    if not titulo:
        return "Título inválido. Digite algo."
    if not descricao:
        return "Descrição inválida. Digite algo."
    if not sala:
        return "Sala inválida. Tente novamente."
    if not materia:
        return "Matéria inválida. Tente novamente."

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO atividades (titulo, descricao, sala, materia)
                VALUES (%s, %s, %s, %s)
            """, (titulo, descricao, sala, materia))
        conn.commit()

    return redirect(url_for("filtroSala", sala=sala))

@app.route("/update/<int:id>", methods=["POST"])
def editar(id):
    if block():
        return "Acesso negado."

    novoTitulo = request.form.get("titulo", "").strip()
    novaDescricao = request.form.get("descricao", "").strip()
    novaMateria = request.form.get("materia", "").strip()
    sala = request.form.get("sala", "").strip()

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE atividades
                SET titulo = %s, descricao = %s, materia = %s
                WHERE id = %s
            """, (novoTitulo, novaDescricao, novaMateria, id))
        conn.commit()

    return redirect(url_for("filtroSala", sala=sala))

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if block():
        return "Acesso negado."

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM atividades WHERE id = %s", (id,))
        conn.commit()

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
