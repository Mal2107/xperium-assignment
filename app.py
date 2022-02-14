from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import loads, dumps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["MONGO_DBNAME"] = "HotelManagement"
app.config["MONGO_URI"] = "mongodb+srv://admin:599PmNaNaSLzVyU@cluster0.bxytl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


mongo = PyMongo(app)


def convertToJSON(data):
	print(dumps(data))
	return dumps(data)


@app.route('/')
def hello_world():
	return "This is my first flask api call"


@app.route('/getGuests',methods = ["GET"])
def getGuests():
	try:

		guests = mongo.db.guests

		try:
			mongoGuests = guests.find({})
			guestsData = []
			
			for guest in mongoGuests:
				
				# guestsData.append(convertToJSON(guest))
				gData = {}
				gData["name"] = guest["name"]
				gData["age"] = guest["age"]
				gData["adhaarNumber"] = guest["adhaarNumber"]
				gData["checkInDate"] = guest["checkInDate"]
				gData["durationOfStay"] = guest["durationOfStay"]
				gData["allotedRoom"] = guest["allotedRoom"]
				gData["costOfRoomPrice"] = guest["costOfRoomPrice"]
				
				guestsData.append(gData)

		except:
			output = {"success":False,"message":"Error In Loading Guest"}
			return jsonify(output),500

		output = {"success":True,"message":"Loaded Guests","data":guestsData}
		return jsonify(output),200

	except:
		output = {"success":False,"message":"Internal Server Error"}
		return jsonify(output),500


@app.route('/addGuest',methods=["POST"])
def addGuest():
	try:
		guests = mongo.db.guests
		
		#get data from request
		try:
			name = request.json["name"]
			age = request.json["age"]
			adhaarNumber = request.json["adhaarNumber"]
			checkInDate = request.json["checkInDate"]
			durationOfStay = request.json["durationOfStay"]
			costOfRoomPrice = request.json["costOfRoomPrice"]
			allotedRoom = request.json["allotedRoom"]
		except:
			output = {"success":False,"message":"Invalid request Body"}
			return jsonify(output),400
		
		# Add guest To mongo
		try:		
			guest_id = guests.insert_one({"name":name,
									      "age":age,
									      "adhaarNumber":adhaarNumber,
									      "checkInDate":checkInDate,
									      "durationOfStay":durationOfStay,
									      "costOfRoomPrice":costOfRoomPrice,
									      "allotedRoom":allotedRoom})
		except:
			output = {"success":False,"message":"Error In Adding Guest"}
			return jsonify(output),500
		# fetch guest from mongo and return to user
		print(guest_id)
		new_guest = guests.find_one({'_id':guest_id.inserted_id})
		output = {"success":True,"message":"Guest added successfully"}
		return jsonify(output),201
	except:
		output = {"success":False,"message":"Internal Server Error"}
		return jsonify(output),500

@app.route('/deleteGuest',methods=["POST"])
def deleteGuest():
	try:
		guests = mongo.db.guests
		
		#get data from request
		try:	
			adhaarNumber = request.json["adhaarNumber"]
		except:
			output = {"success":False,"message":"Invalid request Body"}
			return jsonify(output),400
	
		# Add guest To mongo
		try:		
			guest_id = guests.delete_one({"adhaarNumber":adhaarNumber})
		except:
			output = {"success":False,"message":"Error In Deleting Guest"}
			return jsonify(output),500

		# Check delete count
		if guest_id.deleted_count > 0:
				output = {"success":True,"message":"Deleted Guest Successfully"}
		else:
				output = {"success":False,"message":"No Guest Found"}
		return jsonify(output)
	except:
		output = {"success":False,"message":"Internal Server Error"}
		return jsonify(output),500

@app.route('/updateGuest',methods=["POST"])
def updateGuest():
	try:
		guests = mongo.db.guests
		
		#get data from request
		try:	
			adhaarNumber = request.json["adhaarNumber"]
			name = request.json["name"]
			age = request.json["age"]
			adhaarNumber = request.json["adhaarNumber"]
			checkInDate = request.json["checkInDate"]
			durationOfStay = request.json["durationOfStay"]
			costOfRoomPrice = request.json["costOfRoomPrice"]
			allotedRoom = request.json["allotedRoom"]
		except:
			output = {"success":False,"message":"Invalid request Body"}
			return jsonify(output),400
	
		# Add guest To mongo
		try:		
			guest_id = guests.update_one({"adhaarNumber":adhaarNumber},
										{
											"$set":{
												"name":name,
												"age":age,
												"adhaarNumber":adhaarNumber,
												"checkInDate":checkInDate,
												"durationOfStay":durationOfStay,
												"costOfRoomPrice":costOfRoomPrice,
												"allotedRoom":allotedRoom	
											}
										})
		except:
			output = {"success":False,"message":"Error In Updating Guest"}
			return jsonify(output),500

		# Check delete count
		if guest_id.modified_count > 0:
				output = {"success":True,"message":"Guest Updated Successfully"}
		else:
				output = {"success":False,"message":"No Guest Found"}
		return jsonify(output)
	except:
		output = {"success":False,"message":"Internal Server Error"}
		return jsonify(output),500



if __name__ == '__main__':
	app.run(debug=True)