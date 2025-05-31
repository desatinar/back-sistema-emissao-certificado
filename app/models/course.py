from app import db
from datetime import date

class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    workload = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    course_date = db.Column(db.Date, nullable=False, default=date.today)

    certifacates = db.relationship("Certificate", backref="course", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "workload": self.workload,
            "description": self.description,
            "course_date": self.course_date.isoformat() if self.course_date else None
        }
    
    def __repr__(self):
        return f"<Course {self.name}"