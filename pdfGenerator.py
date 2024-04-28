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

    for department in departments:
        x = 1920
        y = 1080
        c = canvas.Canvas(f"{department}.pdf", pagesize=(1920, 1080 ))
        c.setFont("Helvetica-Bold", 48)
        c.drawCentredString(x/2, 1000, f"Department: {department}")

        # Table headers
        header_x = 100
        header_y = 900
        cell_width = 100
        cell_height = 50


        # Draw dates headers
        for i, date in enumerate(dates):
            c.setFont("Helvetica-Bold", 24)
            c.saveState()
            c.translate(header_x + (i * cell_width), header_y)
            c.rotate(45)
            c.drawString(150, -150, date)
            c.restoreState()

        # Draw ids headers
        for i, employee_id in enumerate(ids):
            c.setFont("Helvetica-Bold", 24)
            c.drawString(header_x, header_y - ((i + 1) * cell_height), id_name_surname[employee_id])

        # Draw table cells
        cell_x = header_x + cell_width + 50
        cell_y = header_y - cell_height
        for i, employee_id in enumerate(ids):
            for j, date in enumerate(dates):
                c.setFont("Helvetica", 24)
                c.setFillColorRGB(0.8, 0.8, 0.8)  # Set cell color
                c.rect(cell_x + (j * cell_width), cell_y - (i * cell_height), cell_width, cell_height, fill=True, stroke=False)  # Draw cell
                c.setFillColorRGB(0, 0, 0)  # Reset fill color
                c.drawString(cell_x + (j * cell_width) + 10, cell_y - (i * cell_height) + 10, "Cell")  # Add text with padding
                c.setStrokeColorRGB(0, 0, 0)  # Set line color
                c.rect(cell_x + (j * cell_width), cell_y - (i * cell_height), cell_width, cell_height, fill=False, stroke=True)  # Draw cell border


        c.save()
    
    print("PDF generated successfully")
