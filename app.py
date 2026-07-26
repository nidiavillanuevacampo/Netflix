from werkzeug import datastructures
import hashlib
import uuid
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from tmdb import obtener_populares, obtener_por_genero
from flask import session
from datetime import datetime, timedelta
from flask import session, redirect
import random
app = Flask (__name__)
app.secret_key = "uppvideo2026"


app.config['MYSQL_HOST'] = 'sql10.freesqldatabase.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'sql10833934'
app.config['MYSQL_PASSWORD'] = 'cJq5tmppE4'
app.config['MYSQL_DB'] = 'sql10833934'
mysql = MySQL(app)


@app.route('/')
def home():
    return redirect('/login')

@app.route('/home')
def inicio():

    if 'id_usuario' not in session:
        return redirect('/login')

    peliculas = obtener_populares()

    banner = random.choice(peliculas)

    return render_template(
        'home.html',
        banner=banner,
        peliculas=peliculas
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()

        cur.execute(
            """
            SELECT *
            FROM usuarios
            WHERE usuario = %s
            AND password = %s
            """,
            (username, password),
        )

        usuario = cur.fetchone()

        if usuario:

            fecha = datetime.now()
            token = str(uuid.uuid4())
            
            session["id_usuario"] = usuario[0]
            session["nombre"] = usuario[1]
            session["usuario"] = usuario[2]
            session["token"] = token
            session["ultimo_movimiento"] = fecha.isoformat()    

            cur.execute(""" 

            INSERT INTO token
            (idUsuario,cToken,dFecha)VALUES(%s,%s,%s)""",(usuario[0],token,fecha))
            
            cur.close()
            mysql.connection.commit()

            return redirect("/home")

        cur.close()
        return "Usuario o contraseña incorrectos"

    return render_template("login.html")

@app.route('/usuarios')
def clientes():
    if 'id_usuario' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    data = cur.fetchall()
    cur.close()
    return render_template("usuarios.html", Usuarios = data)


@app.route('/usuarios/agregar', methods=['POST'])
def agregar_usuario():
    if 'id_usuario' not in session:
        return redirect('/login')
    nombre = request.form.get('nombre')
    usuario = request.form.get('usuario')
    correo = request.form.get('correo')
    password = request.form.get('password')
    
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "INSERT INTO usuarios (nombre, usuario, correo, password, lActivo) VALUES (%s, %s, %s, %s, 1)",
            (nombre, usuario, correo, password)
        )
        mysql.connection.commit()
    except Exception as e:
        print("Error al agregar usuario:", e)
    finally:
        cur.close()
    return redirect('/usuarios')


@app.route('/usuarios/editar/<int:id>', methods=['POST'])
def editar_usuario(id):
    if 'id_usuario' not in session:
        return redirect('/login')
    nombre = request.form.get('nombre')
    usuario = request.form.get('usuario')
    correo = request.form.get('correo')
    password = request.form.get('password')
    
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "UPDATE usuarios SET nombre = %s, usuario = %s, correo = %s, password = %s WHERE idUsuario = %s",
            (nombre, usuario, correo, password, id)
        )
        mysql.connection.commit()
    except Exception as e:
        print("Error al editar usuario:", e)
    finally:
        cur.close()
    return redirect('/usuarios')


@app.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):
    if 'id_usuario' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM usuarios WHERE idUsuario = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        print("Error al eliminar usuario:", e)
    finally:
        cur.close()
    return redirect('/usuarios')


@app.route('/peliculas/<id>')
def peliculas(id):
    return render_template('peliculas.html', ID= id)

@app.route('/ajax', methods=['GET', 'POST'])
def ajax():
    return '{"result"}:"20"'

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

@app.before_request
def controlar_inactividad():

    if 'ultimo_movimiento' in session:

        ultimo = datetime.fromisoformat(session['ultimo_movimiento'])

        if datetime.now() - ultimo > timedelta(minutes=1):

            session.clear()

            return redirect('/login')

    session['ultimo_movimiento'] = datetime.now().isoformat()

@app.route('/categoria/<int:genero>')
def categoria(genero):
    peliculas = obtener_por_genero(genero)

    print("Género:", genero)
    print("Películas:", peliculas)

    return render_template(
        'peliculas.html',
        peliculas=peliculas
    )


if __name__ == '__main__':
    app.run(port = 5000, debug = True)