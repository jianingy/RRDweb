setting = dict()


def load(yaml):
    from yaml import load as yaml_load
    import codecs

    global setting
    with codecs.open(yaml, "r", encoding="utf-8") as f:
        setting = yaml_load(f.read())

    from rrdweb.render import init as init_render_engine
    init_render_engine()

    return setting
