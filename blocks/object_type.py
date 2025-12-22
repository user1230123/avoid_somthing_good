from blocks import object_trigger

# 함부로 변경하지 마세요. 일부 하드코딩된 값들이 있습니다.

BALL = 1
PLATFORM = 2
SPIKE_BLOCK = 3
ELEVATOR_BLOCK = 4
GRAVITY_BLOCK = 5
COMPLETE_BLOCK = 6
JUMP_BLOCK = 7
GLASS_BLOCK = 8

collisionTriggerFuncs = {PLATFORM:object_trigger.platform_block_func,
                         SPIKE_BLOCK:object_trigger.spike_block_func,
                         ELEVATOR_BLOCK:object_trigger.elevator_block_func,
                         GRAVITY_BLOCK:object_trigger.gravity_block_func,
                         COMPLETE_BLOCK:object_trigger.complete_block_func,
                         JUMP_BLOCK:object_trigger.jump_block_func,
                         GLASS_BLOCK:object_trigger.glass_block_func
                         }