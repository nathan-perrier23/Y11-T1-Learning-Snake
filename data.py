import sqlite3
from sqlite3 import Error
import sys, os

class DATA:
    def __init__(self):
        self.database = "database.db"
        # create a database connection
        self.sql_create_player_table = '''CREATE TABLE IF NOT EXISTS high_scores (placement int, username text, score int)'''
        self.sql_create_user_table = '''CREATE TABLE IF NOT EXISTS users (username text, user_password text, user_device_name text, ip text)'''
        
        
    
    def main_db(self):
        
        conn_db = self.create_db_connection(self.database)
        #creates a concetion with memory
        conn_mem = self.create_mem_connection()
        
        
        # create tables
        if conn_db is not None:
            # create projects table
            self.create_table(self.sql_create_player_table,conn_db)
            self.create_table(self.sql_create_user_table,conn_db)
            
            print('placement - Username - score')
            print(conn_db.execute("select * from high_scores").fetchall())
            
            print('username - password - device name - ip')
            print(conn_db.execute("select * from users").fetchall())
            
            conn_db.close()
      
        else:
            print("Error! cannot create the database connection.")
    
    
    
    def create_table(self, create_table_sql, conn_db):
        try:
            c = conn_db.cursor()
            c.execute(create_table_sql)
            c.close()
            print('tables created')
        except Error as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    
    def create_db_connection(self,db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            # print(sqlite3.version)
            return conn
        except Error as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
                
    def create_mem_connection(self):
        conn = None;
        try:
            conn = sqlite3.connect(':memory:')
            print(sqlite3.version)
            return conn
        except Error as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)




