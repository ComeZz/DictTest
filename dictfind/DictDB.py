import pymysql
import hashlib

class dictDB:
    '''
    字典数据库
    '''
    def __init__(self,host='localhost',port=3306,user='root',password='123456',charset='utf8',database=None):
        self.db = pymysql.connect(host=host,
                                  port=port,
                                  user=user,
                                  password=password,
                                  database=database,
                                  charset=charset)

        # 创建游标 (操作数据库语句,获取查询结果)
        self.cur = self.db.cursor()

    def insertoHist(self,name,word):
        sqlstr="insert into hist(name,word) values('%s','%s')"%(name,word)
        try:
            self.cur.execute(sqlstr)
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def RegisterUser(self,name,pw):
        sqlstr="select * from user where name='%s'"%(name)
        self.cur.execute(sqlstr)
        result=self.cur.fetchone()
        if result:
            return False

        pw=self.hashpw(pw)
        insertsql="insert into user (name,passwd) values (%s,%s)"
        try:
            self.cur.execute(insertsql,[name,pw])
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    def LookupWord(self,name,word):
        sql="select word,mean from words where word=%s"
        self.cur.execute(sql,word)
        result=self.cur.fetchone()
        self.insertoHist(name,word)
        return result

    def LookupHis(self,name):
        sql="select word,time from hist where name='%s' order by time desc"%(name)
        self.cur.execute(sql)
        result=self.cur.fetchmany(10)
        return result


    def Login(self,name,pw):
        sqlstr = "select passwd from user where name='%s'"%(name)
        self.cur.execute(sqlstr)
        result = self.cur.fetchone()
        pw=self.hashpw(pw)
        if result[0]==pw:
            return True
        else:
            return False

    def close(self):
        self.cur.close()
        self.db.close()

    def hashpw(self,pw):
        pw=pw+'@sh'
        hash = hashlib.md5()
        hash.update(pw.encode())
        pw = hash.hexdigest()
        return pw











