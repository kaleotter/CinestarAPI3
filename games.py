# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from app import db, ma, json, models, helpers
import urllib3

class GBAPI:
    def apiConnection(self,remoteResourcePath,**kwargs):
        http = urllib3.PoolManager()
        
        apiKey = 'f23f99074aad79c28e3c4fad5f0b03f9ebe227dd'
        
        fields = {'api_key':apiKey, **kwargs}
        
        uri = 'http://giantbond.com/api/' %(remoteResourcePath)
        
        try:
            r= http.request(
                'GET', 
                MovUrl,
                fields = fields)
            
            
            if r.status == 200:       #we have valid data
                returndata = {"status": True, "data": json.loads(r.data.decode('utf8'))}
                
            else:
                returndata = {"status": False, "data": r.statuscode}
                
            
        except Exception as e:
        
            returndata = {"status":False, "data":"There was a problem with urllib3 %s" % (e)}
            return returndata
        
        return returndata
    
    def gameSummaries(self, searchargs):
        
        #expected structure of searchargs
        #{"title" titlename,"year": year_of_release} Keep search terms simple. 
        
        #construct fields here
        uri = 'games/'
        
        
        
        #so first we should call the api to get data back
        conn = GBAPI()
        
        #Work out filterstring
        filterstring ='name:%s'%(searchargs['name'])
        if 'year' in searchargs.keys() and helpers.checkYear(searchargs.keys['year']):
            filterstring += ',original_release_date:%i'%(searchargs['year'])
        
        data = conn.apiConnection(uri,
        filter = filterstring,
        field_list='name,original_release_date, image')
        
        print (data)
        return("nothing to see here boys")
        
        