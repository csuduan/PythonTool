import  redis

r = redis.StrictRedis(host='192.168.1.20', port=6379)

r.set('name','kukudeyu')
print(r.get('name'))
print(r.get('dq'))