from app import db, ma
from sqlalchemy.dialects.mysql import LONGTEXT, DOUBLE
import datetime

class Users(db.Model):

    
    userID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.BLOB)
    salt = db.Column(db.BLOB)
    LiveChats = db.relationship('LiveChat',backref='users',lazy=True)
    MovieReview = db.relationship('MovieReview', backref ='users',lazy = True)
    
    def __repr__(self):
        return "<Users( userID = '%s',username='%s', email='%s', password='%s', salt=%s)>" % (
                        self.userID,
                        self.username, 
                        self.email, 
                        self.password,
                        self.salt)
    


    
class Movies (db.Model):
    __tablename__ ='movies'
    
    MovieID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(500))
    Year = db.Column(db.Integer)
    Certification = db.Column(db.String(45))
    Release_date = db.Column(db.String(50))
    Runtime = db.Column(db.String())
    Genres = db.Column(db.String(1000)) 
    Directors = db.Column(db.String(1000)) 
    Writers = db.Column(db.String(1000)) 
    Actors = db.Column(db.String(1000)) 
    Synopsis = db.Column(db.String(5000)) 
    Languages = db.Column(db.String(500)) 
    Country = db.Column(db.String(70)) 
    Awards = db.Column(db.String(500)) 
    Poster_URL = db.Column(db.String(1000)) 
    IMDBRating = db.Column (db.Float) 
    MetaScore =db.Column(db.Float) 
    Type = db.Column(db.String(50)) 
    DVD =db.Column(db.String(50))
    Website = db.Column(db.String(500))
    ImdbID = db.Column (db.String(30))
    Reviews = db.relationship('MovieReview',backref='movies',lazy=True)
    
    def  __repr__(self):
        return "<Movies (Title='%s',Year='%s',Certification='%s',Release_date='%s',Runtime='%s',Genres='%s',Directors='%s',Writers='%s', Actors='%s', Synopsis='%s', languages='%s', Country='%s',Awards='%s',Poster_URL='%s',IMDBRating='%s', MetaScore='%s',Type='%s',DVD='%s',Website='%s', ImdbID = '%s')>" % (
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
                self.Languages,
                self.Country,
                self.Awards,
                self.Poster_URL,
                self.IMDBRating,
                self.MetaScore,
                self.Type,
                self.DVD,
                self.Website,
                self.ImdbID 
                )
                
class MovieReview(db.Model):
    __tablename__ = 'moviereview'
    ReviewID = db.Column(db.Integer, primary_key=True, autoincrement = True)
    MovieID = db.Column(db.Integer, db.ForeignKey("movies.MovieID"), nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey("users.userID"), nullable=False)
    Score = db.Column(db.Integer, nullable=False)
    Review = db.Column(db.String(5000), nullable=False)
    DatePosted= db.Column(db.DateTime, nullable = False, default=datetime.datetime.utcnow)
    

    def __repr__ (self):
        return "<Reviews (ReviewID = %i, MovieID = %i, UserID= %i, Score= %i, Review='%s', DatePosted = '%s')>" %(
        self.ReviewID,
        self.MovieID,
        self.UserID,
        self.Score,
        self.Review,
        self.DatePosted)
    


class LiveChat(db.Model):
    
    __tablename__= 'livechat'
    
    MsgTime = db.Column(db.DateTime)
    UserID = db.Column(db.Integer, db.ForeignKey("users.userID"), nullable= False)
    ChatMsg =db.Column(db.String, nullable = False)
    msgID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    
    def __repr__(self):
        return"<LiveChat(MsgTime = '%s', UserID, %i, Chatmsg = '%s')>" %(
    self.MsgTime,
    self.UserID,
    self.ChatMsg
    )
    
class Games(db.Model):
    __tablename__ = 'games'
    
    gameID = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(500), nullable = False)
    release_date = db.Column(db.DateTime, nullable = False)
    gb_guid = db.Column(db.String,nullable=False)
    game_rating = db.Column(db.String, nullable = True)
    platforms = db.Column(db.String, nullable = True)
    game_summary = db.Column(db.String, nullable = False)
    date_added = db.Column(db.DateTime, nullable = False)
    last_updated = db.Column(db.DateTime, nullable = True)
    description = db.Column(db.String, nullable = False)
    dlc = db.Column(db.String, nullable = False)
    genres = db.Column(db.String, nullable = True)
    developers = db.Column(db.String, nullable = True)
    publishers = db.Column(db.String, nullable = True)
    aggregateScore= db.Column(DOUBLE, nullable=True)
    number_reviews= db.Column(db.Integer, nullable =True)
    image_url =db.Column(db.String, nullable = True)
    giantbomb_url = db.Column(db.String, nullable = False)
    
    
    
    def __repr__(self):
        return "<games(name = '%s',release_date = '%s',gb_guid = '%s',game_rating = '%s',platforms ='%s',summary = '%s',date_added = '%s',last_updated = '%s',description = '%s',dlc = '%s',genres = '%s',developers = '%s', publishers ='%s',aggregateScore= %f, number_reviews=%i, image_url = '%s')>" %(
                self.name,
                self.release_date,
                self.gb_guid,
                self.game_rating,
                self.platforms,
                self.game_summary,
                self.date_added,
                self.last_updated,
                self.description,
                self.dlc,
                self.genres,
                self.developers,
                self.publishers,
                self.aggregateScore,
                self.number_reviews,
                self.image_url)
    
    
#Schemas
class UserSchema (ma.ModelSchema):
    class Meta:
        model = Users
        fields = ('username', 'email')   
    
class MoviesSumSchema(ma.ModelSchema):
    class Meta:
        model = Movies 
        fields= ('MovieID','Title', 'Year', 'ImdbID', 'Poster_URL', 'Type')
        
class AllMovsSchema(ma.ModelSchema):
    class Meta:
        model = Movies
        
class gameSummarySchema(ma.ModelSchema):
    class Meta:
        model = Games
        fields = ('gameid','name', 'release_date', 'summary', 'image_url')