from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be blank!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "item not found"}, 404

    @staticmethod
    def post(name):
        if ItemModel.find_by_name(name):
            return {"message": "Item is already exits!"}, 400
        data_in = Item.parser.parse_args()
        item = ItemModel(name, data_in['price'])
        try:
            item.insert_item()
        except:
            return {"message": "An error happend while inserting"}, 500
        return {"message": "Item added", "item": item.json()}, 200

    def delete(self, name):
        if ItemModel.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))

            connection.commit()
            connection.close()
            return {'message': 'item have been deleted'}, 200
        return {'message': 'Item did not exist!'}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            try:
                updated_item.insert_item()
            except:
                return {"message": "An error occurded while inserting data"}, 500
        else:
            try:
                updated_item.update_item()
            except:
                return {"message": "An error occurded while updateing data"}, 500
        return updated_item.json(), 200


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        rows = result.fetchall()
        items = []
        for row in rows:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()
        return {'items': items}, 200
