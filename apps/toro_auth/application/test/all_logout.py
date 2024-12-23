from redis import Redis
from redis.exceptions import RedisError
import requests

# Redis 클라이언트 설정
redis_client = Redis(host='localhost', port=6379, decode_responses=True)
logout_url = "http://localhost:8000/api/logout"

try:
    cursor = 0
    pattern = "refresh_token:*"
    while True:
        # SCAN으로 토큰 키 점진적으로 가져오기
        cursor, keys = redis_client.scan(cursor=cursor, match=pattern, count=100)
        
        for key in keys:
            token = key.split("refresh_token:")[-1]
            
            # API 요청
            try:
                response = requests.post(logout_url, json={"token": token})
                if response.status_code == 200:
                    print(f"Token {token} successfully logged out.")
                else:
                    print(f"Failed to logout token {token}: {response.status_code} - {response.json()}")
            except requests.RequestException as e:
                print(f"Request failed for token {token}: {str(e)}")
        
        # SCAN 완료
        if cursor == 0:
            break

except RedisError as e:
    print(f"Redis error: {str(e)}")
