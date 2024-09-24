from states import UserStates


class StateError(Exception):
    """State error"""

    def __init__(self, current_state: UserStates, expected_state: list[UserStates]) -> None:
        self.current_state = current_state
        self.expected_state = expected_state

    def __str__(self) -> str:
        return f'User has state «{self.current_state}», but one of the following needed: «{"», «".join(self.expected_state)}»'
