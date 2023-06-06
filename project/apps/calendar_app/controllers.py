"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL, HTTP
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from py4web.utils.form import Form, FormStyleBulma

@action("index")
@action.uses("index.html", auth.user, T)
def index():
    user = auth.get_user()
    message = T("{first_name}'s Calendar".format(**user) if user else "Hello")
    actions = {"allowed_actions": auth.param.allowed_actions}
    return dict(message=message, actions=actions)

@action("create_event", method=["GET", "POST"])
@action.uses("create_event.html", db, session, auth.user)
def create_event():
    form = Form(db.event, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

@action('edit_event/<id:int>', method=["GET", "POST"])
@action.uses('edit_event.html', db, session, auth.user)
def edit_event(id=None):
    assert id is not None
    edit_event = db.event[id]
    if edit_event is None:
        redirect(URL('index'))
    form = Form(db.event, record=edit_event, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

@action('view_event/<id:int>', method=["GET", "POST"])
@action.uses('view_event.html', db, session, auth.user)
def view_event(id=None):
    assert id is not None
    edit_event = db.event[id]
    if edit_event is None:
        redirect(URL('index'))
    rows = db(db.event.id == id).select()
    return dict(events=rows)

@action('delete_event/<id:int>')
@action.uses(db, session, auth.user)
def delete_event(id=None):
    assert id is not None
    event_id = db.event[id]
    if event_id is None:
        redirect(URL('index'))
    db(db.event.id == id).delete()
    redirect(URL('index'))

# made this to get events to put into the fullCalendar
@action("get_events", method=["GET"])
@action.uses(db, session, auth.user)
def get_events():
    username = auth.get_user()['id']
    events = db(db.event.created_by == username).select()
    return dict(events=events)