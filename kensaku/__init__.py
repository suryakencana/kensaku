import json
from bson import json_util
from pyramid.config import Configurator


class MongoJSONRenderer:
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        request = system.get('request')
        if request is not None:
            if not hasattr(request, 'response_content_type'):
                request.response_content_type = 'application/json'
        return json.dumps(value, default=json_util.default)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.include('.db')
    config.add_renderer('json', MongoJSONRenderer)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('kensaku', '/kensaku')
    config.add_route('results', '/results')
    config.add_route('promo', '/promo/{ref_tag}/{ref_id}')
    config.add_route('upromo', '/promo/{id}')
    config.add_route('suggest', '/sg')
    config.add_route('valid', '/v')
    config.scan()
    return config.make_wsgi_app()
