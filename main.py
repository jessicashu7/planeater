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
