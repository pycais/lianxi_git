import redis
import time
client = redis.StrictRedis(db=11)

while True:
    client.publish("1807" , "hello")
    time.sleep(2)