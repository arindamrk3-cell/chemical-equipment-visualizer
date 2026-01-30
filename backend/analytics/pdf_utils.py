from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_report(dataset):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 50

    summary = dataset.summary

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Chemical Equipment Report")

    y -= 40
    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"File Name: {dataset.file_name}")

    y -= 20
    p.drawString(50, y, f"Uploaded At: {dataset.uploaded_at}")

    y -= 30
    p.drawString(50, y, f"Total Equipment: {summary['total_equipment']}")

    y -= 20
    p.drawString(50, y, f"Average Flowrate: {summary['avg_flowrate']:.2f}")
    y -= 20
    p.drawString(50, y, f"Average Pressure: {summary['avg_pressure']:.2f}")
    y -= 20
    p.drawString(50, y, f"Average Temperature: {summary['avg_temperature']:.2f}")

    y -= 30
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Equipment Type Distribution:")

    p.setFont("Helvetica", 11)
    for key, value in summary["equipment_type_distribution"].items():
        y -= 18
        p.drawString(70, y, f"{key}: {value}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
