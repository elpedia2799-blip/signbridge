import os
from flask import Flask, render_template
from config import Config
from database.db import db
from flask_login import LoginManager
from models.user import User

from routes.main import main
from routes.auth import auth
from routes.interpreter import interpreter
from routes.learning import learning
from routes.dictionary import dictionary
from routes.dashboard import dashboard
from routes.admin import admin

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(main)
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(interpreter, url_prefix="/interpreter")
app.register_blueprint(learning, url_prefix="/learning")
app.register_blueprint(dictionary, url_prefix="/dictionary")
app.register_blueprint(dashboard, url_prefix="/dashboard")
app.register_blueprint(admin, url_prefix="/admin")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
