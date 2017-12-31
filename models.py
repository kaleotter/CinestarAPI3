from app import db, ma

class Users(db.Model):

    
    userID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.BLOB)
    salt = db.Column(db.BLOB)
    
    
    def __repr__(self):
        return "<Users( userID = '%s',username='%s', email='%s', password='%s', salt=%s)>" % (
                        self.userID,
                        self.username, 
                        self.email, 
                        self.password,
                        self.salt)
    


    
class Movies (db.Model):
    __tablename__ ='Movies'
    
    MovieID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String)
    Year = db.Column(db.Integer)
    Certification = db.Column(db.String(45))
    Release_date = db.Column(db.DATETIME)
    Runtime = db.Column(db.String())
    Genres = db.Column(db.String(1000)) 
    Directors = db.Column(db.String(1000)) 
    Writers = db.Column(db.String(1000)) 
    Actors = db.Column(db.String(1000)) 
    Synopsis = db.Column(db.String(5000)) 
    languages = db.Column(db.String(500)) 
    Country = db.Column(db.String(70)) 
    Awards = db.Column(db.String(500)) 
    Poster_URL = db.Column(db.String(1000)) 
    IMDBRating = db.Column (db.DECIMAL(1,0)) 
    MetaScore =db.Column(db.DECIMAL(1,0)) 
    Type = db.Column(db.String(50)) 
    DVD =db.Column(db.DATE)
    Website = db.Column(db.String(500))
    
    def  __repr__(self):
        return "<Movies (Title='%s',Year='%s',Certification='%s',Release_date='%s',Runtime='%s',Genres='%s',Directors='%s',Writers='%s', Actors='%s', Synopsis='%s', languages='%s', Country='%s',Awards='%s',Poster_URL='%s',IMDBRating='%s', MetaScore='%s',Type='%s',DVD='%s',Website='%s')>" % (
                self.Title,
                self.Year,
                self.Certification,
                self.Release_date,
                self.Runtime,
                self.Genres,
                self.Directors,
                self.Writers,
                self.Actors,
                self.Synopsis,
                self.languages,
                self.Country,
                self.Awards,
                self.Poster_URL,
                self.IMDBRating,
                self.MetaScore,
                self.Type,
                Self.DVD,
                Self.Website
                )
                

#Schemas
class UserSchema (ma.ModelSchema):
    class Meta:
        model = Users