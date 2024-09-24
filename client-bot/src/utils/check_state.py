import logging
from models import User
from models.exceptions import StateError
from states import UserStates


def check_state(current_state: User.state, correct_states: list[UserStates]):
    if current_state not in correct_states:
        logging.exception(StateError(current_state, correct_states))
        raise StateError(current_state, correct_states)
