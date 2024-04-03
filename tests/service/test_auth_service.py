import pytest
from src.service.auth_service import AuthService
from src.model.user import User

@pytest.fixture
def mock_user_repository(mocker):
    return mocker.MagicMock()

@pytest.fixture
def auth_service(mock_user_repository):
    return AuthService(mock_user_repository)

def test_hash_password(auth_service):
    password = "testpassword"
    hashed_password = auth_service.hash_password(password)
    assert hashed_password != password
    assert auth_service.verify_password(password, hashed_password)

def test_verify_password(auth_service):
    password = "testpassword"
    hashed_password = auth_service.hash_password(password)
    assert auth_service.verify_password(password, hashed_password)
    assert not auth_service.verify_password("wrongpassword", hashed_password)

def test_register_user_new_email(auth_service, mock_user_repository):
    username = "testuser"
    email = "test@example.com"
    password = "testpassword"

    mock_user_repository.find_user_by_email.return_value = None
    new_user = auth_service.register_user(username, email, password)
    assert new_user is not None
    mock_user_repository.create_user.assert_called_once()

def test_register_user_existing_email(auth_service, mock_user_repository):
    username = "testuser"
    email = "test@example.com"
    password = "testpassword"
    existing_user = User(username, email, password)

    mock_user_repository.find_user_by_email.return_value = existing_user
    with pytest.raises(ValueError):
        auth_service.register_user(username, email, password)    