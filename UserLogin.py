
class UserLogin():
     
    def is_active (self):
        return True
    
    def is_authenticated(self):
        return True
    
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self
    
    def create(self, user):
        self.__user = user
        return self
    
    def get_id(self):
        return str(self.__user['id'])
    
    def getName(self):
        return self.__user['name'] if self.__user else 'No name'