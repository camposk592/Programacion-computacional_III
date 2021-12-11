from flask import Flask
from flask import render_template,request,redirect
from flaskext.mysql import MySQL
from datetime import datetime


app = Flask(__name__)

mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)


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

    cursor.execute("DELETE FROM peliculas WHERE idPeliculas=%s",(idPeliculas))
    conn.commit()
    return redirect('/')


@app.route('/edit/<int:idPeliculas>')
def edit(idPeliculas):


    
    return render_template('peliculas/edit.html')


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