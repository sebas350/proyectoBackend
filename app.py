from flask import Flask ,jsonify ,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://pysebas:prueba1234@pysebas.mysql.pythonanywhere-services.com/pysebas$proyect'
# URI de la BBDD                    driver de la BD  user:clave@URLBBDD/nombreBBDD

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


# defino las tablas
class Users(db.Model):   # la clase Producto hereda de db.Model de SQLAlquemy
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    password=db.Column(db.String(100))

    def __init__(self,name,email,password): #crea el  constructor de la clase
        self.name=name # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.email=email
        self.password=password

#  si hay que crear mas tablas , se hace aqui

with app.app_context():
    db.create_all()  # aqui crea todas las tablas si es que no estan creadas
#  ************************************************************
class UsersSchema(ma.Schema):
    class Meta:
        fields=('id','name','email','password')


user_schema=UsersSchema()  # El objeto producto_schema es para traer un producto
users_schema=UsersSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto


@app.route('/',methods=['GET'])
def index():
    return "hola mundo"




# crea los endpoint o rutas (json)
@app.route('/users',methods=['GET'])
def get_users():
    all_users=Users.query.all() # el metodo query.all() lo hereda de db.Model
    result=users_schema.dump(all_users)  #el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)     # retorna un JSON de todos los registros de la tabla




@app.route('/users/<id>',methods=['GET'])
def get_user(id):
    user=Users.query.get(id)
    return user_schema.jsonify(user)   # retorna el JSON de un producto recibido como parametro


@app.route('/users/<id>',methods=['DELETE'])
def delete_user(id):
    user=Users.query.get(id)
    db.session.delete(user)
    db.session.commit()                     # confirma el delete
    return user_schema.jsonify(user) # me devuelve un json con el registro eliminado


@app.route('/users', methods=['POST']) # crea ruta o endpoint
def create_user():
    #print(request.json)  # request.json contiene el json que envio el cliente
    name=request.json['name']
    email=request.json['email']
    password=request.json['password']

    #nuevo usuerio con los datos pasados por input del form
    new_user=Users(name,email,password)
    db.session.add(new_user)
    db.session.commit() # confirma el alta
    return user_schema.jsonify(new_user)


@app.route('/user/<id>' ,methods=['PUT'])
def update_user(id):
    user=Users.query.get(id)

    user.name=request.json['name']
    user.email=request.json['email']
    user.password=request.json['password']

    db.session.commit()    # confirma el cambio
    return user_schema.jsonify(user)    # y retorna un json con el producto