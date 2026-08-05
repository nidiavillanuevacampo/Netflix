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
app.config['MYSQL_USER'] = 'sql10834549'
app.config['MYSQL_PASSWORD'] = 'f2Pmwc9SWY'
app.config['MYSQL_DB'] = 'sql10834549'
mysql = MySQL(app)


@app.route('/')
def home():
    return redirect('/login')

@app.route('/home')
def inicio():
    if 'id_usuario' not in session:
        return redirect('/login')

    peliculas = obtener_populares()
    banner = random.choice(peliculas) if peliculas else None

    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT p.idPelicula, p.titulo, p.sinopsis, p.año, p.duracion, p.imagen_url, g.nombre
            FROM peliculas p
            LEFT JOIN generos g ON p.idGenero = g.idGenero
        """)
        peliculas_locales = cur.fetchall()
    except Exception as e:
        print("Error al obtener peliculas locales:", e)
        peliculas_locales = []
    finally:
        cur.close()

    return render_template(
        'home.html',
        banner=banner,
        peliculas=peliculas,
        peliculas_locales=peliculas_locales
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT idUsuario, nombre, usuario, correo, password, lActivo
            FROM usuarios
            WHERE usuario = %s
            AND password = %s
            AND lActivo = 1
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

            cur.execute("DELETE FROM token WHERE idUsuario = %s", (usuario[0],))
            
            cur.execute(
                """
                INSERT INTO token (idUsuario, cToken, dFecha)
                VALUES (%s, %s, %s)
                """,
                (usuario[0], token, fecha)
            )
            
            cur.close()
            mysql.connection.commit()

            return redirect("/home")

        cur.close()
        return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")

@app.route('/usuarios')
def clientes():
    if 'id_usuario' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT
        u.idUsuario,
        u.nombre,
        u.usuario,
        u.correo,
        p.nombre AS plan
    FROM usuarios u
        LEFT JOIN suscripciones s
            ON u.idUsuario = s.idUsuario
        LEFT JOIN planes p
            ON s.idPlan = p.idPlan
    """)
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


@app.route('/generos')
def generos():
    if 'id_usuario' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM generos")
    data = cur.fetchall()
    cur.close()
    return render_template("generos.html", Generos=data)


@app.route('/generos/agregar', methods=['POST'])
def agregar_genero():
    if 'id_usuario' not in session:
        return redirect('/login')
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "INSERT INTO generos (nombre, descripcion) VALUES (%s, %s)",
            (nombre, descripcion)
        )
        mysql.connection.commit()
    except Exception as e:
        print("Error al agregar genero:", e)
    finally:
        cur.close()
    return redirect('/generos')


@app.route('/generos/editar/<int:id>', methods=['POST'])
def editar_genero(id):
    if 'id_usuario' not in session:
        return redirect('/login')
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "UPDATE generos SET nombre = %s, descripcion = %s WHERE idGenero = %s",
            (nombre, descripcion, id)
        )
        mysql.connection.commit()
    except Exception as e:
        print("Error al editar genero:", e)
    finally:
        cur.close()
    return redirect('/generos')


@app.route('/generos/eliminar/<int:id>')
def eliminar_genero(id):
    if 'id_usuario' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM generos WHERE idGenero = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        print("Error al eliminar genero:", e)
    finally:
        cur.close()
    return redirect('/generos')


@app.route('/planes')
def planes():
    if 'id_usuario' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM planes")
    data = cur.fetchall()
    cur.close()
    return render_template("planes.html", Planes=data)

from datetime import datetime

@app.route('/suscripcion/agregar', methods=['POST'])
def agregar_suscripcion():

    if 'id_usuario' not in session:
        return redirect('/login')

    idUsuario = session['id_usuario']

    idPlan = request.form.get('idPlan')
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    telefono = request.form.get('telefono')
    metodo = request.form.get('metodo')

    fecha = datetime.now()

    cur = mysql.connection.cursor()

    try:

        cur.execute("""
        INSERT INTO suscripciones
        (
            idUsuario,
            idPlan,
            nombre,
            correo,
            telefono,
            metodoPago,
            fecha
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """,

        (
            idUsuario,
            idPlan,
            nombre,
            correo,
            telefono,
            metodo,
            fecha
        ))

        mysql.connection.commit()

    except Exception as e:

        print(e)

    finally:

        cur.close()

    return redirect('/planes')

