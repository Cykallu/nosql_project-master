import pymongo
from bson.objectid import ObjectId
from pymongo.server_api import ServerApi
from passlib.hash import pbkdf2_sha256 as sha256
from errors.validation_error import ValidationError
from errors.not_found import NotFound


client = pymongo.MongoClient("mongodb+srv://Cykallu:NupLfVcy6J5P0irW@cluster0.uzflz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.users

# CRUD
# C => create()
# R => get_all() ja get_by_id()
# U => update()
# D => delete()

class User:
    
    #Määritetään class sisältö
    def __init__(self, username, password=None, profile_picture=None, role='user', _id=None):
        self.username = username
        self.password = password
        self.profile_picture = profile_picture
        self.role = role
        
        if _id is not None:
            _id = str(_id)
        self._id = _id

    
    # CRUD:n C (eli tässä lisätään käyttäjä)
    def create(self):
        result = db.users.insert_one({
            'username': self.username,
            'password': sha256.hash(self.password),
            'role': self.role
        })
        self._id = str(result.inserted_id)
    
    #Muokkaa yksittäisen käyttäjän tiedot json muotoon
    def to_json(self):
        user_in_json_format = {
            '_id': str(self._id),
            'username': self.username,
            'role': self.role
        }

        return user_in_json_format
    
    #Käyttäjä listan muuttaminen json muotoon
    @staticmethod
    def list_to_json(users):
        users_list_in_json = []
        for user in users:
            users_list_in_json.append(user.to_json())
        return users_list_in_json
    
    # CRUD:n R (READ) => haetaan kaikki käyttäjät
    @staticmethod
    def get_all():
        users = []
        users_cursor = db.users.find()
        for user in users_cursor:
            users.append(User(user['username'], _id=user['_id']))
        return users
    
    #Hakee käyttäjän IDn perusteella
    @staticmethod
    def get_by_id(_id):
        user_dictionary = db.users.find_one({'_id': ObjectId(_id)})
        user = User(user_dictionary['username'], _id=_id)
        return user
    
    #Hakee käyttäjän käyttäjänimellä
    @staticmethod
    def get_by_username(username, update=False, logged_in_user_id=None):
        if update:
            if logged_in_user_id is None:
                raise ValidationError('When updating your account, provide your user ID')
            user = db.user.find_one({'username':username, 
            '_id':  {'$ne': ObjectId(logged_in_user_id)}})
        else:
            user = db.users.find_one({'username':username})
        return user
        

    #Hakee käyttäjän s.posti osoitteella
    @staticmethod
    def get_by_email(email):
        user = db.users.find_one({'email': email})
        if user is None:
            raise NotFound(message='Email not found')
        return User(
        username = user['username'], 
        email = user['email'],
        password=user['password'], 
        role=user['role'], 
        _id=user['_id'])

    
    # CRUD:n osa U
    def update(self):
        db.users.update_one({'_id': ObjectId(self._id)},
        {
            '$set': {'username': self.username}
        })
    
    # CRUD:n osa U (Käyttäen static methodia)
    @staticmethod
    def update_by_id(_id, new_username):
        db.users.update_one({'_id': ObjectId(_id)}, {
            '$set': {'username': new_username}
        })

        user = User.get_by_id(_id)
        return user

    # CRUD:n osa D (Yksittäisen käyttäjän poisto)
    def delete(self):
        db.users.delete_one({'_id': ObjectId(self._id)})
    
    # CRUD:n osa D (Yksittäisen käyttäjän poisto staattisella metodilla)
    @staticmethod
    def delete_by_id(_id):
        db.users.delete_one({'_id': ObjectId(_id)})

    

### PUBLICATION ###
class Publication:
    def __init__(self, 
    title, 
    description, 
    url, 
    owner=None, 
    likes=[],
    shares=0,
    tags=[],
    comments=[],
    visibility=2,
    share_link=None,
    _id=None):
        self.title = title
        self.description = description
        self.url = url
        self.owner = owner
        self.likes = likes
        self.shares = shares
        self.tags = tags
        self.comments = comments
        self.visibility = visibility 
        #2 = näkyy kaikille,
        #1 = näkyy vain kirjautuneille käyttäjille
        # 0= vain itselle+admin
        self.share_link=share_link
        if _id is not None:
            # jos _id ei ole oletusarvo (eli None), silloin se tulee muuttaa merkkijonoksi käyttäen str:ää
            # muuten jsonify epäonnistuu
            _id = str(_id)
        self._id = _id
    
    ### CRUD C ###
    #Luodaan uusi julkaisu
    def create(self):
        result = db.publications.insert_one({
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'owner': self.owner,
            'likes': self.likes,
            'shares': self.shares,
            'tags': self.tags,
            'comments': self.comments,
            'visibility': self.visibility,
            'share_link': self.share_link
        })
        self._id = str(result.inserted_id)

    ### CRUD R ###
    #Hakee kaikki julkaisut
    @staticmethod
    def get_all():
        publications = []
        publications_cursor = db.publications.find()
        for publication in publications_cursor:
            title = publication['title']
            description = publication['description']
            url = publication['url']
            owner = publication['owner']
            likes = publication['likes']
            shares = publication['shares']
            tags = publication['tags']
            comments = publication['comments']
            visibility = publication['visibility']
            share_link = publication['share_link']
            _id = publication['_id']
            publication_object = Publication(title, description, url,owner,likes,shares,tags,comments,visibility,share_link,_id)
            publications.append(publication_object)
        
        return publications
    #Hakee julkaisun ID:n perusteella
    @staticmethod
    def get_by_id(_id):
        publication_dictionary = db.publications.find_one({'_id': ObjectId(_id)})
        if publication is None:
            raise NotFound('Publication not found')
        publication = Publication(
            title = publication_dictionary['title'],
            description = publication_dictionary['description'],
            url = publication_dictionary['url'],
            owner = publication_dictionary['owner'],
            likes = publication_dictionary['likes'],
            shares = publication_dictionary['shares'],
            tags = publication_dictionary['tags'],
            comments = publication_dictionary['comments'],
            visibility = publication_dictionary['visibility'],
            share_link = publication_dictionary['share_link'],
            _id = publication_dictionary['_id'],
            publication = Publication(
                title,
                description,
                url,
                owner=owner,
                likes=likes,
                shares=shares,
                tags=tags,
                comments=comments,
                visibility=visibility,
                share_link=share_link,
                _id=_id
            ))
        return publication

    def get_comments(self):
        comments_dicts = db.comments.find({'publication' : ObjectId(self._id)})
        comments = []
        for comment_dict in comment_dicts:
            comments.append(Comment(
                comment_dict['body'],
                str(comment_dict['owner'], 
                str(comment_dict['publication']
                ))))
        self.comments = comments
    
    def get_owner(self):
        if self.owner is not None:
            owner = User.get_by_id(self.owner)
            self.owner = owner
    

    @staticmethod
    def get_by_visibility(visibility=2):
        publications_cursor = db.users.publications.find({'visibility':visibility})
        publications = []
        for publication_dictionary in publications_cursor:
            title = publication_dictionary['title']
            description = publication_dictionary['description']
            url = publication_dictionary['url']
            owner = publication_dictionary['owner']
            likes = publication_dictionary['likes']
            shares = publication_dictionary['shares']
            tags = publication_dictionary['tags']
            comments = publication_dictionary['comments']
            visibility = publication_dictionary['visibility']
            share_link = publication_dictionary['share_link']
            _id = publication_dictionary['_id']
            publication = Publication(
                title,
                description,
                url,
                owner=owner,
                likes=likes,
                shares=shares,
                tags=tags,
                comments=comments,
                visibility=visibility,
                share_link=share_link,
                _id=_id
            )
            publications.append(publication)
        return publication
        
        
    #Hakee julkaisun käyttäjän ja näkyvyyden perusteella
    @staticmethod
    def get_by_owner_and_visibility(user={}, visibility=[2]):
        publications_cursor = db.users.publications.find({
            '$or': [
                {'visibility':{'$in':visibility}},
                {'owner':ObjectId(user['sub'])}
            ]
        })
        #Looppaa julkaisun sisällön ja tekee niistä Publication tyyppisen
        publications = []
        for publication_dictionary in publications_cursor:
            title = publication_dictionary['title']
            description = publication_dictionary['description']
            url = publication_dictionary['url']
            owner = publication_dictionary['owner']
            likes = publication_dictionary['likes']
            shares = publication_dictionary['shares']
            tags = publication_dictionary['tags']
            comments = publication_dictionary['comments']
            visibility = publication_dictionary['visibility']
            share_link = publication_dictionary['share_link']
            _id = publication_dictionary['_id']
            publication = Publication(
                title,
                description,
                url,
                owner=owner,
                likes=likes,
                shares=shares,
                tags=tags,
                comments=comments,
                visibility=visibility,
                share_link=share_link,
                _id=_id
            )
            publications.append(publication)
        return publication
    
    # CRUD:n osa U
    #Päivittää julkaisun ID:n mukaan
    def update(self):
        db.publications.update_one({'_id': ObjectId(self._id)},
        {
            '$set': {'title': self.title}, 
            '$set': {'description':self.description},
            '$set': {'visibility':self.visibility}
        })
    
    #Muokkaa käyttäjän postauksen static metodilla
    @staticmethod
    def update_by_id(_id, new_title, new_description):
        db.publications.update_one({'_id': ObjectId(_id)}, 
        {
            '$set': {'title': new_title},
            '$set': {'description':new_description}
        })
        publication = Publication.get_by_id(_id)
        return publication
        
   
    ### CRUD D ###
    #Julkaisun poisto
    def delete(self):
        db.publications.delete_one({'_id': ObjectId(self._id)})
    
    #Julkaisun poisto @staticmethod käyttäen
    @staticmethod
    def delete_by_id(_id):
        db.publications.delete_one({'_id': ObjectId(_id)})
 
    
    
    #JSON muotoon muuttaminen
    def to_json(self):
        owner = self.owner
        if owner is not None:
            owner = str(owner)
        publication_in_json_format = {
            '_id': self._id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'owner': owner,
            'likes': self.likes,
            'shares': self.shares,
            'tags': self.tags,
            'comments': self.comments,
            'visibility': self.visibility,
            'share_link': self.share_link
        }
        return publication_in_json_format

    
    #Listan muuttaminen JSON muotoon
    @staticmethod
    def list_to_json(publications_list):
        publications_in_json_format = []
        for publication in publications_list:
            publication_in_json_format = publication.to_json()
            publications_in_json_format.append(publication_in_json_format)
        return publications_in_json_format



class Comment:
    def __init__(self, body,owner,publication, _id=None):
        self.body = body
        self.owner = str(owner)
        self.publication = str(publication)
        if _id is not None:
            _id = str(_id)
        self._Id = _id
    
    def get_owner(self):
        return User.get_by_id(self.owner)

    def to_json(self, include_owner = False):
        owner = str(self.owner)
        if include_owner:
            owner = self.get_owner().to_json()
        return {
            '_id' : self._id,
            'owner' : self.owner
        }

    @staticmethod
    def list_to_json(comments):
        comments_in_json_format = []
        for comment in comments:
            comments_in_json_format.append(comment.to_json())
        return comments_in_json_format
    
