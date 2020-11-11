from flask import Flask
from flask_restful import Resource,Api
from flask_jwt import JWT,jwt_required

from resources.item import Item,ItemList
from resources.user import UserRegister
from resources.store import Store,StoreList
from security import authenticate,identity


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'thisismysecret'
api = Api(app)

jwt = JWT(app,authenticate,identity)  #authentication

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Item,'/item/<string:name>')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister,'/register')

if __name__=='__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)