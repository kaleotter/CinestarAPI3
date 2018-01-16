# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from app import db, ma, models
from datetime import datetime, timedelta


class LiveChat():

    def writeMessage(self,user_id,message):
        new_chatMsg = models.LiveChat(
        UserID = user_id,
        ChatMessage = message
        )
    
        try: 
            db.session.add(new_chatMsg)
            db.session.commit()
        
        except Exception as e: 
            return {'status':1, 'data':"Problem connecting to database: %s" %(e)}
    
        return{'status':0,'data':'message saved successfully'}
    
    def getMessages(self):
        currentTime = datetime.utcnow()
        
        
        try: 
            q=db.session.query(models.LiveChat.MsgTime, models.Users.username, models.LiveChat.ChatMsg).join(models.Users)\
            .filter(models.LiveChat.MsgTime >= currentTime - timedelta(minutes=5))
        
            print ("we accessed the db")
        except Exception as e:
            return {'status':1, 'data':"there was a problem connecting to the database: %s" % (e)}
    
        e = q.all()
        print (e)
        mergemsg =[]
        print (" got data. looping now")
        for MsgTime, username, ChatMsg in e:
            msgDict={'time': MsgTime.__str__(), 'user':username,'ChatMsg':ChatMsg}
            print (msgDict)
            mergemsg.append(msgDict)
            
        
        message={"messages":mergemsg}
        
        print (message)
        
        
        return{'status':0,'message':message}
        
        
