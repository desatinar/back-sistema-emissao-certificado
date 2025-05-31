from app import db
from datetime import date
import uuid

class Certificate(db.Model):
    __tablename__ = "certificate"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)

    issue_date = db.Column(db.Date, nullable=False, default=date.today)
    unique_validation_code = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "issue_date": self.issue_date,
            "unique_validation_code": self.unique_validation_code
        }
    
    def __repr__(self):
        return f"<Certificate {self.unique_validation_code}"