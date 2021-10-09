from logging import log
from flask import Flask, render_template, request, url_for,flash, jsonify
import yagmail
import utils
import os
from formulario import FormInicio
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from mensaje import mensajes

app= Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/login', methods=["GET","POST"])
def login():
    try:
        if request.method=="POST":
            user1=request.form["usuario"]
            pass1=request.form["password"]

            if not user1:
                error="Debes ingresar el usuario"
                print(error)
                return render_template("login.html")
            if not pass1:
                error="Debes ingresar la contraseña"
                print(error)
                return render_template("login.html")
            
            if user1=="Prueba" and pass1=="Prueba123":
                return redirect("mensaje")
            else:
                error="Usuario o contraseña errados"
                flash(error)
                return render_template("login.html")

        return render_template("login.html")

    except:
        return render_template("register.html")

 

@app.route("/register" , methods=["GET","POST"])
def register():
    try:
        if request.method=="POST":
            user1=request.form["nombre"]
            pass1=request.form["contrasena"]
            email=request.form["correo"]
            error = None
            
            if not utils.isUsernameValid(user1):
                error ="El usuario no es correcto"
                flash(error)
                return render_template("register.html")
            
            if not utils.isPasswordValid(pass1):
                error="Password invalido"
                flash(error)
                return render_template("register.html")
            
            if not utils.isEmailValid(email):
                error="Correo invalido"
                flash(error)
                return render_template("register.html")

            yag=yagmail.SMTP("pruebamintic2022","minTIC2022*")
            yag.send(to=email, subject="Activa tu cuenta", contents="Bienvenido, usa este link para activar tu cuenta")
            flash("Revisa tu correo para activar tu cuenta")        
            return render_template("login.html")
        else:
            return render_template("register.html")
    except:
        return render_template("register.html")


@app.route('/contacto',methods=['GET','POST'])
def conacto():
    form = FormInicio()
    
    if(form.validate_on_submit()):
        flash('Inicio de sesion solicitado por el usuario {form.nombre.data}')
        return redirect( url_for("gracias"))
    
    return render_template('contacto.html',
                           titulo='Formulario', form=form)
    
@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

@app.route("/mensaje", methods=["GET","POST"])
def mensaje():
    return jsonify({
        "Usu": "Mensajes de usuario",
        "mensajes":mensajes
    })
            
if __name__ == '__main__':
    app.run(debug=True, port=8080)