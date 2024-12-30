from apps.toro_auth.domain.entity.account import Account
from apps.toro_auth.application.repositories.account_repository import AccountRepository
from apps.toro_auth.infrastructure.orm.models.account_model import AccountModel
from apps.toro_auth.infrastructure.orm.mapper.account_mapper import AccountMapper
from django.contrib.auth.hashers import make_password, check_password
from typing import Optional


class AccountRepositoryImpl(AccountRepository):
    """AccountRepository의 Django ORM을 이용한 구현체."""

    def create(self, email: str, password: str, name: str) -> Account:
        """
        새로운 사용자를 생성.
        비밀번호는 해시 처리하여 저장하고, 생성된 계정을 Domain 객체로 반환.
        """
        hashed_password = make_password(password)  # 해시된 비밀번호 생성
        account_model = AccountModel.objects.create(email=email, password=hashed_password, name=name)
        return AccountMapper.to_domain(account_model)  # Domain 객체로 매핑

    def find_by_email(self, email: str) -> Optional[Account]:
        """
        이메일로 사용자 조회.
        존재하지 않으면 None 반환.
        """
        account_model = AccountModel.objects.filter(email=email).first()  # filter + first로 효율적 조회
        return AccountMapper.to_domain(account_model) if account_model else None

    def find_by_email_and_password(self, email: str, password: str) -> Optional[Account]:
        """
        이메일과 비밀번호로 사용자 조회.
        이메일로 사용자 조회 후 비밀번호 검증. 일치하지 않으면 None 반환.
        """
        account_model = AccountModel.objects.filter(email=email).first()
        if account_model and check_password(password, account_model.password):  # 비밀번호 검증
            return AccountMapper.to_domain(account_model)
        return None

    def find_by_id(self, account_id: str) -> Optional[Account]:
        """
        계정 ID로 사용자 조회.
        존재하지 않으면 None 반환.
        """
        account_model = AccountModel.objects.filter(id=account_id).first()
        return AccountMapper.to_domain(account_model) if account_model else None