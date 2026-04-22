import os
import psycopg
import cloudinary
import cloudinary.uploader
from flask import Flask, render_template, request, redirect, url_for, session, flash


app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "key_pra_localhost"
)

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:1234@localhost:5432/teste"
)

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
                    sala TEXT NOT NULL,
                    imagem TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS imagens (
                id SERIAL PRIMARY KEY
                atividade_id INTEGER NOT NULL
                url TEXT NOT NULL
            """)
        conn.commit()

create_table()

def separar_atividades_por_sala(atividades):
    atividades_704 = [a for a in atividades if a[4] == "704"]
    atividades_705 = [a for a in atividades if a[4] == "705"]
    return atividades_704, atividades_705

@app.route("/")
def home():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, titulo, descricao, materia, sala, imagem
                FROM atividades
                ORDER BY id DESC
            """)
            atividades = cursor.fetchall()

    atividades_704, atividades_705 = separar_atividades_por_sala(atividades)
    logado = "usuario" in session

    return render_template(
        "index.html",
        atividades=atividades,
        logado=logado,
        atividades_704=atividades_704,
        atividades_705=atividades_705
    )

@app.route("/login", methods=["POST"])
def logar():
    usuario = request.form.get("user", "").strip()
    senha = request.form.get("senha", "").strip()

    if not usuario:
        flash("Usuário inválido.")
        return redirect(url_for("home"))

    if not senha:
        flash("Senha inválida.")
        return redirect(url_for("home"))

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

    flash("Login inválido.")
    return redirect(url_for("home"))

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
                SELECT id, titulo, descricao, materia, sala, imagem
                FROM atividades
                WHERE sala = %s
                ORDER BY id DESC
            """, (sala,))
            atividades = cursor.fetchall()

    atividades_704, atividades_705 = separar_atividades_por_sala(atividades)
    logado = "usuario" in session

    return render_template(
        "index.html",
        atividades=atividades,
        logado=logado,
        atividades_704=atividades_704,
        atividades_705=atividades_705
    )

@app.route("/enviar", methods=["POST"])
def enviar():
    if block():
        return "Acesso negado."

    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    sala = request.form.get("sala", "").strip()
    materia = request.form.get("materia", "").strip()
    imagens = request.files.getlist("imagens")
    nome_imagem = None

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
                RETURNING id
            """, (titulo, descricao, sala, materia))
            atividade_id = cursor.fetchone()[0]

     for imagem in imagens:
        if imagem and imagem.filename:
            resultado = cloudinary.uploader.upload(imagem)
            nome_imagem = resultado["secure_url"]

        cursor.execute("""
            INSERT INTO imagens (atividade_id, url)
            VALUES (%s, %s)
            """, (atividade_id, url_imagem))

    conn.commit(
    
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

    sala = request.form.get("sala", "").strip()

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM atividades WHERE id = %s", (id,))
        conn.commit()

    return redirect(url_for("filtroSala", sala=sala))

if __name__ == "__main__":
    app.run(debug=True)
