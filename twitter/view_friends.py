import twitter

api = twitter.Api(consumer_key='fCeev0j68fRvehhRe4ZirAC7P',
                  consumer_secret='QuefvIyXw3pgMkqlyGnJ0sPKmLZbg1PSRd3bbj9GRwLL8ab4pv',
                  access_token_key='1617304460-YTKDNPvWR6UBtwuw9qXQhfqXkRCyEjhNt3z1C92',
                  access_token_secret='V2mzTzYufyy3hmJOrhUHr5EAriuqecBK7TJd6OhCW2ykk')
users = api.GetFriends()
print [u.name for u in users]
