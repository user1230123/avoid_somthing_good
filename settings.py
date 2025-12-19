import utils

BALL_RADIUS = 10
BALL_JUMP_CORRECTION = 3
BALL_JUMP_POWER = 400

GRAVITY_BLOCK_TEXTURE_TUPLE = (utils.imageLoad("block_textures","gravity.png"), utils.imageLoad("block_textures","gravity_inversed.png"))

# 가로 32개 , 세로 18개 블록 기준
BLOCK_SIZE = (40,40)