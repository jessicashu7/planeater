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

@app.route('/', methods = ['GET'])
def main():
    #the following lists are used for now to get templating to work
    #they will be removed later once we get actual database data
    #the looping in index.html will need to change also
    years = [1,2,3,4]
    quarters = ["Fall", "Winter", "Spring", "Summer"]
#    conn = mysql.connect()
#    cursor = conn.cursor()
#    statement = 'SELECT * FROM inputclass'
#    cursor.execute('SELECT * FROM inputclass')
#    posts = cursor.fetchall()
#    for p in posts:
#        print(p)
#        print(type(p))


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
            name = request.form[str(y) + "_" + q]
            units = request.form[str(y) + "_" + q + "_units"]
            if name != "" or units !="": #if both fields blank, no need to insert in database
                #format statement puts in name and units (NULL if nothing entered in field)
                name = (("'{}'".format(name)) if name != "" else "NULL")
                units = (float(units) if units != "" else "NULL")
                statement = "INSERT INTO inputclass VALUES (1, '{}', '{}', {}, {}) ON DUPLICATE KEY UPDATE name={}, units={};".format(y,q,name, units, name, units)
                cursor.execute(statement)
                conn.commit()
                flash("Your 4 year plan has been successfully saved", 'success')

    #returning to login page
    return redirect(url_for('main'));



if __name__ == "__main__":
    app.run(debug = True) #Set debug = False in a production environment
