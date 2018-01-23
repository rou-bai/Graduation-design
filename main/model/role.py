from . import db
from flask_security import RoleMixin

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<角色:%r  权限:%r>' % (self.name, self.description)