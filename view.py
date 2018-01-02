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
        'a': fields.String(required=False, missing='', location ='query'),                #optionally we need an actor name
        'order': fields.Integer(required=False, missing=0, location = 'query'),
        'sort':     fields.String (required=False, missing ='ascending', location = 'query')        #we need to know how the user wants the data sorted
        }        
    @use_kwargs(mov_search_args)
    def get (self, m, a, order, sort):

            result = 'if you see this then something went wrong'
            
            search_result = MovieView.movSearch({"movie":m, "actor":a, "orderBy": order, "sort": sort})
            status_code = search_result['status']
            print (status_code)

            if status_code == '0':  #nothing found. abort and give a 404. Client should then proceed to make a get request. 
                print ('nothing found')

                result = ({"Message":"no results found for %s" %(m)})
                returncode = 404
            
            return result, returncode

    @use_kwargs(mov_search_args)
    def post (self, m, a, order, sort):
            

            data = MovieView.newMov({'m': m},"c")
            
            
                
                

            return ('not done yet')
    
class MovieId (Resource):
    def get (self,id):
        
        #we're going to display a movie
        
        return ("not done yet")
        
        

    class  (Resource):
        
        def put 

    class MovieReviews(Resource):
        def get(self,MovId):
            
            return jsonify(result)
        





class Users (Resource):

    def post(self):                #create an acccount
    
        json_data = request.get_json(force=True)
        output = userView.createNewUser(json_data)
        
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

class UpdateMovie(Resource): #Updates a movie with all relevant data
class AddSummary(Resource): #Adds summary data for new movie searches
    
    def put (self, movie_ID):
        
        return ("Im not done yet")
        

api.add_resource(Movies, '/movies')
api.add_resource(MovieId, '/movies/<int:movie_ID>')
api.add_resource(UpdateMovie, '/movies/<int:movie_ID/update')
api.add_resource(AddMov, 'movies/summaries')
api.add_resource(MovieSearch, '/movies/search', endpoint='search')
api.add_resource(Users, '/users')
api.add_resource(Profile, '/users/<int:usr_ID>')
api.add_resource(Login, '/users/login')
    

