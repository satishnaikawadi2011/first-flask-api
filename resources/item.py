from flask_restful import Resource,reqparse
from models.item import ItemModel
from flask_jwt import jwt_required

class Item(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('store_id',type=int,required=True,help='Every item must have store id')
    parser.add_argument('price',type=float,required=True,help='This field must not be blank')

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'item not found!'},404

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message':f"An item with name {name} already exists!"},400

        data = Item.parser.parse_args()

        item = ItemModel(name,data['price'],data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message':'An error occurred during saving the item to database!'},500

        return item.json(),201


    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':'Item deleted successfully!'},200

    def patch(self,name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            return {'message':'Item not found!'},404
        else:
            item.price = data['price']
            item.save_to_db()
            return item.json()

class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}