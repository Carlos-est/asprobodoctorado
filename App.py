from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_mysqldb import MySQL
import functions
from werkzeug.exceptions import HTTPException
from forms import FormForward
import datetime
import dateutil.parser
import funcionesGenerales
import nuevasFuncionesChulucanas
import functionsChulucanas
from forms import FormIndicadoresCultivo
from forms import FormBiomasa
from forms import FormPrediction
import numpy as np
""" loginv  """
from flask import Flask, render_template, request, redirect, url_for, flash
#from config import config
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect

#from flask_login import LoginManager
from flask_login import LoginManager, login_user,logout_user, login_required


from models.ModelUser import ModelUser

from models.entities.User import User

app = Flask(__name__)


#MYSQL CONECTION
app.config['MYSQL_HOST'] = 'labsac.com'
app.config['MYSQL_USER'] = 'labsacco_dia'
app.config['MYSQL_PASSWORD'] = 'ciba15153232'
app.config['MYSQL_DB'] = 'labsacco_banano'
 #db=mysql.connector.connect( host="labsac.com",user="labsacco_dia", password="ciba15153232", database="labsacco_banano")
       
#SETTINGS
app.secret_key = 'mysecretkeyRepDom'
#app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)
#variables = variables()

### login
db=MySQL(app)
login_manager_app=LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        print("dentro de post")
        print(request.form['username'])
        print(request.form['password'])
        ###COMPARAR
        print("antes de user")
        user = User(0, request.form['username'], request.form['password'])
        print("despues deuser:", user)
        logged_user = ModelUser.login(db, user)
        print("antes de los if")
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                print("usuario validado ")
                return redirect(url_for('home'))

            else:
                flash("invalid password")
                return render_template('auth/login.html')

        else:
            flash("User not found")

            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('index.html')


@app.route('/formVariables')
@login_required
def formVariables():
    data = functionsChulucanas.graficas()
    estacion = "Ubicado en Buenos Aires-Morropón"
    session['data'] = data
    session['estacion'] = estacion

    fechas = [row[0] for row in data]
    tempPromedio = [row[1] for row in data]
    temp_max = [row[2] for row in data]
    humedad = [row[3] for row in data]
    temp_min = [row[4] for row in data]
 
    #return render_template('viewBiomasa.html',valor1 = valor1, valor2 = valor2, valor3=valor3,  estacionName = estacionName)
    return render_template('formVariables.html', data = data, fechas = fechas ,tempPromedio =tempPromedio,temp_max = temp_max, humedad =humedad,temp_min=temp_min ,estacionName = estacion)


@app.route('/formprediction')
@login_required
def formPrediction():
    """ estacionName = "CHULUCANAS" 
    session['estacionName'] = estacionName """
    cur = db.connection.cursor()
    cur.execute("SELECT fc.ID, fc.FECHA, fc.DESCRIPCION FROM F_CORRECTIVA AS fc ORDER BY fc.ID DESC LIMIT 2")
    dataF1 = cur.fetchall()
    for h in dataF1:
        print("valores de BD:", h)
    dataF1_1=dataF1[0][1]
    print("Data f2:", dataF1_1, type(dataF1_1))
    cur.execute("SELECT fp.ID, fp.FECHA, fp.DESCRIPCION FROM F_PREVENTIVA AS fp ORDER BY fp.ID DESC LIMIT 2")
    dataF2 = cur.fetchall()
    dataF1_2=dataF2[0][1]
    cur.execute("SELECT fl.ID, fl.FECHA, fl.DESCRIPCION FROM F_LIMPIEZA AS fl ORDER BY fl.ID DESC LIMIT 2")
    dataL = cur.fetchall()
    dataL_L=dataL[0][1]
    formPrediction = FormPrediction()

    return render_template('formPrediction.html', form = formPrediction, datosC=dataF1, datosP=dataF2,datosL=dataL, dataF1_1=dataF1_1, dataF1_2=dataF1_2,dataL_L=dataL_L)


@app.route('/viewPrediction', methods=['POST'])
@login_required
def viewPrediction():
    cur = db.connection.cursor()
    cur.execute("SELECT fc.ID, fc.FECHA, fc.DESCRIPCION FROM F_CORRECTIVA AS fc ORDER BY fc.ID DESC LIMIT 2")
    dataF1 = cur.fetchall()
    dataF1_1=dataF1[0][1]
    cur.execute("SELECT fp.ID, fp.FECHA, fp.DESCRIPCION FROM F_PREVENTIVA AS fp ORDER BY fp.ID DESC LIMIT 2")
    dataF2 = cur.fetchall()
    dataF1_2=dataF2[0][1]
    cur.execute("SELECT fl.ID, fl.FECHA, fl.DESCRIPCION FROM F_LIMPIEZA AS fl ORDER BY fl.ID DESC LIMIT 2")
    dataL = cur.fetchall()
    dataL_L=dataL[0][1]
    print("Data f2_2:", dataF1_1, type(dataF1_1))
    if request.method == 'POST':
        ID_parcela=request.form['ID_parcela']
        """ fechaPredictionF1 = request.form['fechaPredictionF1']
        fechaPredictionF2 = request.form['fechaPredictionF2']  
        fechaPredictionC = request.form['fechaPredictionC'] """  
        fechaPredictionF1 = dataF1_1
        fechaPredictionF2 = dataF1_2
        fechaPredictionC = dataL_L
        estacion = request.form['cmbEstacion']
        session['fechaPredictionF1'] = fechaPredictionF1
        session['fechaPredictionF2'] = fechaPredictionF2
        session['fechaPredictionC'] = fechaPredictionC
        session['ID_parcela'] = ID_parcela
        session['estacion'] = estacion
        print("parcela ID:", ID_parcela)
        #print("valores obtenidos ANTES de cambio de fecha:",fechaPredictionF1)
        ##llamamos a la funcion para cambiar el formato de la fecha insertada
        """ fechaPredictionF1 = funcionesGenerales.cambiar_formato_fecha(fechaPredictionF1)
        fechaPredictionF2 = funcionesGenerales.cambiar_formato_fecha(fechaPredictionF2)
        fechaPredictionC = funcionesGenerales.cambiar_formato_fecha(fechaPredictionC) """
        #print("valores obtenidos despues de cambio de fecha:",fechaPredictionF1)
        if (estacion=="1"):
            estacionName="ASPROBO"
            session['estacionName']= estacionName
            print("antes de data...")
            data, evaluacion_plagas =nuevasFuncionesChulucanas.Prediccion(fechaPredictionF1,fechaPredictionF2,fechaPredictionC,int(ID_parcela))
            print("data filtrada:",data)
            print("evaluación de plagas:", evaluacion_plagas)
            data=data[-7:]
            fechas = [row[0] for row in data]
            predicciones = [row[1] for row in data]
            #print("predicciones:", predicciones)

        #return render_template('viewprediction.html', fechaF1 = fechaPredictionF1, fechaF2 = fechaPredictionF2, fechaC = vafechaPredictionC, fechas = fechas, predicciones= predicciones, datosCompletos = data)
        return render_template('viewprediction.html', fechaF1 = fechaPredictionF1, fechaF2 = fechaPredictionF2, fechaC = fechaPredictionC, fechas=fechas, predicciones=predicciones, datosCompletos=data, evaluacion_plagas = evaluacion_plagas)

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e

    flash('Error: Verifique los datos ingresados')
    return render_template("formError.html", e=e), 500


def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1> Página no encontrada </h1>", 404

if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(port=3000, debug=True)
    