@app.route('/peliculas_db')
def peliculas_db():
    if 'id_usuario' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.idPelicula, p.titulo, p.sinopsis, p.año, p.duracion, p.imagen_url, p.idGenero, g.nombre
        FROM peliculas p
        LEFT JOIN generos g ON p.idGenero = g.idGenero
    """)
    peliculas = cur.fetchall()
    
    cur.execute("SELECT idGenero, nombre FROM generos")
    generos = cur.fetchall()
    cur.close()
    
    return render_template("peliculas_db.html", Peliculas=peliculas, Generos=generos)


@app.route('/peliculas_db/agregar', methods=['POST'])
def agregar_pelicula_db():
    if 'id_usuario' not in session:
        return redirect('/login')
    titulo = request.form.get('titulo')
    sinopsis = request.form.get('sinopsis')
    anio = request.form.get('anio')
    duracion = request.form.get('duracion')
    imagen_url = request.form.get('imagen_url')
    idGenero = request.form.get('idGenero')
    
    if not idGenero:
        idGenero = None
        
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            """
            INSERT INTO peliculas (titulo, sinopsis, anio, duracion, imagen_url, idGenero)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (titulo, sinopsis, anio, duracion, imagen_url, idGenero)
        )
        mysql.connection.commit()
    except Exception as e:
        print("Error al agregar pelicula:", e)
    finally:
        cur.close()
    return redirect('/peliculas_db')

@app.route('/peliculas_db/editar/<int:id>', methods=['POST'])
def editar_pelicula_db(id):
    if 'id_usuario' not in session:
        return redirect('/login')
    titulo = request.form.get('titulo')
    sinopsis = request.form.get('sinopsis')
    anio = request.form.get('anio')
    duracion = request.form.get('duracion')
    imagen_url = request.form.get('imagen_url')
    idGenero = request.form.get('idGenero')
    
    if not idGenero:
        idGenero = None
        
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            """
            UPDATE peliculas 
            SET titulo = %s, sinopsis = %s, anio = %s, duracion = %s, imagen_url = %s, idGenero = %s 
            WHERE idPelicula = %s
            """,
            (titulo, sinopsis, anio, duracion, imagen_url, idGenero, id)
        )
        mysql.connection.commit()
    except Exception as e:
        print("Error al editar pelicula:", e)
    finally:
        cur.close()
    return redirect('/peliculas_db')

@app.route('/peliculas_db/eliminar/<int:id>')
def eliminar_pelicula_db(id):
    if 'id_usuario' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM peliculas WHERE idPelicula = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        print("Error al eliminar pelicula:", e)
    finally:
        cur.close()
    return redirect('/peliculas_db')

@app.route('/peliculas')
def peliculas():

    if 'id_usuario' not in session:
        return redirect('/login')

    peliculas = obtener_populares()

    return render_template(
        'peliculas.html',
        peliculas=peliculas
    )

@app.route('/categoria/<int:genero>')
def categoria(genero):
    peliculas = obtener_por_genero(genero)

    print("Género:", genero)
    print("Películas:", peliculas)

    return render_template(
        'peliculas.html',
        peliculas=peliculas
    )

@app.route('/ajax', methods=['GET', 'POST'])
def ajax():
    return '{"result"}:"20"'

@app.route('/logout')
def logout():
    if 'id_usuario' in session and 'token' in session:
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM token WHERE idUsuario = %s AND cToken = %s", (session['id_usuario'], session['token']))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            print("Error al eliminar token al cerrar sesion:", e)
    session.clear()
    return redirect('/login')

@app.before_request
def controlar_inactividad():
    if request.path.startswith('/static') or request.path in ('/login', '/logout') or request.endpoint == 'static':
        return

    if 'id_usuario' not in session:
        return redirect('/login')

    if 'ultimo_movimiento' in session:
        ultimo = datetime.fromisoformat(session['ultimo_movimiento'])
        if datetime.now() - ultimo > timedelta(minutes=2):
            if 'token' in session:
                try:
                    cur = mysql.connection.cursor()
                    cur.execute("DELETE FROM token WHERE idUsuario = %s AND cToken = %s", (session['id_usuario'], session['token']))
                    mysql.connection.commit()
                    cur.close()
                except Exception as e:
                    print("Error al eliminar token por inactividad:", e)
            session.clear()
            return redirect('/login')

    if 'token' in session:
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT idToken FROM token WHERE idUsuario = %s AND cToken = %s", (session['id_usuario'], session['token']))
            token_db = cur.fetchone()
            cur.close()
            if not token_db:
                session.clear()
                return redirect('/login')
        except Exception as e:
            print("Error al validar token de base de datos:", e)

    session['ultimo_movimiento'] = datetime.now().isoformat()

if __name__ == '__main__':
    app.run(port = 5000, debug = True)