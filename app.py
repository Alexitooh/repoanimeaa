from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

class DAO_Autenticacion:
    def __init__(self, password):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="animefinder"  # Cambié el nombre de la base de datos
        )
        self.mycursor = self.mydb.cursor()

    def autenticar_usuario(self, usuario, contraseña):
        sql = "SELECT 1 FROM usuarios WHERE usuario = %s AND contraseña = %s"
        val = (usuario, contraseña)
        
        self.mycursor.execute(sql, val)
        resultado = self.mycursor.fetchone()
        
        return resultado is not None

class DAO_Recomendaciones:
    def __init__(self, password):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="animefinder"
        )
        self.mycursor = self.mydb.cursor()

    def obtener_recomendaciones(self, anime_buscado=None):
        if anime_buscado:
            sql = "SELECT * FROM animes WHERE nombre LIKE %s"
            self.mycursor.execute(sql, (f'%{anime_buscado}%',))
        else:
            sql = "SELECT * FROM animes LIMIT 10"
            self.mycursor.execute(sql)
        
        resultados = self.mycursor.fetchall()
        return resultados

# Instancias de los DAOs
dao_auth = DAO_Autenticacion("tu_password")
dao_recomendaciones = DAO_Recomendaciones("tu_password")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('username')
    contraseña = data.get('password')
    
    if dao_auth.autenticar_usuario(usuario, contraseña):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Credenciales incorrectas'})

@app.route('/api/recomendaciones', methods=['POST'])
def obtener_recomendaciones():
    data = request.get_json()
    anime_buscado = data.get('animeName', '')
    
    resultados = dao_recomendaciones.obtener_recomendaciones(anime_buscado)
    
    # Convertir resultados a formato JSON
    animes = []
    for row in resultados:
        anime = {
            'id': row[0],
            'nombre': row[1],
            'genero': row[2],
            'puntuacion': row[3],
            'descripcion': row[4]
        }
        animes.append(anime)
    
    return jsonify({'animes': animes})

if __name__ == '__main__':
    app.run(debug=True)