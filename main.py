from flask import Flask, render_template, url_for, redirect, flash
#from flask_sqlalchemy import SQLAlchemy #need to install flask-sqlalchemy
#from flask.ext.mysql import MySQL


app = Flask(__name__)
#app.config['SECRET_KEY']= 'hf9789fdfasd234567jhgdjkjfasd' #won't need this after implmenting google
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #using sqlite for easier testing and implementation, can switch later
#db = SQLAlchemy(app)



@app.route('/', methods = ['GET', 'POST'])
def main():
    #the following lists are used for now to get templating to work
    #they will be removed later once we get actual database data
    #the looping in index.html will need to change also
    years = [1,2,3,4]
    quarters = ["Fall", "Winter", "Spring", "Summer"]
    return render_template('index.html', years=years, quarters=quarters)

@app.route('/save')
def save():
    #saving data to database here


    flash("Your 4 year plan has been successfully saved", 'success')


    #returning to login page
    return redirect(url_for('main'));



if __name__ == "__main__":
    app.run(debug = True) #Set debug = False in a production environment
