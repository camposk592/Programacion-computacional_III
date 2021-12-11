from flask import Flask
from flask import render_template,request,redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os


app = Flask(__name__)

mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)


CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA


@app.route("/")
def index():

    sql = "SELECT * FROM `peliculas`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    peliculas = cursor.fetchall()
    print(peliculas)
    conn.commit()


    return render_template('peliculas/index.html',peliculas=peliculas)


@app.route('/destroy/<int:idPeliculas>')
def destroy(idPeliculas):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT foto FROM peliculas WHERE IdPeliculas=%s",idPeliculas)
    fila=cursor.fetchall()

    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))

    cursor.execute("DELETE FROM peliculas WHERE idPeliculas=%s",(idPeliculas))
    conn.commit()
    return redirect('/')


@app.route('/edit/<int:idPeliculas>')
def edit(idPeliculas):

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM peliculas WHERE idPeliculas=%s",(idPeliculas))
    peliculas = cursor.fetchall()
    conn.commit()
    print(peliculas)


    return render_template('peliculas/edit.html',peliculas=peliculas)

@app.route('/update', methods=['POST'])
def update():

    _nombre =request.form['txtNombre']
    _telefono = request.form['txtTelefono']
    _pelicula =request.form['txtpelicula']
    _estado =request.form['txtEstado']
    _foto =request.files['txtFoto']
    IdPelicula = request.form['txtIdPeliculas']

    sql = "UPDATE `peliculas` SET `nombre`=%s, `telefono`=%s, `película`=%s, `estado de la película`=%s WHERE `idPeliculas`=%s;"
    datos = (_nombre,_telefono,_pelicula,_estado,IdPelicula)
    
    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

        cursor.execute("SELECT foto FROM peliculas WHERE IdPeliculas=%s",IdPelicula)
        fila=cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))

        cursor.execute("UPDATE `peliculas` SET `foto`=%s WHERE `idPeliculas`=%s",(nuevoNombreFoto,IdPelicula))
        conn.commit()



    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

@app.route("/create")
def create():

    return render_template('peliculas/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre =request.form['txtNombre']
    _telefono = request.form['txtTelefono']
    _pelicula =request.form['txtpelicula']
    _estado =request.form['txtEstado']

    _foto =request.files['txtFoto']

    'concatenar la foto'
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    sql = "INSERT INTO `peliculas` (`idPeliculas`, `nombre`, `telefono`, `película`, `estado de la película`, `foto`) VALUES (NULL,%s,%s,%s,%s,%s);"
    datos = (_nombre,_telefono,_pelicula,_estado,nuevoNombreFoto)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return render_template('peliculas/index.html')




if __name__ == '__main__':
    app.run(debug=True)