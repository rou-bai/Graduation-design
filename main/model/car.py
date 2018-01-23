from . import db


class Car(db.Model):
    __tablename__ = 'car'
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_number = db.Column(db.Integer)
    car_type = db.Column(db.String(64))

    car_teacher_id = db.Column(db.Integer)


    def __repr__(self):
        return '<上课人数:%r >' % (self.class_number)