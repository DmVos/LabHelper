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
    
    #Получение всего списка меню
    def getMenu(self):
        sql = '''SELECT * FROM mainmenu WHERE title in ('Home', 'Login') ORDER BY sq'''

        #try:
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        if res:
            return res
        #except:
        #    print ("Ошибка чтения из БД")
        return []
    
    #Получение меню для авторизованных пользователей
    def getMenuForUser(self):
        sql = '''SELECT * FROM mainmenu WHERE title in ('Home', 'My experiments', 'All experiments', 'Add experiment', 'Logout') ORDER BY sq'''

        #try:
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        if res:
            return res
        #except:
        #    print ("Ошибка чтения из БД")
        return []
    
    def addExreriment(self, title, start_date, img):
        try:
            tm = math.floor(time.time())
            binary = sqlite3.Binary(img)
            self.__cur.execute("INSERT INTO experiments VALUES(NULL, ?, ?, ?, ?)", (title, tm, 0, binary))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления эксперимента в БД " + str(e))
            return False
        return True

    def getExperiment(self, exp_id):
        try:
            self.__cur.execute(f"SELECT title, start_date FROM experiments WHERE id={exp_id} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения эксперимента в БД " + str(e))
            
        return (False, False)
    
    def getAllExperiments(self):
        try:
            self.__cur.execute(f"SELECT id, title, start_date FROM experiments ORDER BY id DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения экспериментов в БД " + str(e))
            
        return []
    
    # Функция для загрузки изображения из базы данных SQLite
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
            print("Ошибка получения изображения из БД " + str(e))        
        return None
    
    # Функция для регистрации пользователя
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
            print("Ошибка добавления пользователя" + str(e))    
            return False     
        return True
    

    # Функция для получения пользователя
    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print ('Пользователь не найден в БД.')
                return False
            
            return res
        except sqlite3.Error as e:
            print("Ошибка получения пользователя из БД" + str(e))    
            return False     
        
    # Функция для получения пользователя по логину
    def getUserByLogin(self, userlogin):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE login = '{userlogin}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print ('Пользователь не найден в БД.')
                return False
            
            return res
        except sqlite3.Error as e:
            print("Ошибка получения пользователя из БД" + str(e))    
            return False     
        



