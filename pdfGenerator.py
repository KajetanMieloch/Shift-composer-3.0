from reportlab.pdfgen import canvas

def generate_pdf(data_for_pdf, id_name_surname):

    # print(data_for_pdf)
    # print(id_name_surname)

    # Extract unique departments, dates, and employee IDs
    departments = set(d["department"] for d in data_for_pdf)
    dates = set(d["working_hours"][0] for d in data_for_pdf)
    ids = set(d["employee_id"] for d in data_for_pdf)

    # Create a dictionary to store work hours for each employee on each date
    work_hours = {date: {emp_id: "-" for emp_id in ids} for date in dates}
    for d in data_for_pdf:
        work_hours[d["working_hours"][0]][d["employee_id"]] = f"{d['working_hours'][1]} - {d['working_hours'][2]}"

    for department in departments:
        x = 1920
        y = 1080
        c = canvas.Canvas(f"{department}.pdf", pagesize=(1920, 1080))
        c.setFont("Helvetica-Bold", 48)
        c.drawCentredString(x/2, 1000, f"Department: {department}")

        # Table headers
        header_x = 100
        header_y = 900
        cell_width = 150
        cell_height = 50

        # Draw dates headers
        for i, date in enumerate(sorted(dates)):
            c.setFont("Helvetica-Bold", 24)
            c.saveState()
            c.translate(header_x + (i * cell_width), header_y)
            c.rotate(45)
            c.drawString(180, -180, date)
            c.restoreState()

        # Draw ids headers
        for i, employee_id in enumerate(ids):
            c.setFont("Helvetica-Bold", 24)
            c.drawString(header_x, header_y - ((i + 1) * cell_height), id_name_surname[employee_id])

        # Draw table cells
        cell_x = header_x + cell_width + 50
        cell_y = header_y - cell_height
        for i, employee_id in enumerate(ids):
            for j, date in enumerate(sorted(dates)):
                c.setFont("Helvetica", 24)
                c.setFillColorRGB(0.8, 0.8, 0.8)  # Set cell color
                c.rect(cell_x + (j * cell_width), cell_y - (i * cell_height), cell_width, cell_height, fill=True, stroke=False)  # Draw cell
                c.setFillColorRGB(0, 0, 0)  # Reset fill color
                c.drawString(cell_x + (j * cell_width) + 10, cell_y - (i * cell_height) + 10, work_hours[date][employee_id])
                c.setStrokeColorRGB(0, 0, 0)  # Set line color
                c.rect(cell_x + (j * cell_width), cell_y - (i * cell_height), cell_width, cell_height, fill=False, stroke=True)  # Draw cell border

        c.save()

