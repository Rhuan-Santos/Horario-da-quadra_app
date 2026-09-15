from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
