from flask import Flask, render_template, url_for, redirect, flash, request,session, jsonify
from functools import wraps
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask_dance.contrib.google import google
from flask_oauthlib.client import OAuth
from auth import OAuthSignIn
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import secret
import copy

# Use a service account
cred = credentials.Certificate('planeater-ad76f9668f15.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)
app.config['SECRET_KEY']= 'hf9789fdfasd234567jhgdjkjfasd' #won't need this after implmenting google
app.config['GOOGLE_ID'] = secret.client_id
app.config['GOOGLE_SECRET'] = secret.secret_key
oauth = OAuth(app)

empty_plan = {
    1 : {
            1 : [("",-1),("",-1),("",-1),("",-1)],
            2 : [("",-1),("",-1),("",-1),("",-1)],
            3 : [("",-1),("",-1),("",-1),("",-1)],
            4 : [("",-1),("",-1),("",-1),("",-1)]
        },
    2 : {
            1 : [("",-1),("",-1),("",-1),("",-1)],
            2 : [("",-1),("",-1),("",-1),("",-1)],
            3 : [("",-1),("",-1),("",-1),("",-1)],
            4 : [("",-1),("",-1),("",-1),("",-1)]
        },
    3 : {
            1 : [("",-1),("",-1),("",-1),("",-1)],
            2 : [("",-1),("",-1),("",-1),("",-1)],
            3 : [("",-1),("",-1),("",-1),("",-1)],
            4 : [("",-1),("",-1),("",-1),("",-1)]
        },
    4 : {
            1 : [("",-1),("",-1),("",-1),("",-1)],
            2 : [("",-1),("",-1),("",-1),("",-1)],
            3 : [("",-1),("",-1),("",-1),("",-1)],
            4 : [("",-1),("",-1),("",-1),("",-1)]
        }
}
temp_plan = copy.deepcopy(empty_plan)


google_auth = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/update', methods=['POST'])
def update_user_plan():

    user_plan = copy.deepcopy(empty_plan)
    years = [1,2,3,4]
    quarters = [1, 2, 3, 4]
    classes = [1,2,3,4]
    for y in years:
        for q in quarters:
            for c in classes:
                name = request.form[str(y) + "_" + str(q) + "_" + str(c)]
                units = request.form[str(y) + "_" + str(q) + "_" + str(c) + "_units"]
                if name != "" or units !="":
                    user_plan[y][q][c-1] = (name if name != "" else "", float(units) if units != "" else -1)

    return user_plan


@app.route('/login', methods= ['GET','POST'] )
def login():
    global temp_plan
    temp_plan = update_user_plan()

    #plan = update_user_plan()
    return google_auth.authorize(callback=url_for('authorized', _external=True), prompt = "consent")


@app.route('/logout', methods = [ "GET", 'POST'])
def logout():
    session.clear()
    global temp_plan
    temp_plan = copy.deepcopy(empty_plan)
    return redirect(url_for("main"))



@app.route('/', methods = ['GET'])
def main():
    #plan represents all four years. it is a dictionary
    #which matches year# to dictionary of quarters, which matches
    #quarter (represented in 0-3) to list of tuples of name, units
    # 0 is fall, 1 is winter, 2 is spring, 3 is summer
    # "" and -1 are # values for name, units
    global temp_plan
    if 'google_token' in session:
        plan_doc_ref = db.collection(u'userplans').document(get_user_data()['email'])
        plan_dict = plan_doc_ref.get().to_dict()
        if plan_dict == None:
            plan = copy.deepcopy(temp_plan)
        else:
            plan = json.loads(plan_dict['plan'])
        user_picture = get_user_data()["picture"] #link to your profile picture
        #if no user picture must have error checking

        return render_template('index.html', plan=plan, picture = user_picture, logged_in = True)
    return render_template('index.html', plan=temp_plan, picture = None, logged_in = False)

@app.route('/save', methods=['POST', 'GET '])
def save():
    #need an if here checking if the person is logged in or not to the webpage
    #if yes, proceed to database, else prompt them to login first
    #saving data to database

    if 'google_token' in session:
        plan = update_user_plan()


        flash("Your 4 year plan has been successfully saved", 'success')

        doc_ref = db.collection(u'userplans').document(get_user_data()['email'])
        doc_ref.set({
                u'plan': json.dumps(plan)
        })
        return redirect(url_for('main'));
    else:
        global temp_plan
        temp_plan = update_user_plan()
        flash("Please login in to save!", 'warning')
        return redirect(url_for('main'))



@app.route('/login/authorized')
def authorized():
    resp = google_auth.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    return redirect(url_for("main"))


@google_auth.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

def get_user_data():
    user_data =  google_auth.get('userinfo')
    # for x in user_data.data.items():
    #     print(x)   #printing user data
    return user_data.data #this is a dictionary of user_data


if __name__ == "__main__":
    app.run(debug = True) #Set debug = False in a production environment
