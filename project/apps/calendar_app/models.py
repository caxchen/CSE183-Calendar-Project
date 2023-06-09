"""
This file defines the database models
"""

import datetime
from py4web.utils.populate import FIRST_NAMES, LAST_NAMES, IUP
from .common import db, Field, auth
from pydal.validators import *

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_username():
    return auth.current_user.get('username') if auth.current_user else None

def get_time():
    return datetime.datetime.now()

# Venue table defined here 
db.define_table(
    'venue',
    Field('venue_name', requires=IS_NOT_EMPTY()),
    Field('contact_info', requires=IS_NOT_EMPTY()),
    Field('address', requires=IS_NOT_EMPTY()),
    Field('city', requires=IS_NOT_EMPTY()),
    Field('state', requires=IS_NOT_EMPTY()),
    Field('zip_code', 'integer', requires=(IS_NOT_EMPTY(),IS_INT_IN_RANGE(0, 1e5))),
    Field('capacity', 'integer', requires=(IS_NOT_EMPTY(),IS_INT_IN_RANGE(0, 1e6))),
    auth.signature
)

# Event table defined here
db.define_table(
    'event',
    #Field('category_id', db.category, requires=IS_IN_DB(db, 'category.id', '%(category_name)s', zero='Select category')),
    Field('venue_id', db.venue, requires=IS_IN_DB(db, 'venue.id', '%(venue_name)s', zero='Select Venue')),
    Field('name', requires=IS_NOT_EMPTY()),
    Field('event_time', 'datetime', default=get_time(), requires=(IS_NOT_EMPTY(), IS_DATETIME())),
    Field('description', 'text'),
    Field('all_day', 'boolean', default=False),
    auth.signature,
)
db.define_table(
    'category',
    Field('category_name', 'text', requires=IS_NOT_EMPTY()),
    Field('color', 'string', required=True),
    auth.signature,
)

# Change readable/writable permissions for category table
db.category.id.readable = db.category.id.writable = False
db.category.created_on.readable = db.category.created_on.writable = False
db.category.created_by.readable = db.category.created_by.writable = False
db.category.modified_on.readable =  False
db.category.modified_by.readable = False

# Change readable/writable permissions for venue table
db.venue.id.readable = db.venue.id.writable = False
db.venue.created_on.readable = db.venue.created_on.writable = False
db.venue.created_by.readable = db.venue.created_by.writable = False
db.venue.modified_on.readable =  False
db.venue.modified_by.readable = False

# Change readable/writable permissions for event table
db.event.venue_id.readable = False
db.event.id.readable = db.event.id.writable = False
db.event.created_on.readable = db.event.created_on.writable = False
db.event.created_by.readable = db.event.created_by.writable = False
db.event.modified_on.readable =  False
db.event.modified_by.readable = False

db.commit()
