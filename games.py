# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from app import db, ma, json, models, helpers, jsonify
import certifi
import urllib3
from urllib.parse import urlencode


class GBAPI:
    def apiConnection(self,remoteResourcePath,apiFields, filters, offset =False, ):
        http = urllib3.PoolManager(cert_reqs ='CERT_REQUIRED',
                                    ca_certs=certifi.where())
        print (remoteResourcePath)
        
        apiFields=urlencode({'field_list':apiFields})
        filters=urlencode ({'filter':filters})        
        #key to access the api
        apiKey = 'f23f99074aad79c28e3c4fad5f0b03f9ebe227dd'
        
        #format incoming data as json, expand fields as nessecary.
        #TODO: add additional logic if nessescary.
        
        uri = 'https://www.giantbomb.com/api/'+ remoteResourcePath + '?api_key=%s&format=json' % (apiKey) \
        +'&%s' % (filters)\
        +'&%s' %(apiFields)
        
        if offset != False:
            offset = urlencode({'offset':offset})
            uri + '&%s' %(offset)
            
            
        try:
            r= http.request(
                'GET', 
                uri,
                headers = {"User-Agent": 'Flask-Restful API'})
            
            
            if r.status == 200:       #we have valid data
                returndata = {"status": True, "data": json.loads(r.data.decode('utf8'))}
                
            else:
                print (r.data)
                returndata = {"status": False, "data": r.status}
                
            
        except Exception as e:
        
            returndata = {"status":False, "data":"There was a problem with urllib3 %s" % (e)}
            return returndata
        
        return returndata
    
    def gameSummaries(self, searchargs):
        
        #expected structure of searchargs
        #{"title" titlename,"year": year_of_release} Keep search terms simple. 
        
        #construct fields here
        uri = 'games'
        
        
        
        #so first we should call the api to get data back
        conn = GBAPI()
        
        #Work out filters and search fields
        
        #filters
        filterlist ='name:%s'%(searchargs['name'])
        fields ='name,original_release_date,original_game_rating,site_detail_url,image,deck,site_detail_url,platforms,guid'
        if 'year' in searchargs.keys() and helpers.checkYear(searchargs.keys['year']):
            filterlist + ',original_release_date:%i'%(searchargs['year'])
            
        
        data = conn.apiConnection(uri,
        fields, filterlist)
        
        #extract the data
        data = data['data']
        
        data_check = conn.checkStatus(data['error'])
        
        #check if json has results
        if data["number_of_page_results"] ==0:
            
            response = jsonify ({"message":"we could not find further results on giantbomb.com"})
            response.status_code = 404
            
            
        
        
        
        if not data_check["isOkay"]:
            #if the data is not correctly formed return a 500 code
            response = jsonify ({"Message":"something went wrong with the format to the remote api: %s"})
            response.status_code = 500
            return response
        
        #Now we know that the data is good we can loop through it
        newgame = models.Games()
        summarycount = 0
        
        for game in data['results']:
            newgame.name = game['name']
            newgame.release_date = game['original_release_date']
            newgame.gb_guid = game['guid']
            newgame.game_summary = game['deck']
            newgame.image_url = game['image']['medium_url']
            newgame.giantbomb_url = game['site_detail_url']
            
            
        
            #for fields that return list values, that we also want a set of specific values from:
            
            ###ratings###
            
            ratinglist = ""
            for rating in game['original_game_rating']:
                ratinglist + "%s," %(rating['name'])
                
            #slice the string to remove the trailing whitespace and comma
            #add compiled list to the new dbobject
            newgame.rating = ratinglist[:-3]
            
            
            
            
            ###platforms###
            platform_list = ""
            for platform in game['platforms']:
                platform_list + "%s, " %(platform['name'])
            
            #slice the string to remove the trailing whitespace and comma and
            #add the string to the new dbobject
            newgame.platforms= platform_list[:-3]
            
            db.session.add(newgame)
            summarycount + 1
        
        try:
            db.session.commit()
            response = jsonify ({"we added %i new game summaries" %(summarycount)})
        
        except Exception as e: 
            
            print (e)
            response =jsonify({"message": 'database error'})
            response.status_code = 500
        
        
        return response
        
    
    def checkStatus (self, data):
    #Simple check of the data in Json,     
        if data == "OK":
            #data should be fine.
            return {'isOkay':True, "msg":"none"}
        else: 
            #There was something wrong with the request, but it went through 
            #successfully. Return false and print to log.
            
            #TODO: Impliment logging. Use print for debugging
            print(data)
            
              
            return {'isOkay':True, "msg":data}
        

        