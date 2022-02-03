from io import BytesIO
from django.template.loader import get_template
# from sqlparse.filters import output
from xhtml2pdf import pisa
from django.http import HttpResponse
from rest_framework.response import Response
import uuid
from django.conf import settings


def save_pdf(params: dict):
    template = get_template('pdfGenerator/appointment.html')
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = uuid.uuid4()
    try:
        with open(str(settings.BASE_DIR)+f'/media/OfficialDocuments/{file_name}.pdf', 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)

    except Exception as e:
        print(e)

    if pdf.err:
        return '', False
    else:
        return file_name, True


# def html_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None