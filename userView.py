# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

#Imports
from json import *
from flask_jsonpify import jsonify
import bcrypt

#Local Modules
from app import db, ma, models


def createNewUser(jsondata):  
        
    user = jsondata['username']
    email = jsondata['email']
    pw =  jsondata['password']
        
    #first check if account with user unique
    if (db.session.query(db.exists().where(models.Users.email == email)).scalar()):
        return jsonify({"Message":"An account with this email already exists!"})
        
    #then check to see if username is unique
    if (db.session.query(db.exists().where(models.Users.username == user)).scalar()):
        return jsonify({"Message":"An account with this username azlready exists!"})
        
    #we can then prepare to create the account
        
    #first hash the password using bcrypt
    pw_salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw.encode('utf8'),pw_salt)

    new_user = models.Users(username = user, email = email, password = hashed, salt = pw_salt)
    db.session.add(new_user)
    db.session.commit()
        
    return jsonify({"Message":"Account created successfully! You Can now Log in"})


def doLogin(json_data):
    
    user_name=json_data["username"]
    print (user_name)
    password_raw=json_data["password"]
    print (password_raw)
    returndata={"status":"999", "data":"nothing"}
    
    
    #First Work out if the user exists
    if (db.session.query(db.exists().where(models.Users.username == user_name)).scalar()):
        
        print ("User Found")
        #We know the user Exists, so now we can check thier password
        for instance in db.session.query(models.Users).\
                              filter_by(username = user_name): 

            if bcrypt.checkpw(password_raw.encode('utf8'),instance.password):
                #password is correct so we can return a user id.
                
                returndata= {"Status": 1, "data":{"UserID":instance.userID}}
                

            else: 
                print ("pwd was wrong")
                returndata= {"Status": 2, "data": {"message":"Invalid username or password"}}
        
    else:
        print("username was wrong")
        returndata= {"Status": 2,"data": {"message":"Invalid username or password"}}
    
    return returndata

def getUser (u):

    #session = Session()
    returndata = {"status":2}
    if db.session.query(exists().where(models.Users.userID==u)).scalar():

        print ("we found a user")

        Users_Schema = models.UserSchema(many=True)
        
        all_users = db.session.query(models.Users).all()
        result = Users_Schema.dump(all_users)
        
        resultData = jsonify(result.data)
        
        
        #print ('we tried to jsonify: ')
        #print (jsonData)
        
        returndata = {"status":0, "data": resultData}
        

    else:
            
        returndata = {"status": 1, "data":""}
    
    print (returndata["status"])
    return (returndata) 
    
    
    
