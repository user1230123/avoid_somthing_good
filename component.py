from typing import TYPE_CHECKING
from abc import abstractmethod

if TYPE_CHECKING: # Forward Reference Type Checking
    from object import GameObject

class Component:
    def __init__(self) -> None:
        pass

    def set_owner(self, owner: 'GameObject'):
        """
        Component의 owner를 지정합니다.
        GameObject에 의해 자동으로 초기화되므로 직접 호출하지 마십시오.
        """
        self.owner = owner

    @abstractmethod
    def update(self, dt: float):
        pass
