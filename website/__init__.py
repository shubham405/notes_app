from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#LoginManager is used to find which user is logged in
from flask_login import LoginManager
from os import path
#defining database
db=SQLAlchemy() #/*database objet*/
DB_NAME="databse.db"

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='HEY'
    #my sqlite database is located in this location sqlite:///{DB_NAME}
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    #initialising our flask database
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    from .models import User,Notes
    create_database(app)
    login_manager=LoginManager()
    #login_manager.login view is used for
    #if we are not logedin where we need to go in this case it is auth.login
    login_manager.login_view='auth.login'
    #this is telling that which app we are using 
    login_manager.init_app(app)
    #@login_manager.user_loader
    #def load_user(id): this things tells flask how we load a user  
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app
def create_database(app):
    #if database doesn't exist
    if not path.exists('website'+DB_NAME):
        db.create_all(app=app)
        print('database created successfully')


