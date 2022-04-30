# -*- coding: utf-8 -*-

"""
    Example of gym_tetris environment usage with random actions agent
"""

import os
import numpy as np
import gym
from gym import spaces
import gym_tetris.tetris_engine as game

os.environ["SDL_VIDEODRIVER"] = "dummy"

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480


class TetrisEnv(gym.Env):
    """Custom tetris gym environment class"""

    # changing here "render.modes" to "render_modes" ->
    # -> as in env docs crashes everything
    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(self, state_mode="matrix"):
        """Open up a game state to communicate with emulator"""
        self.game_state = game.GameState()
        self._action_set = self.game_state.getActionSet()
        self.action_space = spaces.Discrete(len(self._action_set))
        self.state_mode = state_mode
        if self.state_mode == "matrix":
            # now each state is a matrix 20x10
            self.observation_space = spaces.Box(low=0, high=2, shape=(200,))
            self.frame_step = self.game_state.frame_step_mtr
        else:
            # now each state is an RGB picture
            self.observation_space = spaces.Box(
                low=0, high=255, shape=(SCREEN_HEIGHT, SCREEN_WIDTH, 3)
            )
            self.frame_step = self.game_state.frame_step
        self.viewer = None
        self._seed = 0

    def step(self, action):
        self._action_set = np.zeros([len(self._action_set)])
        self._action_set[action] = 1
        state, reward, terminal = self.frame_step(self._action_set)
        if self.state_mode == "matrix":
            # need to rotate state matrix for user convenience
            return (
                np.ravel(np.rot90(np.asarray(state), k=-1)),
                reward,
                terminal,
                {},
            )
        return state, reward, terminal, {}

    def _get_image(self):
        return self.game_state.getImage()

    @property
    def n_actions(self):
        return len(self._action_set)

    @property
    def state_shape(self):
        return self.observation_space.shape

    # return: (states, observations)
    def reset(self, **_):
        # same if-else as in __init__
        if self.state_mode == "matrix":
            self.observation_space = spaces.Box(low=0, high=2, shape=(20, 10))
            self.frame_step = self.game_state.frame_step_mtr
        else:
            self.observation_space = spaces.Box(
                low=0, high=255, shape=(SCREEN_HEIGHT, SCREEN_WIDTH, 3)
            )
            self.frame_step = self.game_state.frame_step
        do_nothing = np.zeros(len(self._action_set))
        do_nothing[0] = 1
        state, _, _ = self.frame_step(do_nothing)
        if self.state_mode == "matrix":
            # need to rotate state matrix for user convenience
            return np.ravel(np.rot90(np.asarray(state), k=-1))
        return state

    def render(self, mode="human", close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        img = self._get_image()
        if mode == "rgb_array":
            return img
        elif mode == "human":
            from gym.envs.classic_control import rendering

            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)
