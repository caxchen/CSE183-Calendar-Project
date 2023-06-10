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

@action("create_venue", method=["GET", "POST"])
@action.uses("create_venue.html", db, session, auth.user)
def create_venue():
    form = Form(db.venue, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

@action('edit_event/<id:int>', method=["GET", "POST"])
@action.uses('edit_event.html', db, session, auth.user)
def edit_event(id=None):
    assert id is not None
    edit_event = db.event[id]
    # if edit_event.created_by != auth.user(): raise HTTP(400)
    if edit_event is None:
        redirect(URL('index'))
    form = Form(db.event, record=edit_event, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('view_event', id))
    return dict(form=form)

@action('edit_venue/<id:int>', method=["GET", "POST"])
@action.uses('edit_venue.html', db, session, auth.user)
def edit_venue(id=None):
    assert id is not None
    edit_venue = db.venue[id]
    # if edit_event.created_by != auth.user(): raise HTTP(400)
    if edit_venue is None:
        redirect(URL('index'))
    form = Form(db.venue, record=edit_venue, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('view_venue', id))
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

@action('view_venue/<id:int>', method=["GET", "POST"])
@action.uses('view_venue.html', db, session, auth.user)
def view_venue(id=None):
    assert id is not None
    edit_venue = db.venue[id]
    if edit_venue is None:
        redirect(URL('index'))
    rows = db(db.venue.id == id).select()
    return dict(venues=rows)

@action('delete_event/<id:int>')
@action.uses(db, session, auth.user)
def delete_event(id=None):
    assert id is not None
    event_id = db.event[id]
    if event_id is None:
        redirect(URL('index'))
    db(db.event.id == id).delete()
    redirect(URL('index'))

@action('delete_venue/<id:int>')
@action.uses(db, session, auth.user)
def delete_venue(id=None):
    assert id is not None
    venue_id = db.venue[id]
    if venue_id is None:
        redirect(URL('index'))
    db(db.venue.id == id).delete()
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
    #invitations = db(db.invitations.)
    return dict(users=users, event_id=id)

@action("get_users", method=["GET"])
@action.uses(db, session, auth.user)
def get_users():
    text = request.GET.get("text", "")
    users = db((db.auth_user.username.contains(text) & (db.auth_user.id != auth.get_user()['id']))).select()
    return dict(users=users)

# made this to get venues to put into searchEvents
@action("get_venues", method=["GET"])
@action.uses(db, session, auth.user)
def get_events():
    # username = auth.get_user()['id']
    text = request.GET.get("text", "")
    venues = db((db.venue.venue_name.contains(text))).select()
    return dict(venues=venues)

@action("search_venues", method=["GET"])
@action.uses('search_venues.html', db, session, auth.user)
def search_events():
    #username = auth.get_user()['id']
    request.GET.get("text", "")
    venues = db(db.venue).select()
    return dict(venues=venues)


### category ###
@action("create_category", method=["GET", "POST"])
@action.uses("create_category.html", db, session, auth.user)
def create_category():
    form = Form(db.category, fields=['category_name', 'color'], csrf_session=session, formstyle=FormStyleBulma)
    cat = request.params.get('cat_name')
    colors = request.params.get('color')

    db.category.insert(color=colors, category_name=cat)
    events = db(db.event).select()
    categories = db(db.category).select()
    print("redirecting to", URL("index"))
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form, events=events, categories=categories)

@action('edit_category/<id:int>', method=["GET", "POST"])
@action.uses('edit_category.html', db, session, auth.user)
def edit_category(id=None):
    assert id is not None
    edit_category = db.category[id]
    if edit_category is None:
        redirect(URL('index'))
    form = Form(db.category, fields=['category_name', 'category_description', 'color'], record=edit_category, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('view_category', id))
    return dict(form=form)

@action('view_category/<id:int>', method=["GET", "POST"])
@action.uses('view_category.html', db, session, auth.user)
def view_category(id=None):
    assert id is not None
    view_category = db.category[id]
    if view_category is None:
        redirect(URL('index'))
    rows = db(db.category.id == id).select()
    return dict(cat=rows)

@action('delete_category/<id:int>')
@action.uses(db, session, auth.user)
def delete_category(id=None):
    assert id is not None
    category_id = db.category[id]
    if category_id is None:
        redirect(URL('index'))
    db(db.category.id == id).delete()
    redirect(URL('index'))


@action('apply_category', method=["POST", "GET"])
@action.uses('create_category.html',db, session, auth.user)
def apply_category():
    event_id = request.params.get('event_id')
    category_id = request.params.get('category_id')

    # Retrieve the event and category objects from the database
    event = db.event[event_id]
    category = db.category[category_id]

    if event and category:
        # Apply the category to the event
        event.category_id = category.id
        event.update_record()

        # Return the category color in the response
        #return {'categoryColor': category.color}
        return dict(event=event, category=category)
    # stays on same page
    redirect(URL('create_category'))





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
    venue = got_event.venue
    name = got_event.name
    event_time = got_event.event_time
    description = got_event.description
    all_day = got_event.all_day
    db.event.insert(venue=venue, name=name, event_time=event_time, description=description, all_day=all_day)
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