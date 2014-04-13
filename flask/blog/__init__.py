"""
Init Flask application

"""


import markdown

from flask import Flask, render_template, Markup, request, url_for
from werkzeug.exceptions import NotFound
from flask_bootstrap3 import Bootstrap
import os

app = Flask(__name__)

bootstrap = Bootstrap()
bootstrap.init_app(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
MARKDOWN_DIR = os.path.join(APP_ROOT, 'markdown_files')


def run_server():
    """Start application
    """
    app.run(port=8080, debug=True)


def shutdown_server():
    """Shutdown server
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def file_name(file):
    if os.path.isfile(file) and file.endswith('.md'):
        return os.path.basename(file)[:-3]


def available_routes():
    result = []
    for root, dirs, files in os.walk(MARKDOWN_DIR):
        uri_path = os.path.relpath(root, MARKDOWN_DIR)
        #print(uri_path.split('/'))
        if uri_path == '.':
            uri_path = ''
        else:
            result.append(uri_path)
        for file in files:
            name = file_name(os.path.join(root, file))
            if not name:
                continue
            uri = '{path}/{file}'.format(path=uri_path, file=name)
            result.append(uri.strip('/'))
    return result


def folder_index(real_path, uri):
    result = {}
    for item in os.listdir(real_path):
        item_path = os.path.join(real_path, item)
        item_name = item
        item_uri = item_name
        if os.path.isfile(item_path):
            item_name = file_name(item_path)
            item_uri = item_name
        if not item_name:
            continue
        path = "{uri}/{item}".format(uri=uri, item=item_uri)
        result[item_name] = url_for('blog_index', path=path, _external=True)

    return result


def render_markdown_file(file, **kwargs):
    view_data = kwargs
    view_data['content'] = Markup(markdown.markdown(open(file, 'r').read(),
                                                    output_format='html5'))
    return render_template('article.html', **view_data)


@app.context_processor
def utility_processor():
    def format_price(amount, currency=u'€'):
        return u'{0:.2f}{1}'.format(amount, currency)
    return dict(format_price=format_price)


@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.html'), 404


@app.route('/blog/', defaults={'path': 'index'})
@app.route('/blog/<path:path>')
def blog_index(path):
    """Main route for application

    """
    path = path.strip('/')

    breadcrumb = [{'title': 'home', 'uri': 'index'}]
    path_list = path.split('/')
    for key, item in enumerate(path_list):
        item = {
            'title': item,
            'uri': '/'.join(path_list[:key+1])
        }
        breadcrumb.append(item)

    routes = available_routes()
    if path not in routes:
        raise NotFound

    tree_items = []

    real_path = os.path.join(MARKDOWN_DIR, path)
    if os.path.isdir(real_path):
        index_file = os.path.join(real_path, 'index.md')
        if os.path.isfile(index_file):
            return render_markdown_file(index_file, **locals())
        view_data = locals()
        view_data['items'] = folder_index(real_path, path)
        return render_template('folder_index.html', **view_data)

    md_file = os.path.join(MARKDOWN_DIR, path) + ".md"
    if os.path.isfile(md_file):
        return render_markdown_file(md_file, **locals())
    raise NotFound

