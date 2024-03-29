from pickle import APPEND
import pymongo
import string
import random
from datetime import datetime, timezone
from bson.objectid import ObjectId
from pymongo.server_api import ServerApi
from passlib.hash import pbkdf2_sha256 as sha256
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
            'role': self.role,
            'profile_picture':self.profile_picture
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
    def get_by_username(username):
        user_dictionary = db.users.find_one({'username': username})
        if user_dictionary is None:
            raise NotFound(message='User not found')
        user = User(username, password=user_dictionary['password'], _id=user_dictionary['_id'])
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
            '$set': {'username': self.username},
            '$set': {'password': self.password},
            '$set': {'profile_picture': self.profile_picture}
            
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
        #0 = vain itselle+admin
        self.share_link=share_link
        if _id is not None:

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
        if publication_dictionary is None:
            raise NotFound(message='Publication not found')
        title = publication_dictionary['title']
        description = publication_dictionary['description']
        url = publication_dictionary['url']
        owner = publication_dictionary['owner']
        likes = publication_dictionary['likes']
        tags = publication_dictionary['tags']
        comments = publication_dictionary['comments']
        visibility = publication_dictionary['visibility']
        share_link = publication_dictionary['share_link']
        shares = publication_dictionary['shares']
        _id = publication_dictionary['_id']
        publication = Publication(
            title, 
            description, 
            url, 
            owner=owner, 
            likes=likes,
            tags=tags,
            comments=comments,
            visibility=visibility,
            share_link=share_link,
            shares=shares,
            _id =_id
        )
        return publication


    #hakee julkaisut näkyvyydellä
    @staticmethod
    def get_by_visibility(visibility=2):
        publications_cursor = db.publications.find({'visibility': visibility})
        publications = []
        for publication_dictionary in publications_cursor:
            # voit käyttää tästä alaspäin koodia get_by_id-methodissa suoraan.
            title = publication_dictionary['title']
            description = publication_dictionary['description']
            url = publication_dictionary['url']
            owner = publication_dictionary['owner']
            likes = publication_dictionary['likes']
            tags = publication_dictionary['tags']
            comments = publication_dictionary['comments']
            visibility = publication_dictionary['visibility']
            share_link = publication_dictionary['share_link']
            shares = publication_dictionary['shares']
            _id = publication_dictionary['_id']
            publication = Publication(
                title, 
                description, 
                url, 
                owner=owner, 
                likes=likes,
                tags=tags,
                comments=comments,
                visibility=visibility,
                share_link=share_link,
                shares=shares,
                _id =_id
            )
            publications.append(publication)
        return publications

        
        
    #Hakee julkaisun käyttäjän ja näkyvyyden perusteella
    @staticmethod
    def get_by_owner_and_visibility(user={}, visibility=[2]):
        
        publications_cursor = db.publications.find({
            '$or': [
                {'visibility': {'$in': visibility}},
                {'owner': ObjectId(user['sub'])}
            ]
        })
        publications = []
        for publication_dictionary in publications_cursor:
            title = publication_dictionary['title']
            description = publication_dictionary['description']
            url = publication_dictionary['url']
            owner = publication_dictionary['owner']
            likes = publication_dictionary['likes']
            tags = publication_dictionary['tags']
            comments = publication_dictionary['comments']
            visibility = publication_dictionary['visibility']
            share_link = publication_dictionary['share_link']
            shares = publication_dictionary['shares']
            _id = publication_dictionary['_id']
            publication = Publication(
                title, 
                description, 
                url, 
                owner=owner, 
                likes=likes,
                tags=tags,
                comments=comments,
                visibility=visibility,
                share_link=share_link,
                shares=shares,
                _id =_id
            )
            publications.append(publication)
        return publications

    
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
    def update_by_id(_id, new_title, new_description,new_visibility):
        db.publications.update_one({'_id': ObjectId(_id)}, 
        {
            '$set': {'title': new_title},
            '$set': {'description':new_description},
            '$set': {'visibility':new_visibility}
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
        likes = self.likes
        for count, user_id in enumerate(likes):
            likes[count] = str(user_id)
        if owner is not None:
            owner = str(owner)
        publication_in_json_format = {
            '_id': self._id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'owner': owner,
            'likes': likes,
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
    
    #Tykkäyksen lisäys
    def like(self):
        db.publications.update_one({'_id':ObjectId(self._id)},
        {
            '$set':{'likes':self.likes}
        })
    
    #Jaon lisäys
    def share(self):
        _filter = {'_id':ObjectId(self._id)}
        if self.share_link is None:
            letters = string.ascii_lowercase
            self.share_link = ''.join(random.choice(letters) for _ in range(8))
            _update = {'$set':{'share_link': self.share_link}, 'shares':1}
        else:
            _update = {'$inc':{'shares':1}}
        db.publications.update_one( _filter, _update)
    
    #Kommentin lisäys
    def add_comment(self,body):
        comment = Comment.create()
        comment = self.comments.append(comment)
    
    #Hakee kommentit
    def get_comments(self):
        comments = Comment.get_by_publication_id(self._id)
        return comments   
    
    #Hakee yksittäisen kommentin
    def get_comment(self, comment_id):
        comment =Comment.get_by_id(comment_id)
        return comment
    #Hakee kommentint käyttäjän ja idn perusteella
    def get_comment_by_owner_id(self, comment_id, owner_id):
        comment =Comment.get_by_id_and_owner(comment_id,owner_id)
        return comment
    #Poistaa kommentint
    def delete_comment(self,comment_id):
        Comment.delete_by_id(comment_id)

    #Poistaa kommentitn id ja käyttäjän perusteella
    def delete_comment_by_id_and_owner(self,comment,owner):
        Comment.delete_by_id_owner(comment,owner)
        






class Comment:
    def __init__(self, body, owner, publication, _id=None):
        self.body = body
        self.owner = str(owner)
        self.publication = str(publication)
        if _id is not None:
            _id = str(_id)
        self._id = _id
    
    #Luo kommentti
    def create(self):
        comment = db.comments.insert_one({
            'body':self.body, 
            'owner':ObjectId(self.owner),
            'publication':ObjectId(self.publication),
            'created': datetime.now(timezone.utc)
            })
        self._id = str(comment.inserted_id)
    
    #Päivitä kommentti
    def update(self):
        db.comments.update_one({'_id': ObjectId(self._id)},
        {
            '$set': {'body': self.body}
        })
    
    #Poista kommentti
    def delete(self):
        db.comments.delete_one({'_id': ObjectId(self._id)})
    
    #Kommentin haku vis ja owner perusteella
    @staticmethod
    def get_comment_by_publication_id_and_comment_id(publication_id, comment_id):
        comment = db.comments.find_one({'publication': ObjectId(publication_id), '_id': ObjectId(comment_id)})
        return Comment(comment['body'], comment['owner'], comment['publication'])
    
    def get_by_id_and_owner(_id, owner):
        comment = db.comments.find_one({'id':ObjectId(_id),'owner': ObjectId(owner)})
        if comment is None:
            raise NotFound(message="Comment not found")
        return  Comment(
                comment['body'],
                comment['owner'],
                _id,
                _id = comment['_id'])
    
    #Hakee kommentin omistajan
    def get_owner(self):
        return User.get_by_id(self.owner)
    
    #Hakee publication id perusteella
    @staticmethod
    def get_by_publication_id(_id):
        comments_list = db.comments.find({'publication': ObjectId(_id)})
        if comments_list is None:
            return []
        comments = []
        for comment_dict in comments_list:
            comments.append(Comment(
                comment_dict['body'],
                comment_dict['owner'],
                _id,_id = comment_dict['_id']))
        return comments
    #kommentin haku ID perusteella
    @staticmethod
    def get_by_id(_id):
        comment = db.comments.find_one({'id':ObjectId(_id)})
        if comment is None:
            raise NotFound(message="Comment not found")
        return  Comment(
                comment['body'],
                comment['owner'],
                _id,
                _id = comment['_id'])
    #Kommentin poisto käyttäjän ja idn perusteella
    def delete_by_id_owner(_id,owner):
        db.comments.delete_one({'_id':ObjectId(_id), 'owner':ObjectId(owner)})
    #Kommentin päivitys
    def update(self):
        db.comments.update_one({'_id':ObjectId(self._id)},
                               {'$set':{'body':self.body}})
    #Kommentin poisto IDllä
    @staticmethod
    def delete_by_id(_id):
        db.comments.delete_one({'_id':ObjectId(_id)})
    
    #Kommentti json
    def to_json(self, include_owner = False):
        owner = str(self.owner)
        if include_owner:
            owner = self.get_owner().to_json()
        return {
            '_id' : self._id,
            'body' : self.body,
            'owner' : self.owner,
            'publication': self.publication
        }
    
    #Lista json
    @staticmethod
    def list_to_json(comments_list):
        comments = []
        for comment in comments_list:
            comments.append(comment.to_json())
        return comments
    
