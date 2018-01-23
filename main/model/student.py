from . import db


class Student(db.Model):
    __tablename__ = 'student'
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_subject = db.Column(db.String(128))

    s_u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    s_user = db.relationship('User', back_populates='student')

    s_teacher_id = db.Column(db.Integer)
    s_test_id = db.Column(db.Integer)
    s_class_id = db.Column(db.Integer)

    def __repr__(self):
        return '<id:%r  真实名称:%r>' % (self.id, self.s_real_name)
