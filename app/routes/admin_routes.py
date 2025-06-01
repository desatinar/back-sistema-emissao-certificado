from flask import Blueprint, request, jsonify, session
from functools import wraps
from app.models.course import Course
from app.models.student import Student
from app.models.certificate import Certificate
from app import db
from datetime import datetime
from datetime import date
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint("admin_api", __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session:
            return jsonify({"message": "Acesso não autorizado"})
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/courses", methods=["POST"])
@admin_required
def create_course():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("workload") or not data.get("course_date"):
        return jsonify({"message": "Dados obrigatórios: nome, carga horária, data do curso"}), 400
    
    try:
        course_date_obj = datetime.strptime(data["course_date"], "%Y-%m-%d").date()
        workload_int = int(data["workload"])

        if workload_int <= 0:
            return jsonify({"message": "Carga horária deve ser um número positivo"}), 400
        
        new_course = Course(
            name=data["name"],
            workload=workload_int,
            description=data.get("description"),
            course_date=course_date_obj
        )
        db.session.add(new_course)
        db.session.commit()

        return jsonify(new_course.to_dict()), 201
    
    except ValueError:
        return jsonify({"message": "Formato inválido para carga horária ou data. Data deve ser AAAA-MM-DD"}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao criar curso: {str(e)}"}), 500
    
@admin_bp.route("/courses", methods=["GET"])
@admin_required
def get_courses():
    try:
        courses = Course.query.all()
        return jsonify([course.to_dict() for course in courses]), 200
    
    except Exception as e:
        return jsonify({"message": f"Erro ao buscar cursos: {str(e)}"}), 500
    
@admin_bp.route("/courses/<int:course_id>", methods=["PUT"])
@admin_required
def update_course(course_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Nenhum id foi fornecido"})
    
    try:
        course = Course.query.get(course_id)
        if not course:
            return jsonify({"message": "Curso não encontrado"})
        
        if "name" in data:
            course.name = data["name"]
        if "workload" in data:
            workload_int = int(data["workload"])
            if workload_int <= 0:
                return jsonify({"message": "Carga horária deve ser um número positivo"})
            course.workload = workload_int
        if "description" in data:
            course.description = data["description"]
        if "course_date" in data:
            course.course_date = datetime.strptime(data["course_date"], "%Y-%m-%d").date()
        
        db.session.commit()
        return jsonify(course.to_dict()), 200
    
    except ValueError:
        return jsonify({"message": "Formato inválido para carga horária ou data. Data deve ser AAAA-MM-DD"}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao atualizar curso: {str(e)}"}), 500
    
@admin_bp.route("/courses/<int:course_id>", methods=["DELETE"])
@admin_required
def delete_course(course_id):
    try:
        course = Course.query.get(course_id)
        if not course:
            return jsonify({"message": "Id do curso não encontrado"}), 404
        
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Curso deletado com sucesso!"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao excluir curso {str(e)}"}), 500
    
@admin_bp.route("/students", methods=["POST"])
@admin_required
def create_student():
    data = request.get_json()

    if not data or not data.get("full_name") or not data.get("email") or not data.get("cpf"):
        return jsonify({"message": "Dados obrigatórios: nome completo, email e CPF"}), 400
    
    if len(data["cpf"]) < 11 or len(data["cpf"]) > 14:
        return jsonify({"message": "Formato de CPF inválido"}), 400
    
    try:
        new_student = Student(
            full_name=data["full_name"],
            email=data["email"],
            cpf=data["cpf"]
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify(new_student.to_dict()), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Email ou CPF já cadastrados"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao criar o estudante: {str(e)}"}), 500
    
@admin_bp.route("/students", methods=["GET"])
@admin_required
def get_students():
    try:
        students = Student.query.all()
        return jsonify([student.to_dict() for student in students]), 200
    
    except Exception as e:
        return jsonify({"message": f"Erro ao buscar estudantes: {str(e)}"}), 500
    
@admin_bp.route("/students/<int:student_id>", methods=["PUT"])
@admin_required
def update_student(student_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Nenhum dado foi passado para atualizar"})
    
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"message": "Id do estudante não encontrado"})
        
        if "full_name" in data:
            student.full_name = data["full_name"]
        if "email" in data:
            student.email = data["email"]
        if "cpf" in data:
            if len(data["cpf"]) < 11 or len(data["cpf"]) > 14:
                return jsonify({"message": "Formato de cpf inválido"})
            student.cpf = data["cpf"]

        db.session.commit()
        return jsonify(student.to_dict()), 200
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Email ou CPF já cadastrado por outro estudante"}), 409
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao atualizar estudante: {str(e)}"}), 500

@admin_bp.route("/students/<int:student_id>", methods=["DELETE"])
@admin_required
def delete_student(student_id):
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"message": "Estudante não encontrado"})
        
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": f"Estudante excluído com sucesso!"}), 200
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": f"Erro de integridade ao excluir aluno. Verifique se existem certificados associados ao estudante: {str(e)}"}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao excluir o estudante: {str(e)}"}), 500
    
@admin_bp.route("/certificates/issue", methods=["POST"])
@admin_required
def issue_certificate():
    data = request.get_json()
    student_id = data.get("student_id")
    course_id = data.get("course_id")

    if not student_id or not course_id:
        return jsonify({"message": "ID do aluno e ID do curso são obrigatórios"}), 400
    
    student = Student.query.get(student_id)
    course = Course.query.get(course_id)

    if not student:
        return jsonify({"message": f"Aluno com com id {student_id} não encontrado"}), 400
    if not course:
        return jsonify({"message": f"Curso com ID {course_id} não encontrado"}), 400
    
    existing_certificate = Certificate.query.filter_by(
        student_id=student_id,
        course_id=course_id
    ).first()

    if existing_certificate:
        return jsonify({
            "message": "Certificado já emitido com esse aluno e curso",
            "certificate": existing_certificate.to_dict()
        }), 409
    
    try:
        new_certificate = Certificate(
            student_id=student_id,
            course_id=course_id
        )
        db.session.add(new_certificate)
        db.session.commit()
        return jsonify({
            "message": "Certificado emitido com sucesso!",
            "certificate": new_certificate.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao emitir o certificado {str(e)}"}), 500