# -*- coding: utf-8 -*-
"""
"""
import random
import string
from lxml import html

from loads.case import TestCase

URLS = [
    'site.com',
    'site.com/website-stress-testing/',
    'site.com/disaster-recovery/',
    'site.com/proof-of-concept/',
    'site.com/it-consulting/',
    'site.com/project-environments/',
]

VERIFY_SSL = False

PDF_FORM_URL = 'site.com/test-pdf-download/'


def text_generator(size=60, chars=None, special_chars=None, increase=1):
    """Generates random text.

    :param size: int  length of string
    :param chars: a set of characters to use
    :param special_chars: a set of characters to use for e.g. '.?*'
    :param increase: repeat n- times
    :return: string
    """
    if not chars:
        chars = string.ascii_letters + string.digits
    if special_chars is None:
        special_chars = "\n\t\r"
    available_chars = chars + special_chars
    return ''.join([
        ''.join(random.choice(chars) for _ in range(20)),
        ''.join(random.choice(available_chars) for _ in range(size*increase))
    ])


def generate_from():
    """Generates random email address.

    :return: string
    """
    return ''.join(
        [
            text_generator(size=10, special_chars=''), '@',
            text_generator(size=10, special_chars=''), '.',
            random.choice(['com', 'cc', 'org'])
        ]
    )


class TestWebSite(TestCase):

    def test_es(self):
        for url in URLS:
            resp = self.session.get(url, verify=VERIFY_SSL)
            self.basic_response_check(resp)

        ## Submit form and get PDF file
        user_suffix = text_generator(size=5, special_chars='')
        post_data = {
            'formBuilderForm[FormBuilderID]': 1,
            'formBuilderForm[First_name]': 'test{0}'.format(user_suffix),
            'formBuilderForm[Last_Name]': 'test{0}'.format(user_suffix),
            'formBuilderForm[Email]': generate_from(),
            'formBuilderForm[phone]': '94585454854854',
            'formBuilderForm[City]': 'TestCity',
            'formBuilderForm[Country]': 0,
            'formBuilderForm[Company_Name]': 'TestCompany',
            'formBuilderForm[Job_Title]': 'Test job',
            'formBuilderForm[Explicit_Consent]': 'just a test',
            'formBuilderForm[confirm_something]': 1,
            'formBuilderForm[captcha]': '',
            'REFERER': '',
            'PAGE': 'site.com/test-pdf-download/'
        }
        resp = self.session.post(PDF_FORM_URL, data=post_data,
                                 allow_redirects=True, verify=VERIFY_SSL)

        self.basic_response_check(resp)

        pdf_files = html.fromstring(resp.content).xpath(
            "//a[contains(@href,'.pdf') and contains(@onclick, 'download')]/@href"
        )

        self.assertIsNotNone(pdf_files)
        self.assertGreater(len(pdf_files), 0)
        #  self.assertEqual(len(pdf_files), 1)

        resp = self.session.get(pdf_files[0], verify=VERIFY_SSL)

        self.assertIn('application/pdf', resp.headers.get('Content-Type', ''))

        self.assertEqual(
            int(resp.headers.get('Content-Length')),
            len(resp.content)
        )

    def basic_response_check(self, resp):
        """Check if response is not None and status code is less or equals 399

        :param resp: Requests Response object or None
        :return:
        """
        self.assertIsNotNone(resp, 'Response is Empty')
        self.assertLessEqual(
            resp.status_code,
            399,
            ' {} status code'.format(resp.status_code)
        )

