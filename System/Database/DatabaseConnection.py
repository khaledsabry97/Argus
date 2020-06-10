import os
import sqlite3

from System.Data.CONSTANTS import *


class DatabaseConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "Argus_DB.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()
    def execute(self,query):
        self.connect()
        self.cursor.execute(query)
        self.conn.commit()
        self.close()
    def insertSavedFramesVid(self,camera_id,starting_frame_id):
        query = "INSERT INTO SavedFrames (camera_id,frame_id) VALUES("+str(camera_id)+","+str(starting_frame_id)+")"
        self.execute(query)


    def insertCrashFramesVid(self,camera_id,starting_frame_id,from_no,city,district_no):
        if from_no > 5:
            print("helllo")
        query = "INSERT INTO CrashFrames (camera_id,frame_id,from_no,city,district,crash_time) VALUES("+str(camera_id)+", "+str(starting_frame_id)+","+str(from_no)+",\""+city+"\",\""+district_no+"\",datetime('now'))"
        self.execute(query)


    def updateCrashFramesVid(self,camera_id,starting_frame_id,from_no):
        if from_no > 5:
            print("helllo")
        query = "Update CrashFrames set from_no = "+str(from_no)+" Where camera_id = "+str(camera_id)+" and frame_id = "+str(starting_frame_id)
        print(query)
        self.execute(query)

    def deleteCrashFramesVid(self):
        query = "DELETE FROM CrashFrames Where from_no >=5"
        self.execute(query)

    def deleteSavedFramesVid(self,camera_id,starting_frame_id):
        query = "DELETE FROM SavedFrames Where camera_id = "+str(camera_id)+" and frame_id = "+str(starting_frame_id)
        self.execute(query)


    def selectCrashFrames(self):
        self.connect()

        query = "SELECT * from CrashFrames Where from_no < 5"
        result = self.cursor.execute(query).fetchall()
        self.conn.close()
        return result

    def selectSavedFrames(self,camera_id,starting_frame_id):
        self.connect()

        query = "SELECT frame_id from SavedFrames Where camera_id = "+str(camera_id)+" and frame_id > "+str(starting_frame_id) +" ORDER BY frame_id ASC"
        result = self.cursor.execute(query).fetchall()
        self.conn.close()
        return result

    def selectCrashFramesList(self,dic):
        self.connect()
        array = []
        if CITY in dic:
            array.append("city = \""+dic[CITY]+"\"")
        if DISTRICT in dic:
            array.append("district = \""+dic[DISTRICT]+"\"")
        if START_DATE in dic:
            array.append("crash_time BETWEEN \""+dic[START_DATE]+" "+dic[START_TIME]+"\" AND \""+dic[END_DATE]+" "+dic[END_TIME]+"\"")
        where = ' AND '.join(array)

        query = "SELECT camera_id,frame_id,city,district,crash_time from CrashFrames Where "+where+" ORDER BY crash_time DESC"
        result = self.cursor.execute(query).fetchall()
        self.conn.close()
        return result















# DatabaseConnection().insertSavedFramesVid(1,10)
