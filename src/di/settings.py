from src.di.containers import Container

def initialize_container():
    """DI 컨테이너 초기화 함수"""
    container = Container()
    container.wire(
        modules=[
            "src.interface.toro_auth.controllers.login",  # 컨트롤러 모듈 연결
            "src.interface.toro_auth.controllers.signup",
        ]
    )
    return container
