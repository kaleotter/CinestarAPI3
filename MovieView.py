import json
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

class getMovies:
    def summaries(queryArgs):
        
        

        print ("we started movSearch")
        containsexact=False
        exactmatch={'0'}
    

        #first, check if anything even similar exists in the db. 
        try:
            if db.session.query(db.exists().where(db.func.lower(models.Movies.Title.like(db.func.lower(queryArgs['movie']))))).scalar():
                print ("we found similar")
                
                similar = db.session.query(models.Movies).filter(db.func.lower([models.Movies.Title.like(db.func.lower(queryArgs['movie']))]))
        
            search_results = models.Mov_S_Schema(similar).jsonify
            
            print (search_results)
            
        except Exception as e:
            print ("something went very wrong")
            print (e)
            return {"status":2, "data": e}

        else: #we found exactly nothing
            print ("nothing found")
            returnmeassage = {"status":0, "data":''}
            
        return returnmessage

 
    
class OMDB:
    
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
            
            print (arguments)
            
        except Exception as e:
        
            returndata = {"status":2, "data": e}
        
        return returndata
        
        

    def update(id): 
   
        
        try:
            
            if db.session.query(db.exists().where(models.Movies.MovieID==id )):
   
                try:
                    titleID =db.session.query(models.Movies)\
                            .filter(models.Movies.MovieID==id).first()
                            
                    print(titleID.ImdbID)        
                except Exception as e:
                    return {"status":3, "data":e}
        
        
                mData = OMDB.accessAPI({"apikey": OMDB.apiKey, "i": titleID.ImdbID, "type":"movie"})
                print (mData)
                
                #check that our data is valid.
                if "Title" not in mData.keys():
                    print ("we found that data was not correct")
                    responsedata = {"status": 5, "data": mData}
            
                    return (responsedata)    
            
            
                #create the data ready for modification
                try:
                    print("trying to run query")
                    modMov = db.session.query(models.Movies)\
                    .filter(models.Movies.MovieID == id).first()
                
                except Exception as e:
                    print ("query failed to run")
                    print(e)
                    return {"status":3, "data":e}
                
                modMov.Title = mData['Title']
                modMov.Year = mData['Year']
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
                modMov.MetaScore = mData['Metascore']
                modMov.Type = mData['Type']
                modMov.DVD = mData['DVD']
                modMov.Website = mData['Website']
        
                
            
                try:    #Attempt to commit changes to db. If we fail then Raise error and pass it back
                    print ("tried to commit modification")
                    #db.session.add(modMov)
                    db.session.commit()
                except Exception as e:
                
                    print ("database commit failed")
                    return {"status": 3, "data": e}
                
                print ("database commit succeeded")
                returndata = {"status":1, "data": "we successfully updated %s!" 
                                                            %(mData['Title'])}
            
            else:
    
            #There was no movie at the provided ID
                print ("no movie at this id")
                returndata = {"status":0, "data": "Movie Not found."}
            
        except Exception as e:
            
            print ("query failed")
            return {"status":3, "data":e}
       
        return returndata
    
    def summaries (movieTitle):
        

        mData = OMDB.accessAPI({"apikey": OMDB.apiKey, "s": movieTitle, "type":"movie"})
        
        #check that our data is valid.
        if "Search" not in mData.keys():
            responsedata = {"status": 2, "data": mData}
            
            return (responsedata)
            
        else:
            dataList= mData['Search']
            itemsAdded = 0  
            for elem in dataList: 
                
                #first check if the movie already exists in db
                if not db.session.query(db.exists().where(models.Movies.ImdbID == elem['imdbID'])).scalar():
        
                    new_movie = models.Movies(
                    Title = elem['Title'],
                    Year = elem['Year'],
                    Poster_URL= elem['Poster'],
                    Type = elem['Type'],
                    ImdbID = elem['imdbID'])
                    
                    itemsAdded +1
        
                    try:    
                        db.session.add(new_movie)
                
                    
                    except Exception as e:
                    
                        return {"status": 3, "data": e}
            
            try:
                db.session.commit()
                
            except Exception as e:
                
                return{"status":3,"data":e}
        
            returndata = {"status": 1, "data":"Successfully added %s items" %(itemsAdded)}
            
        return returndata