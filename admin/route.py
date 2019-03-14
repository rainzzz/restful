from .resources.login import Login
from .common.utils import Resource

routes = (
    Resource(Login, '/login', endpoint='login'),
)
