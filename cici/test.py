import pymysql
import datetime

def DataFormat():
    fileHandle = open ( 'D:/data/userlist.txt', 'w' ) 
    userstatus=[]
    userlist=[123123,123123,123123,123132,12313,123132,123132,123132]
    a='Mon Jan 19 09:24:34 +0000 2015'
    creat_time=datetime.datetime.strptime(a[0:19]+a[25:30],'%a %b %d %H:%M:%S %Y')
    print creat_time
    userstatus.append((12312321,
                   123124413,
                   creat_time,
                   'china',
                   '32rerrehgtshrdhyteuj5eu86r8i7i7t6p097p[i0123123423443#$RF^&&^GHGBBNNTDSRGY%%YUHJNM<>LPP\xF0\x9F\x92\x97'))
    try:
        conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='twitterdata_python',port=3306,charset='utf8mb4')
        cur=conn.cursor()
        sql = "insert into tweet(user_id, status_id, creat_time, place, tweet_text) values(%s,%s,%s,%s,%s)"
        cur.executemany(sql,userstatus)
        for u in userlist:
            fileHandle.write( str(u)+"\n" )  
        conn.commit()
        cur.close()
        conn.close()
        fileHandle.close()         
    except pymysql.Error,e :
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def WriteFile():
    fileWriter = open ( 'D:/data/test.txt', 'a' )
    fileWriter.write( "\n"+"4444" )
    fileWriter.close()
    

WriteFile();
