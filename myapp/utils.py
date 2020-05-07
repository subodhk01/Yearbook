import pdfkit
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string


def get_pdf_response(template_name, filename, context, show_content_in_browser):
    html = render_to_string(template_name, context)
    if show_content_in_browser:
        pdf = pdfkit.from_string(html, False,
        configuration=settings.PDFKIT_CONFIG, options=settings.WKHTMLTOPDF_CMD_OPTIONS,
        )
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="{name}"'.format(name=filename)
        return response
    else:
        pdf = pdfkit.from_string(html, False,
            configuration=settings.PDFKIT_CONFIG, options=settings.WKHTMLTOPDF_CMD_OPTIONS
        )
        return pdf
