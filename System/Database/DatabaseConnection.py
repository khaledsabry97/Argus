import sqlite3


class DatabaseConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect('Argus_DB.db')
        self.cursor = self.conn.cursor()


    def insertSavedFramesVid(self,camera_id,starting_frame_id):
        self.connect()
        sql = "INSERT INTO SavedFrames (camera_id,frame_id) VALUES("+str(camera_id)+", "+str(starting_frame_id)+")"

        self.cursor.execute(sql)
        self.conn.commit()
        self.conn.close()






DatabaseConnection().insertSavedFramesVid(1,10)
