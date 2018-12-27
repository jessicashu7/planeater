from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def main():
        #the following lists are used for now to get templating to work
        #they will be removed later once we get actual database data
        #the looping in index.html will need to change also
        y = [1,2,3,4]
        q = ["Fall", "Winter", "Spring", "Summer"]
        return render_template('index.html', years=y, quarters=q)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug = True) #Set debug = False in a production environment
