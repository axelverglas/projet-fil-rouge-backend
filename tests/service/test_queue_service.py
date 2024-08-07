import pytest
from unittest.mock import MagicMock
from bson import ObjectId
from src.service.queue_service import QueueService

@pytest.fixture
def mock_queue_repository():
    return MagicMock()

@pytest.fixture
def mock_game_service():
    return MagicMock()

@pytest.fixture
def queue_service(mock_queue_repository, mock_game_service):
    return QueueService(mock_queue_repository, mock_game_service)

def test_find_or_create_game_create_new_game(queue_service, mock_queue_repository, mock_game_service):
    user_id = "user1"
    game_type = "tictactoe"
    
    # Configure mock to return None, indicating no opponent found
    mock_queue_repository.get_next_player.return_value = None

    result = queue_service.find_or_create_game(user_id, game_type)

    assert result == (None, None)
    mock_queue_repository.add_to_queue.assert_called_once_with(user_id, game_type)

def test_find_or_create_game_existing_opponent(queue_service, mock_queue_repository, mock_game_service):
    user_id = "user1"
    opponent_id = "user2"
    game_type = "tictactoe"
    game_id = str(ObjectId())
    mock_game = MagicMock()
    mock_game._id = game_id
    
    # Configure mock to return an existing opponent
    mock_queue_repository.get_next_player.return_value = opponent_id
    mock_game_service.create_game.return_value = mock_game

    result = queue_service.find_or_create_game(user_id, game_type)

    assert result == (mock_game._id, opponent_id)
    mock_game_service.create_game.assert_called_once_with(opponent_id, user_id, game_type)
