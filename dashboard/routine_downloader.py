import io
from datetime import date

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))


def downloader(exams, routine):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Vera', 8)

    today = str(date.today())

    can.drawString(465, 675, today)  # done

    can.drawString(105, 629, routine.department.name)  # done

    can.drawString(127, 614, "B.Sc.")  # done

    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)

    # file name
    sample_name = f"Sample/Routine/Routine {len(exams)}.pdf"

    # read your existing PDF
    existing_pdf = PdfFileReader(open(sample_name, "rb"))
    output = PdfFileWriter()

    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # finally, write "output" to a real file
    outputStream = open("Sample/output.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
