import os
from flask_admin import Admin
from models import db, Users, People, Planets, Startships, Favorites
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here: User, People, Planetrs, Startships
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(Startships, db.session))

    #Special view for favorite table
    class FavoritesView(ModelView):
        column_list = ('people_id', 'planets_id', 'startships_id', 'users_id')
        form_columns = ('people_id', 'planets_id', 'startships_id', 'users_id')
    
    # Add your models here: Favorites (ForeignKey)    
    admin.add_view(FavoritesView(Favorites, db.session))
   