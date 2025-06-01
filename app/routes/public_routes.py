from flask import Blueprint, jsonify, send_file, abort
from app.models.certificate import Certificate
from app.models.student import Student
from app.models.course import Course
from app.services.pdf_service import generate_certificate_pdf_fpdf2
from app import db
import io

public_bp = Blueprint("public_api", __name__)

@public_bp.route("/certificates/download/<code>", methods=["GET"])
def download_certificate_pdf(code):
    certificate = Certificate.query.filter_by(unique_validation_code=code).first()

    if not certificate:
        return jsonify({"message": "Certificado não encontrado"})
    
    student = Student.query.get(certificate.student_id)
    course = Course.query.get(certificate.course_id)

    if not student or not course:
        return jsonify({"message": "Dados do aluno ou curso não encontrados"}), 500
    
    try:
        pdf_bytes = generate_certificate_pdf_fpdf2(
        student_name=student.full_name,
        student_cpf=student.cpf,
        course_name=course.name,
        course_workload=course.workload,
        course_date_obj=course.course_date,
        issue_date_obj=certificate.issue_date,
        validation_code=certificate.unique_validation_code,
        institution_name_header="FACULDADE DE CIÊNCIAS HUMANAS ESUDA",
        certificate_title="CERTIFICADO",
        city_issue="Recife"
    )

        safe_student_name = "".join(c if c.isalnum() else "_" for c in student.full_name)
        safe_course_name = "".join(c if c.isalnum() else "_" for c in course.name)
        filename = f"certificado_{safe_student_name}_{safe_course_name}.pdf"

        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({"message": f"Erro ao gerar PDF do certificado: {str(e)}"}), 500

