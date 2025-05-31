from flask import Blueprint, request, jsonify
from app.models.course import Course
from app import db
from datetime import datetime

admin_bp = Blueprint("admin_api", __name__)

@admin_bp.route("/courses", methods=["POST"])
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
def get_courses():
    try:
        courses = Course.query.all()
        return jsonify([course.to_dict() for course in courses]), 200
    
    except Exception as e:
        return jsonify({"message": f"Erro ao buscar cursos: {str(e)}"}), 500
    
@admin_bp.route("/courses/<int:course_id>", methods=["PUT"])
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