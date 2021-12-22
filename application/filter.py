
from . import app_factory
from markdown import markdown


@app_factory.template_filter('md')
def markdown_to_html(txt):
    return markdown(txt)