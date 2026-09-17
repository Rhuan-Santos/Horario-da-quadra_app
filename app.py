from flask import Flask, render_template
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


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/nova_reserva")
def nova_reserva():
    return render_template("nova_reserva.html")


@app.get("/reservas")
def reserva():
    return render_template("reservas.html")


@app.get("/editar_reserva")
def editar_reserva():
    return render_template("editar_reserva.html")


try:
    conexao = conectar_banco()
    print("Banco conectado com sucesso!")
    conexao.close()
except mariadb.Error as erro:
    print("Erro ao conectar ao banco:", erro)


if __name__ == "__main__":
    app.run(debug=True)