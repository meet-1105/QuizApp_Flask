from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from Quiz import app
from redis import Redis
# from flask_redis import FlaskRedis
API_URL = 'http://da4d-122-170-119-163.ngrok.io'

# app.config['SECRET_KEY'] = 'Myrulesmylife'
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost/quizapp"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

app.config['REDIS_HOST'] = 'localhost'
app.config['REDIS_PORT'] = 6379
app.config['REDIS_DB'] = 0
redis = Redis(app)
app.config['REDIS_URL'] = 'redis://127.0.0.1:6379'

# login_manager = LoginManager()
# login_manager.init_app(app)
