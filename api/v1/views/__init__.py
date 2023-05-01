#!/usr/bin/python3

"""__init__ file """

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
<<<<<<< HEAD
# from api.v1.views.states import *
# from api.v1.views.cities import *
from api.v1.views.amenities import *
=======
from api.v1.views.states import *
from api.v1.views.cities import *
"""from api.v1.views.users import *"""
"""from api.v1.views.amenities import *"""
"""from api.v1.views.places import *"""
"""from api.v1.views.places_reviews import *"""
>>>>>>> 0a444cab496a674811f07aa0b89011b74206f6fd
