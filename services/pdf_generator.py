# services/pdf_generator.py
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
import os
from models.share_issuance import ShareIssuance
from models.shareholder import Shareholder


def generate_certificate_pdf(issuance: ShareIssuance, shareholder_name: str) -> bytes:

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('certificate.html')

    html_out = template.render(
        name=shareholder_name,
        shares=issuance.number_of_shares,
        price=issuance.price,
        date=issuance.issued_date.strftime("%B %d, %Y"),
        certificate_id=issuance.id,
        company_name="Corporate OS Inc."
    )

    html = HTML(string=html_out)
    return html.write_pdf()