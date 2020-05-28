from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be blank!")

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': "item not found"}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        else:
            return None

    def post(self, name):
        if self.find_by_name(name):
            return {"message": "Item is already exits!"}, 400
        data_in = Item.parser.parse_args()
        item = {'name': name, 'price': data_in['price']}
        try:
            self.insert_item(item)
        except:
            return {"message": "An error happend while inserting"}, 500
        return {"message": "Item added", "item": item}, 200

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        if self.find_by_name(name):
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
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert_item(updated_item)
            except:
                return {"message": "An error occurded while inserting data"}, 500
        else:
            try:
                self.update_item(updated_item)
            except:
                return {"message": "An error occurded while updateing data"}, 500
        return updated_item, 200

    def update_item(self, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


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
