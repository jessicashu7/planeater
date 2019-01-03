from flask import Flask, render_template, url_for, redirect, flash, request
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['SECRET_KEY']= 'hf9789fdfasd234567jhgdjkjfasd' #won't need this after implmenting google
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #using sqlite for easier testing and implementation, can switch later
#db = SQLAlchemy(app)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mypassword!'
app.config['MYSQL_DATABASE_DB'] = 'planeater'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL()
mysql.init_app(app)

@app.route('/', methods = ['GET', 'POST'])
def main():
    #the following lists are used for now to get templating to work
    #they will be removed later once we get actual database data
    #the looping in index.html will need to change also
    years = [1,2,3,4]
    quarters = ["Fall", "Winter", "Spring", "Summer"]
    return render_template('index.html', years=years, quarters=quarters)

@app.route('/save', methods=['POST'])
def save():
    #saving data to database here
    conn = mysql.connect()
    cursor = conn.cursor()
    years = [1,2,3,4]
    quarters = ["Fall", "Winter", "Spring", "Summer"]
    for y in years:
        for q in quarters:
            yq = request.form[str(y) + "_" + q]
            yqu = request.form[str(y) + "_" + q + "_units"]
            print(type(yq))
            print("name: " + yq)
            print("is none: " + str(yq == "") )
            print(type(yqu))
            print("units: "+ yqu)
            print("is none: " + str(yqu == "") )
            if yq != "" or yqu !="":
                statement = "INSERT INTO class (name, units) VALUES ({}, {});".format((("'{}'".format(yq)) if yq != "" else "NULL"), (float(yqu) if yqu != "" else "NULL"))
                cursor.execute(statement)
                conn.commit()
                flash("Your 4 year plan has been successfully saved", 'success')


    #returning to login page
    return redirect(url_for('main'));



if __name__ == "__main__":
    app.run(debug = True) #Set debug = False in a production environment
