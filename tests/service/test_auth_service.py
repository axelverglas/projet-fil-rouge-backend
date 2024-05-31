import pytest
from src.service.auth_service import AuthService
from src.service.user_service import UserService
from src.model.user import User

@pytest.fixture
def mock_user_repository(mocker):
    return mocker.MagicMock()

@pytest.fixture
def auth_service(mock_user_repository):
    return AuthService(mock_user_repository)

@pytest.fixture
def user_service(mock_user_repository, auth_service):
    return UserService(mock_user_repository, auth_service)

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

def test_register_user_new_email(user_service, mock_user_repository):
    username = "testuser"
    email = "test@example.com"
    password = "testpassword"

    mock_user_repository.find_user_by_email.return_value = None
    mock_user_repository.find_user_by_username.return_value = None  # Ajout de cette ligne
    new_user = user_service.register_user(username, email, password)
    assert new_user is not None
    mock_user_repository.create_user.assert_called_once()

def test_register_user_existing_email(user_service, mock_user_repository):
    username = "testuser"
    email = "test@example.com"
    password = "testpassword"
    existing_user = User(username, email, password)

    mock_user_repository.find_user_by_email.return_value = existing_user
    with pytest.raises(ValueError, match="Email already in use"):
        user_service.register_user(username, email, password)
