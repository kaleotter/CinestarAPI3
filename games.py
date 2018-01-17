# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from app import db, ma, json, models.Games, models.GameReviews

class IGDB:
    def apiconnection(self,uri,data, fields):
        http = urllib3.PoolManager()
        
        
        
        try:
            r= http.request(
                'GET', 
                MovUrl,
                headers= {'user-key': '84d5428dae4aa2f4a83c9fd892c00b2b', 'accept':'application/json'},
                fields = fields)
            response = {"status": True, "data": json.loads(r.data.decode('utf8'))}
            
            if r.status == 200       #we have valid data
                
            
        except Exception as e:
        
            returndata = {"status":True, "data": e}
        
        return returndata