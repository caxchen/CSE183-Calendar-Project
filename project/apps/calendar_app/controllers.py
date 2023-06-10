
from py4web import action, request, abort, redirect, URL, HTTP
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from py4web.utils.form import Form, FormStyleBulma

@action("index")
@action.uses("index.html", db, auth.user, T)
def index():
    user = auth.get_user()
    message = T("{first_name}'s Calendar".format(**user) if user else "Hello")
    actions = {"allowed_actions": auth.param.allowed_actions}
    invite_count = len(db(db.invitations.recipient == auth.current_user.get('username')).select())
    return dict(message=message, actions=actions, invite_count=invite_count)

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
    event = db.event[id]
    if event.created_by != auth.user_id: raise HTTP(400)
    if event is None:
        redirect(URL('index'))
    form = Form(db.event, record=event, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('view_event', id))
    return dict(form=form)

@action('view_event/<id:int>', method=["GET", "POST"])
@action.uses('view_event.html', db, session, auth.user)
def view_event(id=None):
    assert id is not None
    event = db.event[id]
    if event.created_by != auth.user_id: raise HTTP(400)
    if event is None:
        redirect(URL('index'))
    rows = db(db.event.id == id).select()
    return dict(events=rows)

@action('delete_event/<id:int>')
@action.uses(db, session, auth.user)
def delete_event(id=None):
    assert id is not None
    event = db.event[id]
    if event.created_by != auth.user_id: raise HTTP(400)
    if event is None:
        redirect(URL('index'))
    db(db.event.id == id).delete()
    redirect(URL('index'))

@action("search_events", method=["GET"])
@action.uses('search_events.html', db, session, auth.user)
def search_events():
    username = auth.get_user()['id']
    request.GET.get("text", "")
    events = db(db.event.created_by == username).select()
    return dict(events=events)
    
# made this to get events to put into the fullCalendar
@action("get_events", method=["GET"])
@action.uses(db, session, auth.user)
def get_events():
    username = auth.get_user()['id']
    text = request.GET.get("text", "")
    events = db((db.event.name.contains(text)) & (db.event.created_by == username)).select()
    return dict(events=events)

@action("search_users/<id:int>", method=["GET"])
@action.uses('search_users.html', db, session, auth.user)
def search_users(id=None):
    text = request.GET.get("text", "")
    users = db(db.auth_user.username.contains(text)).select()
    # now get invitations
    return dict(users=users, event_id=id)

@action("get_users", method=["GET"])
@action.uses(db, session, auth.user)
def get_users():
    text = request.GET.get("text", "")
    users = db((db.auth_user.username.contains(text) & (db.auth_user.id != auth.get_user()['id']))).select()
    return dict(users=users)

@action('invite_user/<event_id>/<recipient_username>', method=["GET","POST"])
@action.uses(db, auth.user)
def invite_user(event_id, recipient_username):
    inviter_username = auth.get_user()['username']
    got = db((db.invitations.inviter==inviter_username) & (db.invitations.recipient==recipient_username) & (db.invitations.event_id==event_id)).select()
    if (len(got) <= 0): 
        db.invitations.insert(inviter=inviter_username, recipient=recipient_username, event_id=event_id)
    redirect(URL('search_users/'+event_id))

@action('get_invitations')
@action.uses('view_invitations.html', db, session, auth.user)
def get_invitations():
    username = auth.get_user()['username']
    # get invitations
    invitations = db((db.invitations.recipient==username)).select()
    # now get events those invitation event ids refer to and put them in a dict for easy lookup: events[invitation.id]
    events = dict()
    if (len(invitations) > 0):
        for invitation in invitations:
            events[invitation.id] = db(db.event.id==invitation.event_id).select()[0]
    return dict(invitations=invitations, events=events)

@action('accept_invitation/<invitation_id>', method=["GET", "DELETE"])
@action.uses(db, session, auth.user)
def accept_invitation(invitation_id):
    # username = auth.get_user()['username']
    # First, insert copy into user's event table
    invitation_set = db(db.invitations.id==invitation_id)
    invitation = invitation_set.select()[0]
    event_id = invitation.event_id
    got_event = db(db.event.id==event_id).select()[0]
    name = got_event.name
    location = got_event.location
    event_time = got_event.event_time
    description = got_event.description
    all_day = got_event.all_day
    db.event.insert(name=name, event_time=event_time, location=location, description=description, all_day=all_day)
    # then delete the invitation
    invitation_set.delete()
    redirect(URL('get_invitations'))

@action('decline_invitation/<invitation_id>', method=["GET", "DELETE"])
@action.uses(db, session, auth.user)
def decline_invitation(invitation_id):
    # delete the invitation
    invitation_set = db(db.invitations.id==invitation_id)
    invitation_set.delete()
    redirect(URL('get_invitations'))