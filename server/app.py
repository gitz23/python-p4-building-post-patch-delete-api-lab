#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(
            jsonify(response_body),
            404
        )
        return response
    
    elif request.method == 'GET':
        bakery_serialized = bakery.to_dict()

        response = make_response(
            bakery_serialized,
            200
        )
        return response
    
    elif request.method == 'PATCH':
        for name in request.form:
            setattr(bakery, name, request.form.get(name))
        
        db.session.add(bakery)
        db.session.commit()

        bakery_dict = bakery.to_dict()
        
        response = make_response(
            jsonify(bakery_dict), 
            200
        )
        return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    if request.method == 'GET':
        baked_goods=[]
        for baked_good in BakedGood.query.all():
            baked_good_dict = baked_good.to_dict()  
            baked_goods.append(baked_good_dict)

        response = make_response(
            jsonify(baked_goods),
            200
        )
        return response
    
    elif request.method == 'POST':
        new_baked_good = BakedGood(
            name = request.form.get("name"),
            price = request.form.get("price"),
            created_at =request.form.get("created_at"),
            updated_at =request.form.get("updated_at"),
        )

        db.session.add(new_baked_good)
        db.session.commit()

        baked_good_dict = new_baked_good.to_dict()

        response = make_response(
            jsonify(baked_good_dict),
            #code request was completed successfully
            201
        )
        return response
    
@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE'])
def baked_goods_by_id(id):
    baked_good = BakedGood.query.filter_by(id=id).first()

    if baked_good == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(
            jsonify(response_body),
            404
        )
        return response
    
    elif request.method == 'DELETE':
        db.session.delete(baked_good)
        db.session.commit()

        response_body = {
            "delete_successful": True, 
            "message": "Baked good deleted"
        }
        response = (
            jsonify(response_body), 
            200
        )
        return response 


if __name__ == '__main__':
    app.run(port=5555, debug=True)
