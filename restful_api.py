import datetime
import math
from pymongo import MongoClient
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

client = MongoClient('localhost', 27017)
db = client['DrugstoresRestMaster']
collection = db['Drugstores']

app = Flask(__name__)
api = Api(app)

class Api(Resource):
    
    def post(self):
        data = request.get_json()
        schedule_representation = self.schedule(data)
        data.update({
            '_id':data['drugstore_id'],
            'created_at':self.current_iso_datetime(),
            'update_at':self.current_iso_datetime(),
            'schedule_representation':schedule_representation
            })
        self.to_collection(collection, data)
        return self.answer({"drugstore_id": data['drugstore_id']}), 201
    
    def put(self):
        data = request.get_json()
        if self.from_collection(collection, {'drugstore_id': data['drugstore_id']}) == None:
            schedule_representation = self.schedule(data)
            data.update({
                '_id':data['drugstore_id'],
                'created_at':self.current_iso_datetime(),
                'update_at':self.current_iso_datetime(),
                'schedule_representation':schedule_representation
                })
            self.to_collection(collection, data)
            return self.answer(data), 200
        else:
            self.update_collection(collection, data)
            return self.answer(self.from_collection(collection, data['drugstore_id'])), 200
        
    def get(self):
        data = request.get_json()
        if data == None:
            parser = reqparse.RequestParser()
            parser.add_argument("limit", type=int, required=True)
            parser.add_argument("offset", type=int, required=True)
            parser.add_argument("city_id", type=str)
            parser.add_argument("region_id", type=str)
            params = parser.parse_args()
            payload = {'result':self.from_collection_with_filtration(collection, params)}
            payload.update({"count": len(payload['result']),
                            "limit": params['limit'],
                            "offset": params['offset']
                            })
            return self.answer(payload), 200
        else:
            payload = self.from_collection(collection, data)
            return self.answer(payload), 200
    
    @app.route('/near')
    def get_near():
        parser = reqparse.RequestParser()
        parser.add_argument("lat", type=float, required=True)
        parser.add_argument("lon", type=float, required=True)
        parser.add_argument("radius", type=float, required=True)
        parser.add_argument("limit", type=int)
        parser.add_argument("offset", type=int)
        params = parser.parse_args()
        for i in params:
            if isinstance(params[i],(int,float)) == False:
                raise TypeError
        params['lat'] = math.radians(params['lat'])
        params['lon'] = math.radians(params['lon'])
        r = params['radius'] / 6371
        delta_lon = math.asin(math.sin(r) / math.cos(params['lat']))
        min_diapason = {'lat_min': math.degrees(params['lat']-r) ,'lon_min': math.degrees(params['lon']-delta_lon)}
        max_diapason = {'lat_max': math.degrees(params['lat']+r),'lon_max': math.degrees(params['lon']+delta_lon)}
        cursor = collection.find(
            {'geo.location.lat':
                 {
                     '$gte': min_diapason['lat_min'],
                     '$lte': max_diapason['lat_max']
                 },
            'geo.location.lon':
                 {
                    '$gte': min_diapason['lon_min'],
                    '$lte': max_diapason['lon_max']
                 }
            }).limit(params['limit']).skip(params['offset'])
        doc = [documents for documents in cursor]
        payload = {'result':doc}
        payload.update({"count": len(payload['result']),
                        "limit": params['limit'],
                        "offset": params['offset']
                        })
        return Api.answer(payload), 200
    
    def delete(self):
        data = request.get_json()
        self.delete_from_collection(collection, data)
        return 204
    
    @staticmethod
    def to_collection(collection, data):
        return collection.insert_one(data)
    
    @staticmethod
    def from_collection(collection, data):
        return collection.find_one(data)
    
    @staticmethod
    def from_collection_with_filtration(collection, params):
        if params['region_id'] != '' and params['city_id'] != '':
            cursor = collection.find({'geo.city_id': params['city_id'], 'geo.region_id': params['region_id']}).limit(params['limit']).skip(params['offset'])
        elif params['region_id'] == '' and params['city_id'] == '':
            cursor = collection.find({}).limit(params['limit']).skip(params['offset'])
        elif params['city_id'] == '':
            cursor = collection.find({'geo.region_id': params['region_id']}).limit(params['limit']).skip(params['offset'])
        else:
            cursor = collection.find({'geo.city_id': params['city_id']}).limit(params['limit']).skip(params['offset'])
        doc = [documents for documents in cursor]
        return doc
    
    @staticmethod
    def update_collection(collection, data):
        collection.update_one(
            {'drugstore_id': data['drugstore_id']},
            {'$set': data}
            )
        collection.update_one(
            {'drugstore_id': data['drugstore_id']},
            {'$set': {'update_at':Api.current_iso_datetime()}}
            )
        
    @staticmethod
    def delete_from_collection(collection, data):
        collection.delete_one(data)
    
    @staticmethod
    def current_iso_datetime():
        return datetime.datetime.now().isoformat()
    
    @staticmethod
    def schedule(data):
        sc = []
        for i in data['schedule']:
            sc.append((i['start'],i['end']))
        if "23:59" in sc[0]:
            schedule = "круглосуточно"
        elif len(list(dict.fromkeys(sc))) == 1:
            schedule = f"ежедневно {sc[0][0]}-{sc[0][1]}"
        else:
            schedule = f"пн-пт {sc[0][0]}-{sc[0][1]} сб, вс {sc[-1][0]}-{sc[-1][1]}"
            
        return schedule
    
    @staticmethod
    def answer(payload):
        return {
                  "status": "true",
                  "detail": "successfully",
                  "payload": payload
               }
if __name__ == '__main__':
    api.add_resource(Api, '/', '/near')
    app.run()