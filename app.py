from flask import Flask, render_template, request, redirect
import mariadb

app = Flask(__name__)


def conectar_banco():
    conexao = mariadb.connect(
        host="localhost",
        user="flask",
        password="flask123",
        database="quadra"
    )
    return conexao


# Página inicial
@app.get("/")
def home():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM horarios")

    reservas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("index.html", reservas=reservas)


# Nova reserva - abrir formulário
@app.get("/nova_reserva")
def nova_reserva():
    return render_template("nova_reserva.html")


# Nova reserva - salvar no banco
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

    cursor.execute("""
        INSERT INTO horarios
        (`Nome/turma`, `Modalidade`, `Horário`, `telefone`, `Dia`, `mês`, `ano`)
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


# Página com todas as reservas
@app.get("/reservas")
def reserva():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM horarios")

    reservas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("reservas.html", reservas=reservas)


# Abrir página de edição
@app.get("/editar_reserva")
def editar_reserva():

    id_reserva = request.args.get("id")

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM horarios WHERE id = ?",
        (id_reserva,)
    )

    reserva = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template(
        "editar_reserva.html",
        reserva=reserva
    )


# Salvar edição
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

    cursor.execute("""
        UPDATE horarios
        SET
            `Nome/turma` = ?,
            `Modalidade` = ?,
            `Horário` = ?,
            `telefone` = ?,
            `Dia` = ?,
            `mês` = ?,
            `ano` = ?
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


if __name__ == "__main__":
    app.run(debug=True)