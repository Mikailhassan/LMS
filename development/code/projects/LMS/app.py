from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from resources import resources_bp
from models import db

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super secret' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
ma = Marshmallow(app)
db.init_app(app)
migrate = Migrate(app, db)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'mikailismail260@gmail.com'  
app.config['MAIL_PASSWORD'] = 'cbem mgim nxvd mrnw'
app.config['MAIL_DEFAULT_SENDER'] = 'mikailismail260@gmail.com'


# Registering the resources blueprint
app.register_blueprint(resources_bp)

if __name__ == '__main__':
    app.run(debug=True)
