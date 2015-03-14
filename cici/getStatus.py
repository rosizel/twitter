import twitter
import pymysql
import datetime
from time import sleep

api = twitter.Api(consumer_key='fCeev0j68fRvehhRe4ZirAC7P',
                  consumer_secret='QuefvIyXw3pgMkqlyGnJ0sPKmLZbg1PSRd3bbj9GRwLL8ab4pv',
                  access_token_key='1617304460-YTKDNPvWR6UBtwuw9qXQhfqXkRCyEjhNt3z1C92',
                  access_token_secret='V2mzTzYufyy3hmJOrhUHr5EAriuqecBK7TJd6OhCW2ykk')
connection = pymysql.connect(host='localhost', user='root', passwd='123456', db='twitterdata_python', port=3306,
                             charset='utf8mb4')

cursor = -1;
userstatus = [];
candidateuser = [];
usersinfo = [];


def Main():
    ReadFile();
    for user in candidateuser:
        GetUserInfo(user);


def ReadFile():
    fileReader = open('D:/data/test.txt', 'r+')
    lines = fileReader.readlines();
    for line in lines:
        candidateuser.append(int(line));
    print candidateuser
    fileReader.close();


def GetUserInfo(uid):
    print str.format("Getting user {0} info", uid)
    user = api.GetUser(uid, None, True);
    usersinfo.append((user.id,
                     user.screen_name,
                     user.location,
                     user.lang,
                     user.description,
                     user.followers_count,
                     user.friends_count,
                     datetime.datetime.strptime(user.created_at[0:19] + user.created_at[25:30],
                                                '%a %b %d %H:%M:%S %Y')))
    try:
        cur = connection.cursor()
        sql_userinfo = "insert into userinfo ( userid, screen_name, location, language, description, follower_count, friends_count, creat_time) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        print "     Writting into database of userinfo"
        cur.executemany(sql_userinfo, usersinfo);
        connection.commit();
        del usersinfo [:]
        print "%s is ready"% user.id;
    except pymysql.Error, e:
        if 'Duplicate entry 'in str(e.message):
            print "user %s already in userinfo" % user.screen_name
        else:
            if "Rate limit exceeded" in str(e.message):
                print "      Rate limit exceeded, sleep 10 mins..."
                sleep(1000)
                print "      continue..."
            else:
                if "Not authorized" in str(e.message):
                    print "      Not authorized to get friendlist, skip this user"
                else:
                    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                    raise Exception


def GetUserTimeLine(uid):
    GetUserInfo(uid)
    userstatus = [];
    status = api.GetUserTimeline(uid, None, None, None, 200, True, None, None)
    for i in range(0, len(status)):
        creat_time = datetime.datetime.strptime(status[i].created_at[0:19] + status[i].created_at[25:30],
                                                '%a %b %d %H:%M:%S %Y')
        userstatus.append((status[i].user.id,
                           status[i].id,
                           creat_time,
                           status[i].location,
                           status[i].text))

    cur = connection.cursor()
    sql = "insert into tweet (user_id, status_id, creat_time, place, tweet_text) values(%s,%s,%s,%s,%s)"
    try:
        cur.executemany(sql, userstatus);
        connection.commit();
        del status[:]
    except pymysql.Error, e:

        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


Main();

