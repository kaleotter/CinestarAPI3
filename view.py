# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from flask import Flask, request, Response
from requests import put, get
from flask_restful import Resource, Api, abort, fields, marshal_with, reqparse 
import json
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser
from flask_jsonpify import jsonify

from app import app


#internal modules
import userView
import MovieView 
import Messages
import games


api = Api(app)

class Movies(Resource):
    def get(self):
        query = conn.execute("SELECT * FROM Movies")
        result = {'data': [dict(zip(tuple (query.keys()),i)) for i in query.cursor]}
        # dict() builds an key data referenced array? Sorta like a pk in a database? See https://docs.python.org/2/tutorial/datastructures.html 5.5)
        # zip() not quite sure I understand this. Ask Typh for help? https://docs.python.org/3.3/library/functions.html#zip
        # tuple() like a list but non dynamic. Can't add or remove without rebuilding it from scratch? http://www.tutorialspoint.com/python/tuple_tuple.htm
        return jsonify(result)
#        return {'movieID':[i[0] for i in query.cursor.fetchall()]}
    
   



class MovieSearch (Resource):
    args={"title": fields.Str(required=True, location='json' ),
        "year": fields.Int(required=False, missing= None, location = 'json')}    
    
    @use_kwargs(args)
    def post (self, title, year):
        
        
        #expected json values for this request
        #title, actor, sort           
            
            returncode = 418
            returndata = 'if you see this then something went wrong. Are you a teacup?'
            
            search= MovieView.GetMovie()
            result= search.summaries(title, year)
            print ("we tried searching")
            status_code = result['status']
            print (status_code)

            if status_code == 0:  #nothing found. abort and give a 404. Client should then proceed to make a get request. 
                

                returndata = {"Message":"no results found"}
                returncode = 404
                
            if status_code == 1: #Everything Went fine
                returncode = 200
                returndata = result['data']
            
            if status_code ==4: #we caught an unexpected error
                returncode=400
                returndata = result['data']
            
            return returndata, returncode


class MovieAddSum(Resource):
    def put (self):
        
        #Json expects only "title"
        json_data = request.get_json(force=True) or 404
        
        search = MovieView.OMDB()
        data = search.summaries(json_data)
        responsecode = 418
        responsemsg = "Something totally unexpected went wrong. Are you a teacup?"
        print (data)
            
        if data['status'] == 1: #search completes successfully
            
            responsemsg = data['data']
            responsecode = 200
            
        elif data['status']== 2: #there was a problem contacting the OMBD API 
        
            responsemsg = "for some reson we could not contact OMDB for data. please try your request again" 
            print (data['data'])
            responsecode = 500
            
        elif data['status']== 3: #there was a problem with the database
        
            responsemsg = "There was a problem connecting to the database. Please try your request again"
            print (data['data'])
            responsecode = 503
 
        return responsemsg, responsecode
    
class MovieAdd (Resource):
    def put (self, movie_id):
        
        Movies = MovieView.OMDB()
        data = Movies.update(movie_id)
        responsecode = 418
        responsemessage = "something totally unexpected went wrong. Are you a teacup?"
        
        if data['status'] == 0: #then we found nothing
        
            responsecode = 404
            responsemessage = "No movie exists with that ID"
        elif data['status'] == 1: #then we found something
            
            responsecode =200
            responsemessage = "Movie details added"
        
        elif data['status'] == 2: #then the connection to the API went wrong
            responsecode = 500
            print (data['data'])
            responsemessage = "for some reson we could not contact OMDB for data. please try your request again"
            
        elif data['status']== 3: #Then something went wrong with the database
            responsecode = 503
            print (data['data'])
            responsemessage = "Our connection to the database failed for some reason, please try again."
            
        return responsemessage, responsecode
    
