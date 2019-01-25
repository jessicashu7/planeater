from flask import Flask, render_template, url_for, redirect, flash, request,g
from flaskext.mysql import MySQL
from functools import wraps
from flask_login import login_user, logout_user, current_user, login_required, LoginManager

from flask_oauth2_login import GoogleLogin
from auth import OAuthSignIn


app = Flask(__name__)
app.config['SECRET_KEY']= 'hf9789fdfasd234567jhgdjkjfasd' #won't need this after implmenting google
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Lockdown1!'
app.config['MYSQL_DATABASE_DB'] = 'planeater'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

app.config.update(
  SECRET_KEY="secret",
  GOOGLE_LOGIN_REDIRECT_SCHEME="http",
)


# for config in (
#   "GOOGLE_LOGIN_CLIENT_ID",
#   "GOOGLE_LOGIN_CLIENT_SECRET",
# ):
  # app.config[config] = os.environ[config]
# google_login = GoogleLogin(app)
# app.config.from_object('config')
# app.secret_key = 'this is very secret'
#
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'


mysql = MySQL()
mysql.init_app(app)
#oauth = OAuth(app)


# @login_manager.user_loader
# def load_user(id):
#     return User.find_by_id(id)
#
#
# @app.route('/authorize/<provider>')
# def oauth_authorize(provider):
#     # Flask-Login function
#     if not current_user.is_anonymous():
#         return redirect(url_for('index'))
#     oauth = OAuthSignIn.get_provider(provider)
#     return oauth.authorize()
#
# @app.route('/callback/<provider>')
# def oauth_callback(provider):
#     if not current_user.is_anonymous():
#         return redirect(url_for('index'))
#     oauth = OAuthSignIn.get_provider(provider)
#     username, email = oauth.callback()
#
#     if email is None:
#         # I need a valid email address for my user identification
#         flash('Authentication failed.')
#         return redirect(url_for('index'))
#
#     # Look if the user already exists
#     user = User.find_or_create_by_email(email)
#
#     # Log in the user, by default remembering them for their next visit
#     # unless they log out.
#     login_user(user, remember=True)
#     return redirect(url_for('index'))
#
#
# @app.route('/login', methods = ['POST', 'GET'])
# def login():
#     if current_user is not None and current_user.is_authenticated():
#         user = User()
#         login_user(user)
#         return redirect(url_for('main'))
#     return render_template('login.html',title='Sign In')
#


@app.route('/', methods = ['GET'])
# @login_required
def main():
    #plan represents all four years. it is a dictionary
    #which matches year# to dictionary of quarters, which matches
    #quarter (represented in 0-3) to list of tuples of name, units
    # 0 is fall, 1 is winter, 2 is spring, 3 is summer
    # "" and -1 are default values for name, units
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




if __name__ == "__main__":
    app.run(debug = True) #Set debug = False in a production environment
