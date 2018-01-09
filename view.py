# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from flask import Flask, request, Response
from requests import put, get
from flask_restful import Resource, Api, abort, fields, marshal_with, reqparse 
from json import dumps
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser
from flask_jsonpify import jsonify

from app import app


#internal modules
import userView
import MovieView 


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
#parameters for the movie search
    mov_search_args = {
        'm': fields.String(required=True, location = 'query'),         #we always need a movie name
        'a': fields.String(required=False, location ='query'),                #optionally we need an actor name
        'order': fields.Integer(required=False, location = 'query'),
        'sort':fields.String (required=False, location = 'query')        #we need to know how the user wants the data sorted
        }        
    @use_kwargs(mov_search_args)
    def get (self, m, a, order, sort):
            returncode = 418
            result = 'if you see this then something went wrong. Are you a teacup?'
            
            search_result = MovieView.getMovies.summaries({"movie":m, "actor":a, "orderBy": order, "sort": sort})
            status_code = search_result['status']
            print (status_code)

            if status_code == '0':  #nothing found. abort and give a 404. Client should then proceed to make a get request. 
                print ('nothing found')

                result = ({"Message":"no results found for %s" %(m)})
                returncode = 404
            
            return result, returncode

    @use_kwargs(mov_search_args)
    def put (self, m,a,order,sort):
    
        
        data = MovieView.OMDB.summaries(m)
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
    
class MovieId (Resource):
    def get (self,movie_id):
        
        #we're going to display a movie
        
        return ("not done yet")
    
    def put (self, movie_id):
        
        data = MovieView.OMDB.update(movie_id)
        responsecode = 418
        responsemessage = "something totally unexpected went wrong. Are you a teacup?"
        
        if data['status'] == 0: #then we found nothing
        
            responsecode = 404
            responsemessage = "No movie exists with that ID"
        if data['status'] == 1: #then we found something
            
            responsecode =200
            responsemessage = "Movie details added"
        
        if data['status'] == 2: #then the connection to the API went wrong
            responsecode = 500
            print (data['data'])
            responsemessage = "for some reson we could not contact OMDB for data. please try your request again"
            
        if data['status']== 3: #Then something went wrong with the database
            responsecode = 503
            print (data['data'])
            responsemessage = "Our connection to the database failed for some reason, please try again."
            
        return responsemessage, responsecode
        
    class MovieReviews(Resource):
        def get(self,MovId):
            
            return jsonify(result)
        





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

#AAAAAAAH I COMMENTED THIS OUT.     
api.add_resource(Movies, '/movies')
api.add_resource(MovieId, '/movies/<movie_id>')
api.add_resource(MovieSearch, '/movies/search', endpoint='search')
api.add_resource(Users, '/users')
api.add_resource(Profile, '/users/<int:usr_ID>')
api.add_resource(Login, '/users/login')