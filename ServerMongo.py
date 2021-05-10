from flask import Flask, request, Response
from random import randint
import pymongo
import json
from flask import jsonify
from bson import json_util
from bson.objectid import ObjectId



app = Flask(__name__)


connection_url = ''

client = pymongo.MongoClient(connection_url)

# Database
Database = client.get_database('sampletable')

# Table
SampleTable = Database.example

CommentTable=Database.comments


tweets = []

@app.route('/posts', methods=['POST', 'GET'])
def handle_create():
  if request.method == 'POST':
    try:
      new_tweet = {'text': request.form['tweet']}
      inserted_data=SampleTable.insert_one(new_tweet)
      tweets.append(new_tweet)
      return Response(
          response = json.dumps(
              {
              'message' : "Created user successfully",
              "id" : f"{inserted_data.inserted_id}",
              }
          ),
          status=200,
          mimetype = "application/json",
      )
    except Exception as ep:
        pass

    return {"message": "Error !", "status": 500, }


  else:
    data_set =list(SampleTable.find())
    for data in data_set:
      data["_id"] = str(data["_id"])
    return Response(
        response=json.dumps(data_set),
        status=200,
        mimetype="application/json",
    )


@app.route('/posts/<id>/comment', methods=["POST","GET"])
def add_comment(id):

    if request.method=="POST":

        if SampleTable.find({'id':id}, limit = 1) != 0:
            new_coment=CommentTable.insert_one({"comment":request.form["comment"], "tweet_id":id})
            return Response(
                response=json.dumps(
                    {
                        'message': "Created user successfully",
                        "id": f"{new_coment.inserted_id}",
                    }
                ),
                status=200,
                mimetype="application/json",
            )
        else:
            return Response(
                response=json.dumps(
                    {
                        'message': "Tweet is not Valid !",

                    }
                ),
                status=500,
                mimetype="application/json",
            )

    elif request.method=="GET":
        Comment_data = list(CommentTable.find())
        for data in Comment_data:
            data["_id"] = str(data["_id"])
        return Response(
            response=json.dumps(Comment_data),
            status=200,
            mimetype="application/json",
        )


@app.route('/posts/<id>', methods=['PUT', 'DELETE'])
def handle_single_tweet(id):

  if request.method == 'PUT':
      data = SampleTable.update_one(
          {'_id': ObjectId(id)},
          {"$set": {"text": request.form["tweet"]}},
      )
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
      else:
          return Response(
              response=json.dumps(
                  {
                      'message': "UPdate failed !",

                  }
              ),
              status=200,
              mimetype="application/json",
          )


  elif request.method == 'DELETE':
      SampleTable.delete_one({'_id': ObjectId(id)})
      resp = jsonify('User deleted successfully!')
      resp.status_code = 200
      return resp



if __name__ == '__main__':
    app.run()