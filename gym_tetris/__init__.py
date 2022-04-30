from gym.envs.registration import register
# important import
from gym_tetris.tetris_env import TetrisEnv

# Pygame
# ----------------------------------------
register(
    id="Tetris-v0",
    entry_point="gym_tetris:TetrisEnv",
    kwargs={},
    # changed timestep_limit to max_episode_steps
    max_episode_steps=1000,
    nondeterministic=False,
)
