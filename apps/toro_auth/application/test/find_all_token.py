from redis import Redis

redis_client = Redis(host='localhost', port=6379, decode_responses=True)

# SCAN 명령으로 refresh_token:* 키 가져오기
cursor = 0
pattern = "refresh_token:*"

while True:
    cursor, keys = redis_client.scan(cursor=cursor, match=pattern, count=100)
    for key in keys:
        value = redis_client.get(key)
        print(f"{key} => {value}")
    if cursor == 0:
        break
