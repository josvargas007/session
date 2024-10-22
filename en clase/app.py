from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Clave secreta para cifrar la sesión

# Base de datos de usuarios (en producción, utiliza una base de datos real)
usuarios = {
    "juan": generate_password_hash("clavesecreta1"),
    "maria": generate_password_hash("clavesecreta2")
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contraseña = request.form["contraseña"]
        
        if usuario in usuarios and check_password_hash(usuarios[usuario], contraseña):
            session["usuario"] = usuario
            return redirect(url_for("bienvenida"))
        else:
            return render_template("login.html", error="Credenciales inválidas")
    return render_template("login.html")

@app.route("/bienvenida")
def bienvenida():
    if "usuario" in session:
        return render_template("bienvenida.html", usuario=session["usuario"])
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
