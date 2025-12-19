from blocks import object_trigger

# 함부로 변경하지 마세요. 일부 하드코딩된 값들이 있습니다.

BALL = 1
PLATFORM = 2
SPIKE_BLOCK = 3
ELEVATOR_BLOCK = 4
GRAVITY_BLOCK = 5
COMPLETE_BLOCK = 6

collisionTriggerFuncs = {PLATFORM:object_trigger.platformBlockFunc,
                         SPIKE_BLOCK:object_trigger.spikeBlockFunc,
                         ELEVATOR_BLOCK:object_trigger.elevatorBlockFunc,
                         GRAVITY_BLOCK:object_trigger.gravityBlockFunc,
                         COMPLETE_BLOCK:object_trigger.completeBlockFunc}