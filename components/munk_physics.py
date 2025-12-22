from component import Component
from typing import TYPE_CHECKING
import pymunk

if TYPE_CHECKING:
    from object import GameObject

class PhysicsComponent(Component):
    def __init__(self, body: pymunk.Body, shape: pymunk.Shape):
        super().__init__()
        self.body = body
        self.shape = shape
        self.isRemoved = True
        self.body.component = self  # Body에 컴포넌트 참조 저장

    def set_owner(self, owner: 'GameObject'):
        """Component의 owner를 지정하고 초기화합니다."""
        super().set_owner(owner)
        # GameObject 위치를 Pymunk Body 위치로 초기화
        self.body.position = owner.get_pos().x, owner.get_pos().y

    def update(self, dt: float):
        """Pymunk Body의 위치와 GameObject의 위치를 동기화합니다."""
        self.owner.set_pos(self.body.position)
        self.owner.set_rotation(self.body.angle)

    def add_to_space(self, space: pymunk.Space):
        """Space에 Body와 Shape를 추가합니다."""
        if self.isRemoved:
            space.add(self.body, self.shape)
            self.isRemoved = False

    def remove_from_space(self, space: pymunk.Space):
        """Space에서 Body와 Shape를 제거합니다."""
        if not self.isRemoved:
            space.remove(self.body, self.shape)
            self.isRemoved = True