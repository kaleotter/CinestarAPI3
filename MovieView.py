from flask import Flask, json
from flask_restful import abort
from sqlalchemy import create_engine, exists, func
from sqlalchemy.orm import sessionmaker
from json import dumps
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser
from flask_jsonpify import jsonify
import urllib3

from app import db, ma, models

#return status codes
#0: no match found
#1: Completed Successfully
#2: Problem with OMDB link
#3: Problem with Database 
#4:
#5:
#6:

class Search:
    def Search(queryArgs):

        print ("we started movSearch")
        containsexact=False
        exactmatch={'0'}
    

        #first, check if anything even similar exists in the db. 

        if db.session.query(exists().where(func.lower(models.Movies.Title.like(func.lower(queryArgs['movie']))))).scalar():
            print ("we found similar")
            similar = db.session.query(models.Movies).filter(func.lower([models.Movies.Title.like(func.lower(queryArgs['movie']))]))
        
            search_results = models.Mov_S_Schema(similar).jsonify

            #check for an exact match
        if db.session.query(exists().where(func.lower(models.Movies.Title)==func.lower(queryArgs['movie']))).scalar():
            containsexact = True
            print ("an exact match was found")
     
            return ({"status":2}) 

        else: #we found exactly nothing
        
            return({"status":0})

 
    
class OMBD:
    
    apiKey = '36d82221'
    
    def accessAPI(arguments):
        
        MovUrl = 'http://www.omdbapi.com/'
        http = urllib3.PoolManager()
        
        
        
        try:
            r= http.request(
                'GET', 
                MovUrl,
                fields = arguments)
            returndata = json.loads(r.data.decode('utf8'))
            
        except Exception as e:
        
            returndata = {"status":2, "data": e}
        
        return returndata
        
        

    def updateMov(self,id): 
   
        
        
        if db.session.query(exists().where(models.Movies.MovieId==id )):
   
            titleID = session.query(db.models.Movies.ImdbID)\.
            filter(models.Movies.MovieID==id).first
        
        
            mData = accessAPI({"apikey": apiKey, "i": titleID, "type":"movie"})
        
            #check that our data is valid.
            if "Title" not in mData.keys():
                responsedata = {"status": 5, "data": mData}
            
                return (responsedata)    
            
            
            #create the data ready for modification
            modMov = db.session.query(models.Movies)\.
            filter(models.Movies.MovID == id).first()
                
            modMov.Title = mData['Title']
            modMov.Year = mData['year']
            modMov.Certification = mData['Rated']
            modMov.Release_date = mData['Released']
            modMov.Runtime= mData['Runtime']
            modMov.Genres= mData['Genre']
            modMov.Directors = mData['Director']
            modMov.Writers = mData['Writer']
            modMov.Actors= mData['Actors']
            modMov.Synopsis = mData['Plot']
            modMov.Languages = mData['Language']
            modMov.Awards = mData['Awards']
            modMov.Poster_URL= mData['Poster']
            modMov.IMDBRating = mData['imdbRating']
            modMov.MetaScore = mData['MetaScore']
            modMov.Type = mData['Type']
            modMov.DVD = mData['DVD']
            movMod.Website = mData['Website']
        
            returndata = {"status":2, "data": "we successfully updated %s!" %(mData['Title'])}
            
            try:    #Attempt to commit changes to db. If we fail then Raise error and pass it back
                db.commit()
            except Exception as e:
                
                return {"status": 7, "data": e}
            
        else:
    
       #There was no movie at the provided ID
            returndata = {"status":0, "data": "Movie Not found."}
       
        return returndata
    
    def newMovies (self,MovieTitle):
        

        mData = accessAPI({"apikey": apiKey, "i": titleID, "type":"movie"})
        
        #check that our data is valid.
        if "Title" not in mData.keys():
            responsedata = {"status": 0, "data": mData}
            
            return (responsedata)
            
            dataList= mdata['Search']
              
            for elem in datalist: 
        
                new_movie = models.Movies(
                Title = elem['Title'],
                Year = elem['Year'],
                Poster_URL= elem['Poster'],
                Type = elem['Type'],
                ImdbID = elem['imdbID'])
        
                db.session.add(new_movie)
            
            try:
                
                db.session.commit()
                    
            except Exception as e:
                    
                return {"status": 7, "data": e}
                            
        
        returndata = {"status": 1, "data":"Successfully added %s items" %(dataList.len())}
            
        return returndata