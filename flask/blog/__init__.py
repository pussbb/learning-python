"""
Init Flask application

"""

from urllib.parse import urlparse
import os


import markdown
from markdown.inlinepatterns import LinkPattern, LINK_RE


from flask import Flask, render_template, Markup, request, url_for
from werkzeug.exceptions import NotFound
from flask_bootstrap3 import Bootstrap


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
    def tree_item(name=None, route=None):
        return {'name': name, 'route': route, 'items': {}}

    root_item = tree_item('/', '/')
    for root, dirs, files in os.walk(MARKDOWN_DIR):
        uri_path = os.path.relpath(root, MARKDOWN_DIR)
        item = root_item
        if uri_path == '.':
            uri_path = ''
        else:
            for i in uri_path.split('/'):
                item = item['items'].get(i)
            result.append(uri_path)

        for dir in dirs:
            dir_item = tree_item(dir,
                                 "{0}/{1}".format(uri_path, dir).strip('/'))
            item['items'][dir] = dir_item

        for file in files:
            name = file_name(os.path.join(root, file))
            if not name :
                continue

            uri = '{path}/{file}'.format(path=uri_path, file=name).strip('/')
            if name != 'index' :
                file_item = tree_item(name, uri)
                item['items'][name] = file_item
            result.append(uri)

    return result, root_item


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


class CheckLinkPattern(LinkPattern):


    def __init__(self, pattern, markdown_instance=None, requested_path=None):
        super().__init__(pattern, markdown_instance)
        self.requested_path = requested_path.split('/')


    def handleMatch(self, m):
        node = LinkPattern.handleMatch(self, m)
        # check 'src' to ensure it is local
        src = node.attrib.get('href')
        scheme, netloc, path, params, query, fragment = urlparse(src)
        if scheme or netloc:
            return node

        if path.endswith('.md'):
            path = path[:-3]
        path_parts = path.split('/')
        if path_parts[-1] == 'index':
            path_parts = path_parts[:-1]
        current_path = self.requested_path[:]
        for path_part in path_parts:
            if path_part == '.' or path_part == '..':
                path_parts = path_parts[1:]
                current_path = current_path[:-1]

        url = url_for('blog_index', path='/'.join(current_path + path_parts),
                      _external=True, _anchor=fragment)
        node.set('href', url)
        return node



def render_markdown_file(file, **kwargs):
    view_data = kwargs
    md = markdown.Markdown(output_format='html5')
    md.inlinePatterns['link'] = CheckLinkPattern(LINK_RE, md,
                                                 view_data.get('requested_path'))
    view_data['content'] = Markup(md.convert(open(file, 'r').read()))
    return render_template('article.html', **view_data)


@app.context_processor
def utility_processor():
    def format_price(amount, currency=u'€'):
        return u'{0:.2f}{1}'.format(amount, currency)

    return dict(format_price=format_price)


@app.template_filter('prettify_file_name')
def prettify_file_name(name):
    return name.replace('_', ' ').capitalize()


@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.html'), 404


@app.route('/blog/', defaults={'path': 'index'})
@app.route('/blog/<path:path>')
def blog_index(path):
    """Main route for application

    """
    requested_path = path.strip('/')

    breadcrumb = [{'title': 'home', 'uri': 'index'}]
    path_list = requested_path.split('/')
    for key, item in enumerate(path_list):
        item = {
            'title': item,
            'uri': '/'.join(path_list[:key+1])
        }
        breadcrumb.append(item)

    routes, route_tree = available_routes()

    if requested_path not in routes:
        raise NotFound

    real_path = os.path.join(MARKDOWN_DIR, requested_path)
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

