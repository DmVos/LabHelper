import sqlite3
import time
import math
import io


from io import BytesIO
from PIL import Image

class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    
    # Get list for main menu
    def getMenu(self):
        sql = '''SELECT * FROM mainmenu WHERE title in ('Home', 'Login') ORDER BY sq'''
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        if res:
            return res
        return []
    
    # Get menu for loggined users
    def getMenuForUser(self):
        sql = '''SELECT * FROM mainmenu WHERE title in ('Home', 'My experiments', 'All experiments', 'Add experiment', 'Logout') ORDER BY sq'''
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        if res:
            return res
        return []
    
    # Add new experiment to DB
    def addExreriment(self, title, unix_timestamp, user, img, sample_size_h, sample_size_w, comment):
        try:
            binary = sqlite3.Binary(img)
            self.__cur.execute("INSERT INTO experiments VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)", (title, unix_timestamp, user, binary, sample_size_h, sample_size_w, comment))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error adding experiment to database " + str(e))
            return False
        return True

    # Get experiment from DB
    def getExperiment(self, exp_id):
        try:
            self.__cur.execute(f"SELECT title, start_date, sample_size_h, sample_size_w, comment FROM experiments WHERE id={exp_id} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error getting experiment from database " + str(e))           
        return (False, False)
    
    # Get all experiments from DB
    def getAllExperiments(self):
        try:
            self.__cur.execute(f"SELECT exp.id, exp.title, exp.start_date, exp.sample_size_h, exp.sample_size_w, exp.comment, u.name FROM experiments exp LEFT JOIN users u ON u.id=exp.user ORDER BY exp.id DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error getting experiments from database " + str(e))
        return []
    
    # Get user's experiments from DB
    def getUserExperiments(self,user_id):
        try:
            self.__cur.execute("SELECT exp.id, exp.title, exp.start_date, exp.sample_size_h,  exp.sample_size_w, exp.comment, u.name FROM experiments exp LEFT JOIN users u ON u.id=exp.user WHERE exp.user=? ORDER BY exp.id DESC",(user_id,))
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error getting experiments from database " + str(e))
        return []
    
    # Get image from DB
    def loadImage (self, exp_id):
        try:
            self.__cur.execute("SELECT image FROM experiments WHERE id=?", (exp_id,))
            res = self.__cur.fetchone()
            if res:
                image_stream = io.BytesIO(res[0])
                image_stream.seek(0)
                image = Image.open(image_stream)
                return image
        except sqlite3.Error as e:
            print("Error getting image from database " + str(e))        
        return None
    
    # Register new user
    def addUser (self, username, userlogin, hpsw):
        try:
            self.__cur.execute(f"SELECT count() as 'count' FROM users WHERE login like '%{userlogin}%'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print ('A user with the same username already exists in the database.')
                return False
            tm = math.floor(time.time())
            self.__cur.execute(f"INSERT INTO users VALUES (NULL, ?, ?, ?, ?)", (username, userlogin, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error adding user to database " + str(e))    
            return False     
        return True
    

    # Get user info
    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print ("The user was not found in the database.")
                return False
            return res
        except sqlite3.Error as e:
            print("Error getting user from database." + str(e))    
            return False     
        
    # Get user by login
    def getUserByLogin(self, userlogin):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE login = '{userlogin}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print ('The user was not found in the database.')
                return False
            
            return res
        except sqlite3.Error as e:
            print("Error getting user from database." + str(e))    
            return False     
        



