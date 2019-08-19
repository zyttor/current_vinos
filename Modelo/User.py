from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):

    def __init__ (self, id_clave, usuario, clave):
        self.id = id_clave
        self.usuario = usuario
        self.clave = clave


