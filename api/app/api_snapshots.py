from app import app, api
from flask import Flask, request, g
from flask_restful import Api, Resource, reqparse


class APISnapshot(Resource):
    decorators = [jwt_required]

    def get(self, snapshot_id):
        snapshot = Snapshots.objects.get(screenshot=bson.objectid.ObjectId(snapshot_id))
        snapshot_file = snapshot.screenshot.read()
        filename = "%s.png" %(snapshot_id)
        response = make_response(snapshot_file)
        response.headers['Content-Type'] = "image/png"
        return response

api.add_resource(APIScreenshot, '/api/v1/snapshot/<string:snapshot_id>')


class APISnapshots(Resource):
    decorators = [jwt_required]

    def __init__(self):
        self.args = reqparse.RequestParser()
        if request.method == "GET":
            self.args.add_argument('max', location='args', required=False, help='max entries', type=int, default=25)
            self.args.add_argument('search', location='args', required=False, default="")

    def get(self):
        args = self.args.parse_args()
        get_snaps = Snapshots.objects(target__contains=args.search).order_by('-timestamp').limit(args.max)
        results = json.loads(get_snaps.to_json())
        return results

api.add_resource(APIScreenshots, '/api/v1/snapshots')