class MovieID(Resource):
    def get(self, movie_id):
        returndata = {"message":"Something seems to have gone terribly, terribly wrong. Are you a teacup?"}
        returncode = 418
        
        Movie = MovieView.GetMovie()
        data = Movie.details(movie_id)
        
        if data['status'] == 0: #File not found
            
            returndata = {"We could not find a movie with this id"}
            returncode = 404
            
        elif data['status'] == 1: #We found a movie. Display it
            returndata = data['data']
            returncode = 200
        elif data['status'] ==3: #There was a problem with the database
            returndata = data['data']
            returncode = 400
            
        return returndata, returncode
        
class MovieReviews(Resource):
    def get(self, movie_id):
        response = Response({"Something appears to have gone horribly wrong, are you a teacup?"},418, mimetype = 'application/json')
        
        reviews = MovieView.Reviews()
        data = reviews.forMovie(movie_id)
        print ("we got data")
        
        if data:    #if data is not empty
            print (data)
            response = data
            
            
        return response
    
    def post(self,movie_id):
        response = jsonify({'message':'something appears to have gone wrong. Are you a teacup?'})
        response.statuscode = 418 
        
        json_data = request.get_json(force = True)
        reviews = MovieView.Reviews()
        data = reviews.postNew(movie_id,json_data)
        if data: 
            response = data
        
        
        return response
        
        
        

class LiveChat(Resource):
    
    def get(self):
        response_code= 418
        response_message ="something has gone terribly wrong, are you a teacup?"
        messages = Messages.LiveChat()#
        print("tried to intantiate lc")
        data = messages.getMessages()
        print("we made the call")
        
        if data['status']==0:
            response_code = 200
            response_message = data['message']
        
        print (data)
        return response_message, response_code



class Users (Resource):
    args={'username': fields.String(required=True, location = 'form'),
        'email': fields.String(Required=True, location = 'form'),
        'password':fields.String(Required=True, location = 'form')}
    
    @use_kwargs(args)    
    def post(self, username, email, password):                #create an acccount
    
        inputData = {"username": username, "email":email,"password":password}
        output = userView.createNewUser(inputData)
        
        
        return(output)

class Profile (Resource):
    #args = { 'u': fields.String(required=True)}

    #@use_kwargs(args)
    def get (self,usr_ID):
        
        #get user data
        data = userView.getUser(usr_ID)
        responseData = {"Message":"something went terribly wrong and may be beyond our control. You are probably a teacup"}
        responseCode = 418        #I'm a little teapot short and stout
        statusCode = data["status"]
        
        #if no user found
        if statusCode == 1:
            responseData= {"message":"No user profile found with that ID"}
            responseCode =404
            
        elif statusCode ==0:
            responseData = data["data"]
            responseCode= 200
            

        return Response (responseData, status =responseCode, mimetype = 'application/json') 
            
class Login (Resource):
    def post (self):

        json_data = request.get_json(force=True)
        
        response_data = userView.doLogin(json_data)
        status = response_data["Status"]
        
        if status == 2:
            print ("we got to an invalid user/pass")


            return response_data['data'], 403
        else:
            print ("we got to a valid user/pass")
            return jsonify(response_data['data'])


class gameSummaries(Resource):
    
    args={"title":fields.Str(required = True),
        "year": fields.Int(required = False)
    
    }
    @use_kwargs(args)
    def get(self, title, year):
        summaries = games.GBAPI()
        data = summaries.gameSummaries({"name":title})
        
        print('aaaaaaaaa')
        return {'aaaaaaaaaa'}
        


#movie routes
api.add_resource(Movies, '/movies')
api.add_resource(MovieID, '/movies/<int:movie_id>', endpoint='movie_id')
api.add_resource(MovieReviews, '/movies/<int:movie_id>/reviews')
api.add_resource(MovieSearch, '/movies/search')
api.add_resource(MovieAddSum, '/movies/summaries')
api.add_resource(MovieAdd, '/movies/add')

#user routes
api.add_resource(Users, '/users')
api.add_resource(Profile, '/users/<int:usr_ID>')
api.add_resource(Login, '/users/login')
api.add_resource(LiveChat,'/chat')

#game routes
api.add_resource(gameSummaries, '/games/summaries')