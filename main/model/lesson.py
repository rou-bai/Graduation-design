from . import db


class Class(db.Model):
    __tablename__ = 'class'
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_time = db.Column(db.DateTime)
    class_number = db.Column(db.Integer)
    class_am = db.Column(db.String(64))
    class_pm = db.Column(db.String(64))


    def __repr__(self):
        return '<上课人数:%r >' % (self.class_number)
