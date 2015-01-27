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
    config.add_route('promo', '/promo/{ref_tag}/{ref_id}')
    config.add_route('upromo', '/promo/{id}')
    config.add_route('suggest', '/sg')

    # set familiar url standart API
    config.add_route('results', '/api/v1/result')
    config.add_route('valid', '/api/v1/valid')
    config.add_route('rest', '/api/v1/rest')

    # set inspeksi data
    config.add_route('testrails', '/api/v1/test_rails')
    config.add_route('results_build', '/api/beta/result')
    config.add_route('valid_build', '/api/beta/valid')
    config.add_route('kensaku_build', '/kensaku-beta')

    config.scan()
    return config.make_wsgi_app()
