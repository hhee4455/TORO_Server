import redis

# Redis 서버 연결 설정
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def test_redis_token_storage():
    # 테스트용 키와 토큰 값
    test_key = "test_token:user123"
    test_token = "example_token_value"

    try:
        # 1. Redis에 토큰 저장
        redis_client.set(test_key, test_token)
        print(f"Token 저장 완료: {test_key} -> {test_token}")

        # 2. Redis에서 토큰 값 가져오기
        stored_token = redis_client.get(test_key)
        print(f"Redis에서 읽어온 Token: {stored_token}")

        # 3. 값이 일치하는지 테스트
        assert stored_token == test_token, "토큰 값이 일치하지 않습니다!"
        print("테스트 성공: 저장된 토큰 값이 올바릅니다.")
    except AssertionError as e:
        print(f"테스트 실패: {e}")
    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        # 테스트 후 키 삭제
        redis_client.delete(test_key)
        print(f"테스트 키 삭제 완료: {test_key}")

if __name__ == "__main__":
    test_redis_token_storage()
