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

# Event table defined here
db.define_table(
    'event',
    Field('name', requires=IS_NOT_EMPTY()),
    Field('event_time', 'datetime', default=get_time(), requires=(IS_NOT_EMPTY(), IS_DATETIME())),
    Field('location'),
    Field('description', 'text'),
    Field('all_day', 'boolean', default=False),
    auth.signature,
)
db.define_table(
    'invitations',
    Field('inviter', default=''), # holds username string of invite sender
    Field('recipient', default=''), # holds username string of invite recipient
    Field('event_id', requires=IS_NOT_EMPTY()),
    auth.signature,
)

# Change readable/writable permissions for event table
db.event.id.readable = db.event.id.writable = False
db.event.created_on.readable = db.event.created_on.writable = False
db.event.created_by.readable = db.event.created_by.writable = False
db.event.modified_on.readable =  False
db.event.modified_by.readable = False

db.commit()
