import redis

client = redis.StrictRedis(db=11)

pb = client.pubsub()
pb.subscribe("1807", "1800")

for i in pb.listen():
    if i.get("type") == "message":
        print(i.get("data").decode())
