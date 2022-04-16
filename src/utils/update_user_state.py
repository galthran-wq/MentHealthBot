from states import UserStates
from models import User


def update_user_state(user: User, state: UserStates) -> None:
    if user.state != state:
        user.state = state
        user.save(only=[User.state])
