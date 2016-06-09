# -*- coding: utf-8 -*-
"""
"""
import concurrent.futures
import multiprocessing
import random
import string

import requests

logger = multiprocessing.log_to_stderr(multiprocessing.SUBWARNING)

URLS = ['http://site.com/',
'http://site.com/website-stress-testing/',
'http://site.com/disaster-recovery/',
'http://site.com/proof-of-concept/',
'http://site.com/it-consulting/',
'http://site.com/project-environments/',
        ]

PDF_FORM_URL = 'http://site.com/test-pdf-download/'
HTTP_TIMEOUT = 60
PROCCESS_WORKERS_COUNT = 2040


class Counter(object):
    def __init__(self):
        self.val = multiprocessing.Value('i', 0)

    def increment(self, n=1):
        with self.val.get_lock():
            self.val.value += n

    @property
    def value(self):
        return self.val.value

    def __str__(self):
        return str(self.value)

TOTAL_REQUESTS = Counter()
COMPLETED_REQUESTS = Counter()
DOWNLOADED = Counter()
FORM_SUBMITED_SUCCESSFULLY = Counter()
FORM_SUBMITED_COUNT = Counter()


def text_generator(size=60, chars=None, special_chars=None, increase=1000):
    if not chars:
        chars = string.ascii_letters + string.digits
    if special_chars is None:
        special_chars = "\n\t\r"
    all = chars + special_chars
    return ''.join([
        ''.join(random.choice(chars) for _ in range(20)),
        ''.join(random.choice(all) for _ in range(size*increase))
    ])


def generate_from():
    return ''.join(
        [
            text_generator(size=10, special_chars="", increase=1), '@',
            text_generator(size=10, special_chars="", increase=1), '.',
            random.choice(['com', 'cc', 'org'])
        ]
    )


def download_pdf(HTTP_TIMEOUT):
    user_suffix = text_generator(size=5, special_chars="", increase=1)
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
        'REFERER': '',
        'PAGE': 'http://site.com/test-pdf-download/'
    }

    response = requests.post(PDF_FORM_URL, data=post_data,
                             allow_redirects=True, timeout=HTTP_TIMEOUT,
                             verify=False,)
    if not response:
        raise Exception('Response is empty')

    content_type = response.headers.get('Content-Type', '')
    content_length = response.headers.get('Content-Length') or 0
    status = response.status_code
    content = response.content
    response.close()

    if content_type not in ['application/pdf', 'application/octet-stream']:
        raise Exception('Error submitting form and downloading PDF {0}'.format(status))

    if status > 399:
        raise Exception(
            '{code} response status code'.format(status))

    if not content_length or int(content_length) != len(content):
        raise Exception('Partial pdf content')

    return content


def load_url(url, timeout):
    response = requests.get(url, allow_redirects=True, timeout=timeout,
                             verify=False, )
    if not response:
        raise Exception('Response is empty')
    if response.status_code > 399:
        raise Exception('{code} response status code'.format(response.status_code))
    content = response.content
    response.close()
    return content


def func(_):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_url = {executor.submit(load_url, url, 60): url for url in
                         URLS}
        future_to_url[executor.submit(download_pdf, 60)] = PDF_FORM_URL

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                logger.error('%r generated an exception: %s' % (url, exc))
            else:
                logger.info('%r page is %d bytes' % (url, len(data)))


with concurrent.futures.ProcessPoolExecutor(max_workers=300) as executor:
    executor.map(func, range(1, PROCCESS_WORKERS_COUNT))

"""
TOTAL_REQUESTS = 0
COMPLETED_REQUESTS = 0
DOWNLOADED = 0
FORM_SUBMITED_SUCCESSFULLY = 0
FORM_SUBMITED_COUNT = 0

"""


#print("""
#Total requests: {total}
#completed requests: {completed}
#bytes downloaded: {bytes}
#Amount of form submition: {form_sub}
#Downloaded PDF's : {pdf_count}
#""".format(total=TOTAL_REQUESTS, completed=COMPLETED_REQUESTS,
#      bytes=DOWNLOADED, form_sub=FORM_SUBMITED_COUNT,
#     pdf_count=FORM_SUBMITED_SUCCESSFULLY ))
