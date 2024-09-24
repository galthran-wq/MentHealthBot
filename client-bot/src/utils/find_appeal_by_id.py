from typing import Optional
from models import Appeal


def find_appeal_by_id(id: int) -> Optional[Appeal]:
    try:
        return Appeal.get_by_id(id)
    except Appeal.DoesNotExist:
        return None
