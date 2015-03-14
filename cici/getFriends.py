from time import sleep
import twitter
import pymysql
import datetime

api = twitter.Api(consumer_key='fCeev0j68fRvehhRe4ZirAC7P',
                  consumer_secret='QuefvIyXw3pgMkqlyGnJ0sPKmLZbg1PSRd3bbj9GRwLL8ab4pv',
                  access_token_key='1617304460-YTKDNPvWR6UBtwuw9qXQhfqXkRCyEjhNt3z1C92',
                  access_token_secret='V2mzTzYufyy3hmJOrhUHr5EAriuqecBK7TJd6OhCW2ykk')
connection=pymysql.connect(host='localhost',user='root',passwd='123456',db='twitterdata_python',port=3306,charset='utf8mb4')
fileHandle = open ( 'D:/data/userlist.txt', 'r+' ) 

nodename='PeppoLorusso';
nodeid=472762626;
line='';
cursor=-1;
user_followers=[];
user_friends=[];
userid=[];
userinfo=[];
userstatus=[];
candidateuser=[];
userRollTwo=[];

def Main():
    #GetRelationByApi(nodeid);
    ReadFile();    
    for user in userRollTwo:
        GetRelationByApi(user);
    connection.close();

def ReadFile():
    fileReader = open ( 'D:/data/userlist1.txt', 'r+' ) 
    lines=fileReader.readlines();
    for line in lines:
        userRollTwo.append(int(line));       
    fileReader.close();

def WriteFile():
    fileWriter = open ( 'D:/data/userlist1.txt', 'a' )
    fileWriter.write("\n")
    for u in candidateuser:
        fileWriter.write( str(u)+"\n" )
    fileWriter.close()

def ConfirmUser(uid):
    user=api.GetUser(uid,None,True);
    print user.screen_name;

def GetRelationByApi(uid):    
    user_followers=[];
    user_friends=[];
    relationid=[];
    userinfo=[];
    candidateuser_roll1=[];

    if(uid==nodeid):
        nodeuser=api.GetUser(uid,None,True);
        userinfo.append((nodeuser.id,
                        nodeuser.screen_name,
                        nodeuser.location,
                        nodeuser.lang,
                        nodeuser.description,
                        nodeuser.followers_count,
                        nodeuser.friends_count,
                         datetime.datetime.strptime(
                             nodeuser.created_at[0:19]+nodeuser.created_at[25:30],
                             '%a %b %d %H:%M:%S %Y')))
    try:
        ConfirmUser(uid)
        print str.format("      Getting friends of {0} ",uid)
        user_friends = api.GetFriendIDs(uid, None, cursor, False, None);
        print str.format("          {0}'s friendlist is OK",uid)

        print str.format("      Getting followers of {0}",uid)
        user_followers = api.GetFollowerIDs(uid,None,cursor,False,None,10000);
        print str.format("          {0}'s followerlist is OK",uid)
    except Exception as e:
        if "Not authorized" in str(e.message):
            print "      Not authorized to get friendlist, skip this user"
        else:
            if "Rate limit exceeded" in str(e.message):
                print "      Rate limit exceeded, sleep 10 mins..."
                sleep(1000)
                print "      continue..."

                if len(user_friends) ==0:
                    print str.format("      Getting friends of {0} ",uid)
                    user_friends = api.GetFriendIDs(uid, None, cursor, False, None);
                    print str.format("          {0}'s friendlist is OK",uid)

                if len(user_followers) ==0:
                    print str.format("      Getting followers of {0}",uid)
                    user_followers = api.GetFollowerIDs(uid,None,cursor,False,None,10000);
                    print str.format("          {0}'s followerlist is OK",uid)
            else:
                raise Exception;



    for i in user_friends:
        relationid.append((uid,i))
        candidateuser.append(i)

    for j in user_followers:
        relationid.append((j,uid))
        candidateuser.append(j)

    try:
        cur=connection.cursor()
        sql_relation = "insert into relationship (user_id, friend_id) values(%s,%s)"
        sql_candidateuser = "insert into candidateuser (id) values(%s)"
        print "      Writting into database of relation"        
        cur.executemany(sql_relation,relationid);
        print "          Writting into database of relation is OK"
        print "      Writting into database of candidateuser"
        cur.executemany(sql_candidateuser,candidateuser);
        print "          Writting into database of relation is OK"
        connection.commit();
        print "      commit is OK"
        #cur.close();
        #connection.close();
        print str.format("{0} is ready ",uid);
    except pymysql.Error:
        print str(pymysql.Error)
    del user_followers[:]
    del user_friends[:]
    del candidateuser_roll1[:]
    
def GetUserTimeLine(uid):
    print str.format("Getting user timeline {0}",uid)
    userstatus=[];
    status=[];
    status=api.GetUserTimeline(uid,None,None,None,200,True,None,None)
    for i in range(0,len(status)):
        creat_time=datetime.datetime.strptime(status[i].created_at[0:19]+status[i].created_at[25:30],'%a %b %d %H:%M:%S %Y')
        userstatus.append((status[i].user.id,
                           status[i].id,
                           creat_time,
                           status[i].location,
                           status[i].text))
    
    cur=connection.cursor()
    sql = "insert into tweet (user_id, status_id, creat_time, place, tweet_text) values(%s,%s,%s,%s,%s)"
    try:
       cur.executemany(sql,userstatus);
       connection.commit();
       cur.close();
       connection.close();
    except pymysql.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

   

Main();
