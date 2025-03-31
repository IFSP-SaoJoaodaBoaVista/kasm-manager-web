from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "chave_secreta"

# Simulação de banco de dados
usuarios = {"admin": "admin123", "usuario": "user123"}
images = [dict(name="Imagem A", link="./imagem", image_url="png/placeholder.png"), 
          dict(name="Imagem B", link="./imagem", image_url="png/placeholder.png"), 
          dict(name="Imagem C", link="./imagem", image_url="png/placeholder.png"), 
          ]
docker_images = []

app.static_folder = "static"

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in usuarios and usuarios[username] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", images=images, is_admin=session["username"] == "admin")

@app.route("/add_docker", methods=["POST"])
def add_docker():
    if "username" in session and session["username"] == "admin":
        image_name = request.form["image_name"]
        docker_images.append(image_name)
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)