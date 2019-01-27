from flask import Flask, render_template, url_for, redirect, flash, request,session, jsonify
from flaskext.mysql import MySQL
from functools import wraps
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask_oauthlib.client import OAuth
from auth import OAuthSignIn


app = Flask(__name__)
app.config['SECRET_KEY']= 'hf9789fdfasd234567jhgdjkjfasd' #won't need this after implmenting google
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Lockdown1!'
app.config['MYSQL_DATABASE_DB'] = 'planeater'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


app.config['GOOGLE_ID'] = "220365352452-1s6a4kaklt0hop8fnjfti0ojfl9hqgr5.apps.googleusercontent.com"
app.config['GOOGLE_SECRET'] = "zXmfJl0CljOg-zEew41bLKi2" #currently Brian's test google project

oauth = OAuth(app)
mysql = MySQL()
mysql.init_app(app)

google = oauth.remote_app(
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

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))


@app.route('/', methods = ['GET'])
# @login_required
def main():
    #plan represents all four years. it is a dictionary
    #which matches year# to dictionary of quarters, which matches
    #quarter (represented in 0-3) to list of tuples of name, units
    # 0 is fall, 1 is winter, 2 is spring, 3 is summer
    # "" and -1 are default values for name, units

    if 'google_token' in session:
        plan = {
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

        conn = mysql.connect()
        cursor = conn.cursor()
        return render_template('index.html', plan=plan)
    return redirect(url_for('login'))

@app.route('/save', methods=['POST'])
def save():
    #need an if here checking if the person is logged in or not to the webpage
    #if yes, proceed to database, else prompt them to login first
    #saving data to database here
    conn = mysql.connect()
    cursor = conn.cursor()
    years = [1,2,3,4]
    quarters = [1, 2, 3, 4]
    classes = [1,2,3,4]
    for y in years:
        for q in quarters:
            for c in classes:
                name = request.form[str(y) + "_" + str(q) + "_" + str(c)]
                units = request.form[str(y) + "_" + str(q) + "_" + str(c) + "_units"]
                if name != "" or units !="": #if both fields blank, no need to insert in database
                    #format statement puts in name and units (NULL if nothing entered in field)
                    name = (("'{}'".format(name)) if name != "" else "NULL")
                    units = (float(units) if units != "" else "NULL")
                    statement = "INSERT INTO inputclass VALUES (1, {}, {}, {}, {}, {}) ON DUPLICATE KEY UPDATE name={}, units={};".format(y,q, c, name, units, name, units)
                    cursor.execute(statement)
                    conn.commit()
    else:
        flash("Your 4 year plan has been successfully saved", 'success')
    #returning to login page
    return redirect(url_for('main'));


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return redirect(url_for("main"))
    #return jsonify({"data": me.data})


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')




if __name__ == "__main__":
    app.run(debug = True) #Set debug = False in a production environment
