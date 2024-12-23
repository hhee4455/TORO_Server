import redis
import json

# Redis 서버 연결 설정
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def test_redis_token_storage():
    # 테스트용 키와 값
    test_key = "test_token:user123"
    test_data = {
        "user_id": "user123",
        "token": "example_token_value"
    }

    try:
        # 1. Redis에 user_id와 token을 JSON 형식으로 저장
        redis_client.set(test_key, json.dumps(test_data))
        print(f"데이터 저장 완료: {test_key} -> {test_data}")

        # 2. Redis에서 값 가져오기
        stored_value = redis_client.get(test_key)
        stored_data = json.loads(stored_value)  # JSON을 파싱해서 딕셔너리로 변환

        # 3. 출력: user_id와 token 값 확인
        print(f"Redis에서 읽어온 데이터: user_id={stored_data['user_id']}, token={stored_data['token']}")

        # 4. 값이 일치하는지 테스트
        assert stored_data["user_id"] == test_data["user_id"], "user_id 값이 일치하지 않습니다!"
        assert stored_data["token"] == test_data["token"], "token 값이 일치하지 않습니다!"
        print("테스트 성공: 저장된 user_id와 token 값이 올바릅니다.")
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
