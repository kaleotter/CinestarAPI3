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

def movSearch(queryArgs):

    print ("we started movSearch")
    containsexact=False
    exactmatch={'0'}


    #first, check if anything even similar exists in the db. 

    if db.session.query(exists().where(func.lower(models.Movies.Title.like(func.lower(queryArgs['movie']))))).scalar():
        print ("we found similar")
        similar = db.session.query(db.Movies).filter(func.lower([models.Movies.Title.like(func.lower(queryArgs['movie']))]))

        #check for an exact match
        if db.session.query(exists().where(func.lower(models.Movies.Title)==func.lower(queryArgs['movie']))).scalar():
            containsexact = True
            print ("an exact match was found")
     
            return ({"status":"1"}) 

    else: #we found exactly nothing
        
        return({"status":'0'})

 
    

def newMov(queryArgs):
   
       apiKey= '36d82221'
       MovUrl = 'http://www.omdbapi.com/'
       http = urllib3.PoolManager()
       r= http.request(
           'GET', 
           MovUrl,
           fields = {'apikey':apiKey, 't':queryArgs['m'],'r': 'json'})
       mData = json.loads(r.data.decode('utf8'))
       print (type(mData))
       

                                
    if db.session.query(exists().where(Title == mdata['Title'])):
        #Then we already have either summary or complete data and are probably updating
        modMov = db.session.query(models.Movies)/.
        filter(models.Movies.Title == mData['title']).first()
        
        modMov.Certification = Mdata['Rated']
        modMov.Release_date = ['Released']
        modMov.
            
        return (something)
    else: #we don't have a match, so add the data rather than just update
                 
                 new_movie = models.Movies(
                                Title = mData['Title'],
                                Year = mData['Year'],
                                Certification = mData['Rated'],
                                Release_date = mData['Released'],
                                Runtime= mData['Runtime'],
                                Genres= mData['Genre'],
                                Directors = mData['Director'],
                                Writers = mData['Writer'],
                                Actors= mData['Actors'],
                                Synopsis= mData['Plot'],
                                Languages= mData['Language'],
                                Awards= mData['Awards'],
                                Poster_URL= mData['Poster'],
                                MetaScore= mData['Metascore'],
                                IMDBRating=mData['imdbRating'],
                                Type= mData['Type'],
                                DVD = mData['DVD'],
                                Website= mData['Website'])
        
        db.session.add(new_movie)

       
    return ("deed eet")
