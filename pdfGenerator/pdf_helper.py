from io import BytesIO
from django.template.loader import get_template
# from sqlparse.filters import output
from xhtml2pdf import pisa
import uuid
from django.conf import settings


def save_pdf(params: dict):
    template = get_template('pdfGenerator/appointment.html')
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = uuid.uuid4()
    try:
        with open(str(settings.BASE_DIR) + f'/media/OfficialDocuments/{file_name}.pdf', 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)

    except Exception as e:
        print(e)

    if pdf.err:
        return '', False
    else:
        return file_name, True