import MySQLdb
result=[] 
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='test',port=3306)
    cur=conn.cursor()
    cur.execute('select * from test')
    result=cur.fetchall()
    print [s for s in result]
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
