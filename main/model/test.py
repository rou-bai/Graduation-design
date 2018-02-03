from . import db


class Test(db.Model):
    __tablename__ = 'test'
    __table_args__ = {
        'extend_existing': True,
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_subject = db.Column(db.String(128))
    test_time = db.Column(db.Date)
    sign_start_time = db.Column(db.Date)
    sign_end_time = db.Column(db.Date)

    # test_student = db.relationship('Student', backref='ss_test')

    def __repr__(self):
        return '<报名科目:%r  考试时间:%r>' % (self.test_subject, self.test_time)
