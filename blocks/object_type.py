from blocks import object_trigger

BALL = 1
PLATFORM = 2
SPIKE_BLOCK = 3
ELEVATOR_BLOCK = 4

collisionTriggerFuncs = {PLATFORM:object_trigger.platformBlockFunc,
                         SPIKE_BLOCK:object_trigger.spikeBlockFunc,
                         ELEVATOR_BLOCK:object_trigger.elevatorBlockFunc}