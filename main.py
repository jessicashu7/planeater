from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def main():
        return render_template('index.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug = True) #Set debug = False in a production environment
