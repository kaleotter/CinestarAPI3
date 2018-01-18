# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from app import db, ma, json, models, helpers
import certifi
import urllib3
from urllib.parse import urlencode


class GBAPI:
    def apiConnection(self,remoteResourcePath,apiFields, filters):
        http = urllib3.PoolManager()
        print (remoteResourcePath)
        
        apiFields=urlencode({'field_list':apiFields})
        filters=urlencode ({'filter':filters})        
        #key to access the api
        apiKey = 'f23f99074aad79c28e3c4fad5f0b03f9ebe227dd'
        
        #format incoming data as json, expand fields as nessecary.
        #TODO: add additional logic if nessescary.
        
        uri = 'http://www.giantbomb.com/api/'+ remoteResourcePath + '?api_key=%s&format=json' % (apiKey) \
        +'&filter=%s' % (filters)\
        +'&field_list=%s' %(apiFields)
        
        print (uri)                                 
        
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
        filterlist ='name:%s'%(searchargs['name'])
        fields ='name,original_release_date,original_game_rating,site_detail_url,image'
        if 'year' in searchargs.keys() and helpers.checkYear(searchargs.keys['year']):
            filterlist + ',original_release_date:%i'%(searchargs['year'])
        
        print (fields)
        print (filterlist)
        
    
        
        data = conn.apiConnection(uri,
        fields, filterlist)
        
        print (data)
        return("nothing to see here boys")
        
        