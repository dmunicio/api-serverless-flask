from flask_sqlalchemy import SQLAlchemy
import os

def create_app(Flask):
    app = Flask(__name__)
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    local_postgresql_url = 'postgresql+psycopg2://root:admin123@app-db:5432/root'
    postgresql_url = os.environ.get('SQLALCHEMY_DATABASE_URI', local_postgresql_url)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = postgresql_url
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    db.app = app
    from .models.user import setup_models    
    app.config["users.db"] = setup_models(db)

    with app.app_context():
        db.create_all()  # Create sql tables for our data models
        db.session.commit()

    return app
