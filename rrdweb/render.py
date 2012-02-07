from mako.lookup import TemplateLookup
from twisted.python import log
from logging import DEBUG as LVL_DEBUG
import os

__all__ = ["render_html"]

html_lookup = None


def init():
    from rrdweb.setting import setting

    global html_lookup
    html_lookup = TemplateLookup(
        directories=[os.path.join(os.getcwd(), setting["html_tpl"])],
        input_encoding='utf-8',
        output_encoding='utf-8')


def render_html(name, context):
    log.msg("render_html: %s with context `%s`" % (name, context),
            level=LVL_DEBUG)
    t = html_lookup.get_template("%s.mako" % name)
    return t.render(**context)
