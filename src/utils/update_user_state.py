from models.user import User
from states import UserStates
from models import User


def update_user_state(user: User, state: UserStates) -> None:
    user.update(state=state).execute()
