from shutil import which

import pdfkit
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string


class HeadlessPdfKit(pdfkit.PDFKit):
    def command(self, path=None):
        cmdlist = []
        if which('xvfb-run'):
            cmdlist = ['xvfb-run', '--']
            # if `auto_servernum` is in options, add the `-a` parameter which
            # should ensure that each xvfb has its own DISPLAY ID
            if 'auto_servernum' in self.options:
                cmdlist = ['xvfb-run', '-a', '--']
        return cmdlist + super().command(path)

def pdf_from_string(input, output_path, options=None, toc=None, cover=None, css=None,
                configuration=None, cover_first=False):
    """
    Convert given string or strings to PDF document

    :param input: string with a desired text. Could be a raw text or a html file
    :param output_path: path to output PDF file. False means file will be returned as string.
    :param options: (optional) dict with wkhtmltopdf options, with or w/o '--'
    :param toc: (optional) dict with toc-specific wkhtmltopdf options, with or w/o '--'
    :param cover: (optional) string with url/filename with a cover html page
    :param css: (optional) string with path to css file which will be added to a input string
    :param configuration: (optional) instance of pdfkit.configuration.Configuration()
    :param configuration_first: (optional) if True, cover always precedes TOC

    Returns: True on success
    """

    r = HeadlessPdfKit(input, 'string', options=options, toc=toc, cover=cover, css=css,
               configuration=configuration, cover_first=cover_first)

    return r.to_pdf(output_path)

def get_pdf_response(template_name, filename, context, show_content_in_browser, verbose=False):
    html = render_to_string(template_name, context)
    if verbose:
        print('V: Rendered html')
    pdf = pdf_from_string(html, False,
        configuration=settings.PDFKIT_CONFIG, options=settings.WKHTMLTOPDF_CMD_OPTIONS
    )
    if show_content_in_browser:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="{name}"'.format(name=filename)
        return response
    return pdf
