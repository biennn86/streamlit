import sqlite3

class ConnectDB:
    __NAME_DB = 'database/db_trans_rtcis.db'

    def getConection(self):
        try:
            self.conn = sqlite3.connect(self.__NAME_DB)
            print('Kết nối database thành công')
            return self.conn
        except:
            print('Connect Database Fail.')
          
version https://git-lfs.github.com/spec/v1
oid sha256:bb5e3c533a4ea05e1d7067e90e4fd343596f3fa2cec4eda5818a5bec0285da0f
size 346
