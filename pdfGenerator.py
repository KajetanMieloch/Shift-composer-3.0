from reportlab.pdfgen import canvas



def generate_pdf(data_for_pdf, id_name_surname):

    print(data_for_pdf)

    departments = []
    for d in data_for_pdf:
        if d["department"] not in departments:
            departments.append(d["department"])
    
    dates = []
    for d in data_for_pdf:
        if d["working_hours"] not in dates:
            dates.append(d["working_hours"][0])

    ids = []
    for d in data_for_pdf:
        if d["employee_id"] not in ids:
            ids.append(d["employee_id"])
            print(id_name_surname[d["employee_id"]])

    print(departments)
    print(dates)

    pdf_file = "output.pdf"  # Specify the path and filename for the PDF file
    c = canvas.Canvas(pdf_file)
    
    
    c.save()
    
    print("PDF generated successfully")
