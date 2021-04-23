
import environ
import datetime
import os
import time
from io import BytesIO

from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


env = environ.Env()


class PdfGenerator:
    def __init__(self, data, pdf_template_path):
        self.data = data
        self.template_path = pdf_template_path

    @staticmethod
    def fetch_pdf_resources(uri, rel):
        """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
        result = finders.find(uri)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path

    def generate(self):
        """
        Generates pdf using context from self.data and template from self.template_path.
        Saves pdf in the directory from env. Env variable "PATH_GENERATED_PDF".
        Generates file name using current date and time.
        """
        context = {'info': self.data}
        template = get_template(self.template_path)

        html = template.render(context)

        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), dest=response, link_callback=self.fetch_pdf_resources)

        if pdf.err:
            raise Exception("We had some errors rendering PDF document <pre>" + html + "</pre>")
        else:
            return response.getvalue()
