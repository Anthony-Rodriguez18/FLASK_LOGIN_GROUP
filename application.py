from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager,login_user,logout_user,login_required 
from flask_mysqldb import MySQL


from config import config

from models.ModelUser import ModelUser

from models.entities.User import User


app = Flask(__name__)


db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route("/") 
def inicio():
  return render_template("inicio.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['correo'], request.form['password'])
        logged_user = ModelUser.login(db, user) 
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)  #comprueba a clave hash
                return redirect(url_for('home'))
            else:
                flash("Contraseña invalida...")
                return render_template('Login.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('Login.html')
    else:
        return render_template('Login.html')

@app.route("/home") 
def home():
  return render_template("inicio.html")



@app.route("/productos") 
def productos():
  return render_template("productos.html")


@app.route("/signup/")
def show_signup_form():
    return render_template("signup_form.html")



def status_401(error):
    return redirect(url_for('Login.html'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


@app.route("/register", methods=["POST","GET"]) 
def register():
  return render_template("Register.html")

@app.route("/cart") 
def cart():
  return render_template("Cart.html")

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()