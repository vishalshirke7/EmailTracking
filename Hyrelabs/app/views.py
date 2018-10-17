from apiclient import errors
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from flask import Blueprint, url_for, redirect, render_template, render_template_string, session, request, send_from_directory
from flask import jsonify, json
from sqlalchemy import and_, desc
import datetime
from Scripts.Hyrelabs.app.decorators import login_required
from httplib2 import Http
from googleapiclient.discovery import build
from Lib import base64
from Scripts.Hyrelabs.app.db import db
from Scripts.Hyrelabs.app.models import User, Email
from requests_oauthlib import OAuth2Session
from oauth2client import file, client, tools
from oauth2client.client import Credentials, OAuth2Credentials, Storage, AccessTokenCredentials
from flask import logging
from requests.exceptions import HTTPError
from Scripts.Hyrelabs import config
from Scripts.Hyrelabs.app.forms import EmailForm

bp = Blueprint('views', __name__, url_prefix='/')


@bp.context_processor
def inject_user():
    """
    global context to check whether user is logged in

    return:  boolean value indicating user status
    """
    if 'user_id' in session:
        userid = session['user_id']
        user = User.query.get(int(userid))
        return {
            'logged_in': True,
            'user': user
        }
    return {
        'logged_in': False
    }


@bp.route('/trackingimage/<path:path>/<path:emailid>')
def send_image(path, emailid):
    """

    :param path: path to tracking image stored in static directory.
    :param emailid: unique id attached to track which email is requesting the tracking image
    :return: tracking image
    """
    email = Email.query.filter_by(id=emailid)
    email.read += 1
    db.session.add(email)
    db.session.commit()
    return send_from_directory('static', path)


@bp.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    """

    :return: returns list of sent email for individual user.
    """
    userid = session['user_id']
    emails = Email.query.filter_by(sender=userid).order_by(desc(Email.sent_at))
    return render_template('reports.html', emails=emails)


@bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    """
    This function is used to send an email using Gmail API using logged in user's account

    """
    userid = session['user_id']
    user = User.query.get(int(userid))
    form = EmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = Email()
            email.recipient = form.recipient.data
            email.subject = form.subject.data
            email.message = form.message.data
            email.sender = user.id
            db.session.add(email)
            db.session.commit()
            msg_content = form.message.data
            emailid = email.id
            msg_body = render_template('email_msg_body.html', msg_content=msg_content, emailid=emailid)
            service = create_service(userid)
            msg = create_message(user.email, form.recipient.data, form.subject.data, msg_body)
            me = 'me'
            send_message(service, me, msg)
            # emails = Email.query.filter_by(sender=userid)
            return redirect(url_for('views.reports'))
        return render_template('home.html', user=user, form=form)

    return render_template('home.html', user=user, form=form)


@bp.route('/login')
def login():
    """
    Base function to login a user using google

    :return:
    """
    if 'user_id' in session.keys():
        print("WHy the hell session is not persisting between two tabs")
        return redirect(url_for('views.home'))
    google = OAuth2Session(
        config.CLIENT_ID,
        redirect_uri=config.REDIRECT_URI,
        scope=config.SCOPE)
    auth_url, state = google.authorization_url(
        config.AUTH_URI, access_type="offline")
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)


def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text, 'html')
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  raw = base64.urlsafe_b64encode(message.as_bytes())
  raw = raw.decode()
  return {'raw': raw}
# .as_string().encode()


def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    # print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
     print('An error occurred: %s' % error)


@bp.route('/gCallback')
def callback():
    """
    Callback method for gmail login. Whenever a user enter credentials for his/her
    gmail account, the page is redirected using this method for obtaining a access token
    for making requests to gmail API

    """
    if 'user_id' in session.keys():
        return redirect(url_for('home'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        google = OAuth2Session(config.CLIENT_ID, state=request.args['state'], redirect_uri=config.REDIRECT_URI)
        try:
            token = google.fetch_token(
                config.TOKEN_URI,
                client_secret=config.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = OAuth2Session(config.CLIENT_ID, token=token)
        resp = google.get(config.USER_INFO)
        # print(resp)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User()
                user.email = email
            user.name = user_data['name']
            # print(token)
            # store = file.Storage('/tokens/'+user.email+'.txt')
            # store.put(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return redirect(url_for('views.home'))
        return 'Could not fetch your information.'


def create_service(userid):
    """
    :param userid:  currently logged in user
    :return: gmail api service instance for making gmail api calls (eg. Sending email in this case )
    """
    user = User.query.get(int(userid))
    data = json.loads(user.tokens)
    credentials = AccessTokenCredentials(data['access_token'], None)
    service = build('gmail', 'v1', http=credentials.authorize(Http()))
    return service


@bp.route('/logout')
@login_required
def logout():
    session.pop('user_id')
    return redirect(url_for('views.login'))