from flask import Flask, render_template, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "chave_secreta"
app.static_folder = "static"

GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''

# Simulação de banco de dados
usuarios = {"admin": "admin123", "usuario": "user123"}
images = [dict(name="Imagem A", link="./imagem", image_url="png/placeholder.png"), 
          dict(name="Imagem B", link="./imagem", image_url="png/placeholder.png"), 
          dict(name="Imagem C", link="./imagem", image_url="png/placeholder.png"), 
          ]
docker_images = []

@app.route("/")
def index():
    return redirect(url_for("login"))
          
# Configuração do OAuth2
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params={'scope': 'openid email profile'},
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/')
def home():
    user = session.get('user')
    if user:
        return render_template("dashboard.html", images=images, is_admin=session["user"] == "admin")
    return '<a href="/login">Entrar com o Google</a>'

@app.route("/login")
def login():
    return google.authorize_redirect(url_for('authorize', _external=True))
          
@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    session['user'] = user_info
    return redirect(url_for('home'))
          
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
