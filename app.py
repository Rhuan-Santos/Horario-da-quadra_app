from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Localização do banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "banco.db")


# =========================
# CONEXÃO COM O BANCO
# =========================

def conectar_banco():
    conexao = sqlite3.connect(DB_PATH)
    return conexao


# =========================
# CRIAR BANCO E TABELA
# =========================

def criar_banco():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            "Nome/turma" VARCHAR(45) NOT NULL,
            "Modalidade" VARCHAR(10) NOT NULL,
            "Horário" VARCHAR(7) NOT NULL,
            telefone VARCHAR(14),
            Dia INTEGER NOT NULL,
            "mês" INTEGER NOT NULL,
            ano INTEGER NOT NULL
        )
    """)

    conexao.commit()
    cursor.close()
    conexao.close()


# =========================
# PÁGINA INICIAL / AGENDA
# =========================

@app.get("/")
def home():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM horarios")

    reservas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "index.html",
        reservas=reservas
    )


# =========================
# NOVA RESERVA - FORMULÁRIO
# =========================

@app.get("/nova_reserva")
def nova_reserva():

    return render_template("nova_reserva.html")


# =========================
# NOVA RESERVA - SALVAR
# =========================

@app.post("/nova_reserva")
def salvar_reserva():

    nome_turma = request.form["nome_turma"]
    modalidade = request.form["modalidade"]
    horario = request.form["horario"]
    telefone = request.form["telefone"]
    dia = request.form["dia"]
    mes = request.form["mes"]
    ano = request.form["ano"]

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Verifica se já existe uma reserva
    # no mesmo dia e horário
    cursor.execute("""
        SELECT id
        FROM horarios
        WHERE "Horário" = ?
        AND Dia = ?
        AND "mês" = ?
        AND ano = ?
    """, (
        horario,
        dia,
        mes,
        ano
    ))

    conflito = cursor.fetchone()

    if conflito:

        cursor.close()
        conexao.close()

        return """
        <h2>Horário já reservado!</h2>
        <p>Já existe uma reserva para esse dia e horário.</p>
        <a href="/nova_reserva">Voltar</a>
        """, 400

    # Se não houver conflito, salva a reserva
    cursor.execute("""
        INSERT INTO horarios
        (
            "Nome/turma",
            "Modalidade",
            "Horário",
            telefone,
            Dia,
            "mês",
            ano
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        nome_turma,
        modalidade,
        horario,
        telefone,
        dia,
        mes,
        ano
    ))

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect("/")


# =========================
# LISTAR RESERVAS
# =========================

@app.get("/reservas")
def reservas():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM horarios")

    lista_reservas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "reservas.html",
        reservas=lista_reservas
    )


# =========================
# EDITAR RESERVA - FORMULÁRIO
# =========================

@app.get("/editar_reserva")
def editar_reserva():

    id_reserva = request.args.get("id")

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM horarios
        WHERE id = ?
        """,
        (id_reserva,)
    )

    reserva = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template(
        "editar_reserva.html",
        reserva=reserva
    )


# =========================
# EDITAR RESERVA - SALVAR
# =========================

@app.post("/editar_reserva")
def salvar_edicao():

    id_reserva = request.form["id"]

    nome_turma = request.form["nome_turma"]
    modalidade = request.form["modalidade"]
    horario = request.form["horario"]
    telefone = request.form["telefone"]
    dia = request.form["dia"]
    mes = request.form["mes"]
    ano = request.form["ano"]

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Verifica conflito, mas ignora
    # a própria reserva que está sendo editada
    cursor.execute("""
        SELECT id
        FROM horarios
        WHERE "Horário" = ?
        AND Dia = ?
        AND "mês" = ?
        AND ano = ?
        AND id != ?
    """, (
        horario,
        dia,
        mes,
        ano,
        id_reserva
    ))

    conflito = cursor.fetchone()

    if conflito:

        cursor.close()
        conexao.close()

        return """
        <h2>Horário já reservado!</h2>
        <p>Já existe outra reserva para esse dia e horário.</p>
        <a href="/editar_reserva?id=""" + str(id_reserva) + """">
            Voltar
        </a>
        """, 400

    # Atualiza a reserva
    cursor.execute("""
        UPDATE horarios
        SET
            "Nome/turma" = ?,
            "Modalidade" = ?,
            "Horário" = ?,
            telefone = ?,
            Dia = ?,
            "mês" = ?,
            ano = ?
        WHERE id = ?
    """, (
        nome_turma,
        modalidade,
        horario,
        telefone,
        dia,
        mes,
        ano,
        id_reserva
    ))

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect("/reservas")


# =========================
# CANCELAR RESERVA
# =========================

@app.post("/cancelar_reserva")
def cancelar_reserva():

    id_reserva = request.form["id"]

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM horarios
        WHERE id = ?
        """,
        (id_reserva,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect("/reservas")


# =========================
# INICIAR BANCO
# =========================

criar_banco()


# =========================
# EXECUTAR APLICAÇÃO
# =========================

if __name__ == "__main__":
    app.run(debug=True)