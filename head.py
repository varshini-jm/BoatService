from flask import *
import requests
from flask_mongoengine import MongoEngine #for interaction b/w flask and mongodb

app=Flask(__name__)
#to connect to mongodb settings related to API
DB_URI="mongodb+srv://intern:intern123@cluster0.fwks7wf.mongodb.net/Boat?retryWrites=true&w=majority"
app.config["MONGODB_HOST"]=DB_URI
db=MongoEngine()
db.init_app(app)

#to create collection intern create class that inherits the document
class boat_service(db.Document): #write the fields that can be put inside this collections
    boat_id=db.IntField()
    customer_name=db.StringField()
    service=db.StringField()
    payment=db.IntField()
    
    def to_json(self):#this is used to convert all the data into json format
        return{
            "boat_id":self.boat_id,
            "customer_name":self.customer_name,
            "service":self.service,
            "payment":self.payment
    
        }
#to add records:
@app.route("/",methods=["POST"])
def add_record():
     document=json.loads(request.data) #get the data the userr has inserted,it will be in json format convert it into string format
     #to insert this into mongodb
     i=boat_service(boat_id=int(document["boat_id"]),customer_name=document["customer_name"],service=document["service"],payment=int(document["payment"])) #same as class name,an object of class intern is created
     i.save()#to get saved inside mongodb
     return jsonify(i.to_json())

#to Update records:
@app.route("/",methods=["PUT"])
def update_record():
     document=json.loads(request.data) #get the data the userr has inserted,it will be in json format convert it into string format
    #to insert this into mongodb
     i=boat_service.objects(boat_id=document["boat_id"])
      #same as class name,an object of class intern is created
      #check if document exists!
     if not i:
       return jsonify("Error in the data")
     else:
         i.update(customer_name=document["customer_name"])
         i.update(service=document["service"])
         i.update(payment=document["payment"])
         

     return jsonify(i.to_json())

#to DELETE the document:
@app.route("/",methods=["DELETE"])
def delete_record():
     document=json.loads(request.data) #get the data the userr has inserted,it will be in json format convert it into string format
    #to insert this into mongodb
     i=boat_service.objects(boat_id=document["boat_id"])
      #same as class name,an object of class intern is created
      #check if document exists!
     if not i:
       return jsonify("Error in the data")
     else:
       i.delete()
     return jsonify("Document Deleted Successfully")

#To search for a specific data:
@app.route("/",methods=["GET"])
def find_record():
     boat_id=request.args.get("boat_id")#get the data the userr has inserted,it will be in json format convert it into string format
    #to insert this into mongodb
     i=boat_service.objects(boat_id=boat_id)#here first usn in user entered data
      #same as class name,an object of class intern is created
      #check if document exists!
     if not i:
       return jsonify("Error in the data")
     else:
       return jsonify(i.to_json())
     
#for Add Front-end:
@app.route("/add",methods=["GET","POST"])
def add():
    if request.method=="GET":
        return render_template("add.html")
    else:
        boat_id=request.form["boat_id"]
        custumer_id=request.form["customer_id"]
        service=request.form["service"]
        payment=request.form["payment"]
        
        #construct the data to be sent as a dictionary
        x={
            "boat_id": boat_id,
            "customer_id":custumer_id,
            "service":service,
            "payment":payment
        
        }
        #convert dictionary to json using dumps and vise-versa using loads
        x=json.dumps(x)
        #calling api using python
        response=requests.post(url="http://127.0.0.1:5000/",data=x)
        return response.text
    
#for Updating Front-end:
@app.route("/update",methods=["GET","POST"])
def update():
    if request.method=="GET":
        return render_template("update.html")
    else:
        boat_id=request.form["boat_id"]
        custumer_id=request.form["customer_id"]
        service=request.form["service"]
        payment=request.form["payment"]
        
        #construct the data to be sent as a dictionary
        x={
            "boat_id": boat_id,
            "customer_id":custumer_id,
            "service":service,
            "payment":payment
        
        }
        #convert dictionary to json using dumps and vise-versa using loads
        x=json.dumps(x)
        #calling api using python
        response=requests.put(url="http://127.0.0.1:5000/",data=x)
        return response.text
    
#for Deleting Front-end:
@app.route("/delete",methods=["GET","POST"])
def delete():
    if request.method=="GET":
        return render_template("delete.html")
    else:
        boat_id=request.form["boat_id"]#first usn is variable name 2nd usn in[] is naem in html
       
        #construct the data to be sent as a dictionary
        x={
            "boat_id": boat_id
        }
        #convert dictionary to json using dumps and vise-versa using loads
        x=json.dumps(x)
        #calling api using python
        response=requests.delete(url="http://127.0.0.1:5000/",data=x)
        return response.text
    
#for Searching Front-end:
@app.route("/find",methods=["GET","POST"])
def find():
    if request.method=="GET":
        return render_template("find.html")
    else:
        boat_id=request.form["boat_id"]#first usn is variable name 2nd usn in[] is naem in html

        #calling api using python
        response=requests.get(url="http://127.0.0.1:5000/",params={"boat_id": boat_id})
        i=json.loads(response.json())
        str1='''<table border><tr><th>boat_id</th><th>customer_name</th><th>service</th><th>payment</th></tr>'''
        for x in i:
            str1+='''
            <tr>
            <td>'''+str(x["boat_id"])+"</td>"+"<td>"+x["costmer_name"]+"</td>"+"<td>"+x["service"]+"</td>"+"<td>"+str(x["paymenrt"])+"</td>"+"</tr>"
        return str1
            

if __name__=="__main__":
    app.run(debug=False)



