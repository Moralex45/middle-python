from typing import Optional

from src.core.in_models.base import Base


class Logout(Base):
    all_devices: Optional[bool]
