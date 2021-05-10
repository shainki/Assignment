from ServerMongo import connection_url
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request, Flask, Response
import pymongo, json



app = Flask(__name__)

client = pymongo.MongoClient(connection_url)

# Database
Database = client.get_database('crud')
# Table
SampleTable = Database.userdata



@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':

        SampleTable.insert_one({'name': request.form["name"], 'pwd': request.form["password"]})
        resp = jsonify('User added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()

#Get Method

@app.route('/users', methods=["GET"])
def users():
    data_set = list(SampleTable.find())
    for data in data_set:
        data["_id"] = str(data["_id"])
    return Response(
        response=json.dumps(data_set),
        status=200,
        mimetype="application/json",
    )


@app.route('/user/<id>', methods=["GET"])
def user(id):

    user = SampleTable.find_one({'_id': ObjectId(id)})
    user["_id"]=str(user.get("_id"))
    return Response(
        response=json.dumps(user),
        status=200,
        mimetype="application/json",
    )


@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    try:
        user_exist=True
        SampleTable.find_one({'_id': ObjectId(id)})
    except Exception as e:
        user_exist=False

    try:
        name=request.form["name"]
    except Exception as e:
        name=""

    try:
        password=request.form["password"]
    except Exception as e:
        password=""

    if name and password and user_exist:

        data = SampleTable.update_one(
            {'_id': ObjectId(id)},
            {"$set": {"name": request.form["name"],"pwd": request.form["password"]}},

        )
    elif name and user_exist:
        data = SampleTable.update_one(
            {'_id': ObjectId(id)},
            {"$set": {"name": request.form["name"]}},

        )
    elif password and user_exist:
        data = SampleTable.update_one(
            {'_id': ObjectId(id)},
            {"$set": {"pwd": request.form["password"]}},

        )

    else:
        if not user_exist:
            resp = jsonify('Error !! NOt a valid userID')
            resp.status_code = 404
            return resp
        else:
            resp = jsonify('Error !! (Name OR Password)One is mandate ')
            resp.status_code = 500
            return resp

    if data.modified_count == 1:
        return Response(
            response=json.dumps(
                {
                    'message': "User Updated !",

                }
            ),
            status=200,
            mimetype="application/json",
        )


@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    SampleTable.delete_one({'_id': ObjectId(id)})
    resp = jsonify('User deleted successfully!')
    resp.status_code = 200
    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run()