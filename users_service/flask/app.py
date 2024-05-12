from flask import Flask, request, jsonify
from db import users,db
from bson import ObjectId


app = Flask(__name__)



@app.route("/getusers",methods=["GET"])
def getusers():
    Users=[]
    _users=users.find()
  
    for index, user in enumerate(_users, start=1):
        Users.append({"user{}".format(index): str(user)})

    return jsonify(Users)



@app.route("/push",methods=['POST'])
def Push():
    _user=request.get_json()
    result=users.insert_one(_user)
    return jsonify({"message": "User created successfully", "id": str(result)}), 201


@app.route("/update",methods=['POST'])
def update_by_name():
    _user=request.get_json()
    myval={"$set":{"password":_user['password']}}
    users.update_one({"name":_user["name"]},myval)
    return 'done',200


@app.route('/update/<string:document_id>', methods=['PUT'])
def update_document_by_id(document_id):
    try:
        # Get the new name and password from the request body
        data = request.json
        new_name = data.get('name')
        new_password = data.get('password')

        # Update the document in the collection
        result = users.update_one(
            {'_id': ObjectId(document_id)},
            {'$set': {'name': new_name, 'password': new_password}}
        )

        if result.modified_count == 1:
            return jsonify({'message': 'Document updated successfully'}), 200
        else:
            return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/delete",methods=['DELETE'])
def delete_by_name_pass():
    _user=request.get_json()
    users.delete_one({"name":_user["name"],"password":_user["password"]})
    return 'done',200




@app.route("/pull",methods=['GET'])
def pulling():
    _users=request.get_json()
    usersquery=[]
   
    pulldata=users.find({"name":_users["name"]})
    for i in pulldata:
        usersquery.append({"name":i["name"],"passsword":i["passsword"]})
    return jsonify(usersquery)



@app.route("/users", methods=["POST"])
def create_user():
    user_data = request.get_json() 
    result = db.users.insert_one(user_data)
    return jsonify({"message": "User created successfully", "id": str(result.inserted_id)}), 201






@app.route("/deleteuser/<string:user_id>", methods=['DELETE'])
def Delete_By_ID(user_id):
    """
       Function to remove the user.
       """
        # Delete the user
    result=db.users.delete_one({"_id": ObjectId(user_id)})

        
    return jsonify({"message": "User delete successfully", "id": str(result)}), 201


@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user with notFound 404 status."""
    # Message to the user
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp





if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)