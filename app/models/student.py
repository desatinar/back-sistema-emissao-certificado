from app import db

class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)

    certificates = db.relationship("Certificate", backref="student", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "cpf": self.cpf
        }
    
    def __repr__(self):
        return f"<Student {self.full_name}"