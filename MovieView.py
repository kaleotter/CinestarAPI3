import json
import urllib3  

from app import db, ma, models, jsonify
#return status codes
#0: no match found
#1: Completed Successfully
#2: Problem with OMDB link
#3: Problem with Database 
#4: General Exception
#5:
#6:

class GetMovie:
    
        
    def summaries(self, searchTitle, searchYear):
        
        

        print ("we started movSearch")     
        
        print ("the movie bieng searched : %s" %(searchTitle))

        #first, check if anything even similar exists in the db. 
        try:
                
            #initialize the query
            q = db.session.query(models.Movies)
            
            #as title is always mandatory for our search, the filter should always try to match on title
            filterQ=[db.func.lower(models.Movies.Title).contains(db.func.lower(searchTitle))]
            
            #optional search parameters go here. 
            if searchYear is not None or '':
                filterQ.append(models.Movies.Year.contains(searchYear))
            
            queryResult = q.filter(*filterQ).all()
            
            #use the schema to filter the result down to the summary fields 
            schema = models.MoviesSumSchema(many=True)
            result = schema.dump(queryResult)
            

            if result.data:
                
                print ("attempting to print results")

                print (result.data)
                returnmessage = {'status':1, 'data': {"summary": result.data}}
                
            else:   #we got no data back
                returnmessage = {'status': 0 , 'data': "no results found for the presented parameters"}

        except Exception as e:
            print ("something went very wrong")
            print (e)
            return {"status":2, "data": e}
        
        return returnmessage

 
    def details(self, movID): 
        try: 
            if models.Movies.query(db.exists()\
         .where(models.Movies.MovieID == movID)).scalar():
             
                query = models.Movies.query.filter(Movies.MovieID == movID)
            
                schema= models.AllMovsSchema()
            
                returnmessage = {'status': 1, 'data': schema.dump(query)} 
            
            else:
                #we didn't find anything
                
                returnmessage ={'status': 0, 'data': ""}
        
        except Exception as e:
            #something went wrong with the database interaction
            
            return {'status':3, 'data': "The following error occured trying to access the database: %s" %(e)}
        
        return returnmessage


class OMDB ():
    
    
    apiKey = '36d82221'
    
    def accessAPI(self, arguments):
        
        MovUrl = 'http://www.omdbapi.com/'
        http = urllib3.PoolManager()
        
        
        
        try:
            r= http.request(
                'GET', 
                MovUrl,
                fields = arguments)
            returndata = json.loads(r.data.decode('utf8'))
            print (returndata)
            
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
        
        
                mData = self.accessAPI({"apikey": self.apiKey, "i": titleID.ImdbID, "type":"movie"})
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
    
    def summaries (self, data):
        

        mData = self.accessAPI({"apikey": self.apiKey, "s": data['title'], "type":"movie"}) 
        #check that our data is valid.
        if "Search" not in mData.keys():
            responsedata = {"status": 2, "data": mData}
            
            return (responsedata)
            
        else:
            dataList= mData['Search']
            itemsAdded = 0  
            for elem in dataList: 
                
                print (elem)
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
    
class Reviews:
        
    def forMovie(self, movID):
        print (movID)
            
        try:
            if db.session.query(db.exists().
            where(models.MovieReview.MovieID == movID)).scalar():

                q= db.session.query(models.MovieReview.ReviewID,
                                models.Users.username, 
                                models.MovieReview.MovieID, 
                                models.MovieReview.Score, 
                                models.MovieReview.Review,
                                models.MovieReview.DatePosted).\
                                join(models.Users).\
                                join(models.Movies).\
                                filter(models.MovieReview.MovieID == movID).all()

        
                dict_for_json= {'reviews':[]}
            
                for r  in q: #for each review in the list returned above
                    reviewdict ={"ID": r.ReviewID, "username": r.username, "movieID":r.MovieID, "score": r.Score, "review": r.Review, "dateposted":r.DatePosted}
                    print (reviewdict)
                    dict_for_json['reviews'].append(reviewdict)
            
            
            
                result =jsonify(dict_for_json)
                result.status_code = 200
            
        
            else: #no match for this movieID 
            
                result = jsonify("The requested resource was not found")
                result.status_code = 404
            
            return result
        
        except Exception as e:
            #something went wrong trying to contact the database
            result = jsonify("there was an error connecting to the database: %s" %(e))
            result.status_code = 503
            #write something to the log here
            
            return result
        
        
    def single(self, movID,revID):
            
        return result
    
    def allReviews(self):
            
        return result
    def post (self, userID, reviewData):
        return result