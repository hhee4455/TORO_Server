from apps.toro_auth.domain.entity.account import Account
from apps.toro_auth.application.repositories.account_repository import AccountRepository
from apps.toro_auth.infra.orm.models.account_model import AccountModel
from django.contrib.auth.hashers import make_password  # 비밀번호 해시화

class AccountRepositoryImpl(AccountRepository):
    """
    AccountRepository의 Django ORM을 이용한 구현체.
    """
    
    def create(self, email: str, password: str, name: str) -> Account:
        """
        이메일, 비밀번호, 이름을 받아 새로운 사용자를 생성합니다.
        
        Args:
            email (str): 이메일 주소
            password (str): 비밀번호
            name (str): 사용자 이름
        
        Returns:
            Account: 생성된 계정 객체
        """
        # 비밀번호를 해시화해서 저장
        hashed_password = make_password(password)
        account_model = AccountModel.objects.create(email=email, password=hashed_password, name=name)
        return Account(id=account_model.id, email=account_model.email, name=account_model.name)

    def find_by_email(self, email: str) -> Account:
        """
        이메일로 사용자를 찾습니다.
        
        Args:
            email (str): 이메일 주소
        
        Returns:
            Account: 계정 객체
        """
        try:
            account_model = AccountModel.objects.get(email=email)
            return Account(id=account_model.id, email=account_model.email, name=account_model.name)
        except AccountModel.DoesNotExist:
            return None
        

