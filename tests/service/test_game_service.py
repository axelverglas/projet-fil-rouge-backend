import pytest
from unittest.mock import ANY, MagicMock
from src.service.game_service import GameService
from src.model.tictactoe import TicTacToe
from src.model.connectfour import ConnectFour

@pytest.fixture
def mock_game_repository(mocker):
    return mocker.MagicMock()

@pytest.fixture
def game_service(mock_game_repository):
    return GameService(mock_game_repository)

def test_create_game_tictactoe(game_service, mock_game_repository):
    player1_id = "player1"
    player2_id = "player2"
    mock_game = TicTacToe(player1_id, player2_id)
    mock_game_repository.create_game.return_value = str(mock_game._id)

    game_id = game_service.create_game(player1_id, player2_id, "tictactoe")
    assert game_id is not None
    mock_game_repository.create_game.assert_called_once_with(ANY)

def test_create_game_connectfour(game_service, mock_game_repository):
    player1_id = "player1"
    player2_id = "player2"
    mock_game = ConnectFour(player1_id, player2_id)
    mock_game_repository.create_game.return_value = str(mock_game._id)

    game_id = game_service.create_game(player1_id, player2_id, "connectfour")
    assert game_id is not None
    mock_game_repository.create_game.assert_called_once_with(ANY)

def test_get_game_tictactoe(game_service, mock_game_repository):
    game_id = "game1"
    player1_id = "player1"
    player2_id = "player2"
    mock_game_data = {
        "_id": game_id,
        "player1_id": player1_id,
        "player2_id": player2_id,
        "board": ["", "", "", "", "", "", "", "", ""],
        "current_turn": player1_id,
        "state": "ongoing",
        "winner": None,
        "game_type": "tictactoe"
    }
    mock_game_repository.find_game_by_id.return_value = mock_game_data

    game = game_service.get_game(game_id, "tictactoe")
    assert game is not None
    assert game.player1_id == player1_id
    assert game.player2_id == player2_id
    mock_game_repository.find_game_by_id.assert_called_once_with(game_id)

def test_get_game_connectfour(game_service, mock_game_repository):
    game_id = "game1"
    player1_id = "player1"
    player2_id = "player2"
    mock_game_data = {
        "_id": game_id,
        "player1_id": player1_id,
        "player2_id": player2_id,
        "board": [['', '', '', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '', '']],
        "current_turn": player1_id,
        "state": "ongoing",
        "winner": None,
        "game_type": "connectfour"
    }
    mock_game_repository.find_game_by_id.return_value = mock_game_data

    game = game_service.get_game(game_id, "connectfour")
    assert game is not None
    assert game.player1_id == player1_id
    assert game.player2_id == player2_id
    mock_game_repository.find_game_by_id.assert_called_once_with(game_id)

def test_get_game_not_found(game_service, mock_game_repository):
    game_id = "game1"
    mock_game_repository.find_game_by_id.return_value = None

    with pytest.raises(ValueError):
        game_service.get_game(game_id, "tictactoe")

def test_make_move_tictactoe(game_service, mock_game_repository):
    game_id = "game1"
    player1_id = "player1"
    player2_id = "player2"
    mock_game_data = {
        "_id": game_id,
        "player1_id": player1_id,
        "player2_id": player2_id,
        "board": ["", "", "", "", "", "", "", "", ""],
        "current_turn": player1_id,
        "state": "ongoing",
        "winner": None,
        "game_type": "tictactoe"
    }
    mock_game_repository.find_game_by_id.return_value = mock_game_data
    mock_game_repository.update_game.return_value = None

    game = game_service.make_move(game_id, player1_id, 0, "tictactoe")
    assert game.board[0] == "X"
    assert game.current_turn == player2_id
    mock_game_repository.update_game.assert_called_once_with(ANY)

def test_make_move_connectfour(game_service, mock_game_repository):
    game_id = "game1"
    player1_id = "player1"
    player2_id = "player2"
    mock_game_data = {
        "_id": game_id,
        "player1_id": player1_id,
        "player2_id": player2_id,
        "board": [['', '', '', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '', ''], ['', '', '', '', '', '', '']],
        "current_turn": player1_id,
        "state": "ongoing",
        "winner": None,
        "game_type": "connectfour"
    }
    mock_game_repository.find_game_by_id.return_value = mock_game_data
    mock_game_repository.update_game.return_value = None

    game = game_service.make_move(game_id, player1_id, 0, "connectfour")
    assert game.board[5][0] == "X"
    assert game.current_turn == player2_id
    mock_game_repository.update_game.assert_called_once_with(ANY)

def test_make_move_invalid(game_service, mock_game_repository):
    game_id = "game1"
    player1_id = "player1"
    player2_id = "player2"
    mock_game_data = {
        "_id": game_id,
        "player1_id": player1_id,
        "player2_id": player2_id,
        "board": ["X", "O", "X", "O", "X", "O", "X", "O", "X"],
        "current_turn": player1_id,
        "state": "finished",
        "winner": player1_id,
        "game_type": "tictactoe"
    }
    mock_game_repository.find_game_by_id.return_value = mock_game_data

    with pytest.raises(ValueError):
        game_service.make_move(game_id, player1_id, 0, "tictactoe")

def test_make_move_not_your_turn(game_service, mock_game_repository):
    game_id = "game1"
    player1_id = "player1"
    player2_id = "player2"
    mock_game_data = {
        "_id": game_id,
        "player1_id": player1_id,
        "player2_id": player2_id,
        "board": ["", "", "", "", "", "", "", "", ""],
        "current_turn": player2_id,
        "state": "ongoing",
        "winner": None,
        "game_type": "tictactoe"
    }
    mock_game_repository.find_game_by_id.return_value = mock_game_data

    with pytest.raises(ValueError):
        game_service.make_move(game_id, player1_id, 0, "tictactoe")
