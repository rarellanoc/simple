from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask import jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from app import db

import json, sqlalchemy
from collections import OrderedDict

from werkzeug.security import generate_password_hash, check_password_hash


# Helper method sqlalchemy object to dictionary
#
def model_to_dict(obj):
    dict = {}
    for c in obj.__table__.columns:
        if isinstance(c.type, sqlalchemy.DateTime):
            value = getattr(obj, c.name).strftime("%Y-%m-%d %H:%M:%S")
        elif c.name == "pw_hash":
            value= ""
        else:
            value = getattr(obj, c.name)
        dict[c.name] = value
    return dict

#
# Helper json data to sqlachemy object

def json_to_model(obj, json):
    if json != None:
        for c in json:
            if c == "password":
                obj.set_password(json[c])
            setattr(obj, c, json[c])
            
    



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    email = db.Column(db.String(30))
    pw_hash = db.Column(db.String(300), unique=True)
    tipo_usuario = db.Column(db.String(30))
    estado = db.Column(db.String(30))
    ulimo_login = db.Column(db.String(300))
    created = db.Column(db.DateTime, default=db.func.now())
    disenadoress = db.relationship('Disenador', backref='user',lazy='dynamic')
    empresas = db.relationship('Empresa', backref='user',lazy='dynamic')
    solicitudes = db.relationship('Solicitud', backref='user',lazy='dynamic')
    tokens = db.relationship('Token', backref='user',lazy='dynamic')
    

    def __init__(self, email=None,password=None,tipo_usuario=None, estado='no-confirmado', ultimo_login=None, json=None):
        self.email = email
        
        self.tipo_usuario = tipo_usuario
        self.estado = estado
        self.ulimo_login = ultimo_login
        
        if password != None: 
            self.set_password(password)
        
        json_to_model(self, json)
	

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
	
	
#    def __repr__(self):
#        return '<User %r>' % self.id
	
    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)
	
	def __repr__(self):
		return 'id = {}, email = {}, tipo = {}, estado = {}, utltimo_login = {}, created = {}'.format(self.id, self.email, self.tipo_usuario, self.estado, self.ultimo_login, self.created)

    def to_dict(self):
        return model_to_dict(self)
	

    
    
class Disenador(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    nombre_dis = db.Column(db.String(100))
    nombre_empresa_dis = db.Column(db.String(100))
    nro_disenos = db.Column(db.Integer)
    nro_solicitudes_env = db.Column(db.Integer)
    ciudad = db.Column(db.String(100))
    proyectos = db.relationship('Proyecto', backref='disenador',lazy='dynamic')
    
    
    
    def __init__(self, id_user, nombre_dis, nombre_empresa_dis, nro_disenos, nro_solicitudes_env, ciudad):
        self.id_user = id_user
        self.nombre_dis = nombre_dis
        self.nombre_empresa_dis = nombre_empresa_dis
        self.nro_disenos = nro_disenos
        self.nro_solicitudes_env = nro_solicitudes_env
        self.ciudad = ciudad
        
        
        
        
class Proyecto(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    nombre_proyecto= db.Column(db.String(100))
    tipo_proyecto= db.Column(db.String(100))
    fecha_inicio = db.Column(db.String(100))
    id_disenadores = db.Column(db.Integer)
    id_empresa = db.Column(db.Integer)
    id_disenador = db.Column(db.Integer, db.ForeignKey('disenador.id'))
    licitaciones_proy = db.relationship('Licitacion', backref='proyecto',lazy='dynamic')
    
    def __init__(self, nombre_proyecto, tipo_proyecto, fecha_inicio , id_disenador):
        self.nombre_proyecto = nombre_proyecto
        self.tipo_proyecto = tipo_proyecto
        self.fecha_inicio = fecha_inicio 
        self.id_disenador = id_disenador
                        
        
        
    
    
    
class Licitacion(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    estado_lic = db.Column(db.String(100))
    etapa_nro = db.Column(db.Integer)
    monto = db.Column(db.Integer)
    responsable = db.Column(db.String(100))
    fecha_tope = db.Column(db.String(100))
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id'))
    
    def __init__(self, id_licitacion, estado_lic, etapa_nro, monto, responsable, fecha_tope, id_empresa, id_proyecto):
        self.estado_lic = estado_lic
        self.etapa_nro = etapa_nro
        self.monto = monto
        self.responsalbe = responsalbe
        self.fecha_tope = fecha_tope
        self.id_empresa = id_empresa
        self.id_proyecto = id_proyecto
                        

class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    remitente_id = db.Column(db.String(100))
    destinatario_id = db.Column(db.String(100))
    asunto = db.Column(db.String(100))
    cuerpo = db.Column(db.String(1000))
    fecha = db.Column(db.String(100))
    proyecto = db.Column(db.String(100))
  
                        
    def __init__(self, remitente_id, destinatario_id, asunto, cuerpo, fecha, proyecto):
	self.remitente_id = remitente_id
	self.destinatario_id = destinatario_id
	self.asunto = asunto
	self.cuerpo = cuerpo
	self.fecha = fecha
	self_proyecto = proyecto
		
		
                      

        
        
class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    nombre_empresa = db.Column(db.String(100))
    direccion_empresa = db.Column(db.String(300))
    telefono_empresa = db.Column(db.String(100))
    nro_proyectos_adj = db.Column(db.Integer)
    nro_solicitudes_rec  = db.Column(db.Integer)
    nontos_historicos = db.Column(db.Integer)
    montos_pendientes = db.Column(db.Integer)
    licitaciones = db.relationship('Licitacion', backref='empresa',lazy='dynamic')

    def __init__(self, id_user, nombre_empresa, direccion_empresa, felefono_empresa, nro_proyectos_adj, nro_solicitudes_rec, montos_historicos, montos_pendientes):
	self.id_user = id_user
	self.nombre_empresa = nombre_empresa
	self.direccion_empresa = direccion_empresa
	self.telefono_empresa = telefono_empresa
	self.nro_proyectos_adj = nro_proyecto_adj
	self.nro_solicitudes_rec = nro_solicitudes_rec
	self.montos_historicos = montos_historicos
	self.montos_pendientes = montos_pendientes
    
    
class Solicitud(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    fecha = db.Column(db.DateTime, default=db.func.now())
    activa = db.Column(db.String(20))
    vista = db.Column(db.String(20))
    titulo = db.Column(db.String(100))
    cuerpo = db.Column(db.String(500))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
                        
    def __init__(self, activa='si', vista='no', titulo = None, cuerpo=None, id_user=None):
        self.activa = activa
        self.vista = vista
        self.titulo = titulo
        self.cuerpo = cuerpo
        self.id_user = id_user
		
        
class Token(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    token = db.Column(db.String(20))
    disponible = db.Column(db.String(20))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, token=None, disponible='si', id_user=None):
        
        self.token=token
        self.disponible = disponible
        self.id_user = id_user
        
    
    
    


    
    
						
		
		

						
    
    
    
    
    
    
    

