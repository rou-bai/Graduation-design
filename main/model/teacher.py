from . import db


class Teacher(db.Model):
    __tablename__ = 'teacher'
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_work_time = db.Column(db.String(128))

    t_u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    t_user = db.relationship('User', back_populates='teacher')

    t_class_id = db.Column(db.Integer)



    def __repr__(self):
        return '<id:%r  工龄:%r>' % (self.id, self.t_work_time)
