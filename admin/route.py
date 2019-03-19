from .common.utils import Resource
from .resources.login import Login, Logout
from .resources.staff import Staff, StaffRole

routes = (
    Resource(Login, '/login', endpoint='login'),
    Resource(Logout, '/logout', endpoint='logout'),
    Resource(Staff, '/staff', endpoint='staff'),
    Resource(StaffRole, '/staff/role', endpoint='staff_role')
)
