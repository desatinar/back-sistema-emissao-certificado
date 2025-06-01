from fpdf import FPDF
from datetime import date

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

def generate_certificate_pdf_fpdf2(
    student_name,
    course_name,
    course_workload,
    issue_date_obj,
    validation_code,
    student_cpf=None,
    course_date_obj=None,
    institution_name_header="FACULDADE DE CIÊNCIAS HUMANAS ESUDA",
    certificate_title="CERTIFICADO",
    body_line1="Certificamos que",
    city_issue="Recife",
    validation_url=None
):
    color_border = (42, 59, 71)
    color_header_text = (42, 59, 71)
    color_body_text = (51, 51, 51)
    color_student_name = (74, 144, 226) 
    color_footer_text = (123, 138, 139)

    pdf = PDF(orientation='P', unit='mm', format='A5')
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)

    page_w = 148
    page_h = 210
    margin = 15
    
    border_offset = 5 
    border_x = margin - border_offset
    border_y = margin - border_offset
    border_w = page_w - 2 * border_x
    border_h = page_h - 2 * border_y

    pdf.set_line_width(1)
    pdf.set_draw_color(*color_border)
    pdf.rect(border_x, border_y, border_w, border_h)

    content_x = margin
    content_w = page_w - (2 * margin)
    
    y_current = margin + 5

    pdf.set_xy(content_x, y_current)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*color_header_text)
    pdf.multi_cell(content_w, 7, institution_name_header.upper(), 0, 'C')
    y_current = pdf.get_y() + 15

    pdf.set_xy(content_x, y_current)
    pdf.set_font('Helvetica', 'B', 26)
    pdf.multi_cell(content_w, 11, certificate_title.upper(), 0, 'C')
    y_current = pdf.get_y() + 15

    font_size_p = 11
    line_height_multiplier = 1.6
    line_h_p = font_size_p * 0.352778 * line_height_multiplier

    pdf.set_font('Times', '', font_size_p)
    pdf.set_text_color(*color_body_text)
    
    body_margin_additional = 10
    body_actual_margin = margin + body_margin_additional
    
    pdf.set_left_margin(body_actual_margin)
    pdf.set_right_margin(body_actual_margin)
    pdf.set_x(body_actual_margin)
    
    current_body_w = page_w - (2 * body_actual_margin)

    pdf.write(line_h_p, f"{body_line1} ")

    pdf.set_font('Times', 'B', font_size_p)
    pdf.set_text_color(*color_student_name)
    pdf.write(line_h_p, f"{student_name}")
    pdf.set_font('Times', '', font_size_p)
    pdf.set_text_color(*color_body_text)

    if student_cpf:
        pdf.write(line_h_p, f", portador(a) do CPF nº {student_cpf},")
    
    pdf.write(line_h_p, " participou na qualidade de Aluno(a) do curso de extensão universitária ")

    pdf.set_font('Times', 'B', font_size_p)
    pdf.write(line_h_p, f"\"{course_name}\"")
    pdf.set_font('Times', '', font_size_p)
    
    final_text_part = ", "
    if course_date_obj:
        meses = {1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril", 5: "maio", 6: "junho", 7: "julho", 8: "agosto", 9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"}
        formatted_course_date = f"{course_date_obj.day} de {meses[course_date_obj.month]} de {course_date_obj.year}"
        final_text_part += f"realizado em {formatted_course_date}, "
    
    final_text_part += "com carga horária de "
    pdf.write(line_h_p, final_text_part)
    pdf.set_font('Times', 'B', font_size_p)
    pdf.write(line_h_p, f"{course_workload} horas")
    pdf.set_font('Times', '', font_size_p)
    pdf.write(line_h_p, ".")
    pdf.ln(line_h_p * 2)
    y_current = pdf.get_y()

    pdf.set_left_margin(margin)
    pdf.set_right_margin(margin)
    pdf.set_font('Times', '', font_size_p)
    meses_emissao = {1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril", 5: "maio", 6: "junho", 7: "julho", 8: "agosto", 9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"}
    formatted_issue_date_body = f"{issue_date_obj.day} de {meses_emissao[issue_date_obj.month]} de {issue_date_obj.year}"
    
    date_issue_text = f"{city_issue}, {formatted_issue_date_body}."
    text_width_date = pdf.get_string_width(date_issue_text)
    
    pdf.set_x(page_w - margin - text_width_date) 
    pdf.multi_cell(text_width_date, line_h_p, date_issue_text, 0, 'R')
    y_current = pdf.get_y() + 10

    line_y_pos = y_current
    max_line_y_pos = page_h - margin - 20 
    if line_y_pos > max_line_y_pos:
        line_y_pos = max_line_y_pos
    
    pdf.set_draw_color(180, 180, 180)
    pdf.set_line_width(0.2)

    pdf.line(content_x + content_w * 0.15, line_y_pos, content_x + content_w * 0.85, line_y_pos)
    y_current = line_y_pos + 5

    pdf.set_font('Helvetica', '', 7)
    pdf.set_text_color(*color_footer_text)
    
    validation_text_line1 = f"Código de Autenticidade: {validation_code}"
    
    pdf.set_xy(content_x, y_current)
    pdf.multi_cell(content_w, 4, validation_text_line1, 0, 'L')
    y_current = pdf.get_y()
    
    if validation_url:
        pdf.set_x(content_x) 
        pdf.set_font('Helvetica', 'U', 7)
        pdf.set_text_color(0,0,238) 
        pdf.multi_cell(content_w, 4, validation_url, 0, 'L', link=validation_url)

    return pdf.output(dest='S')