# -*- coding: utf-8 -*-

import logging
import sys
import gym

# important import for env usage!
import gym_tetris
from gym.wrappers import monitor


class RandomAgent(object):
    """The world's simplest agent!"""

    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return self.action_space.sample()


if __name__ == "__main__":
    # logger setup
    logging.basicConfig()

    # You can optionally set up the logger. Also fine to set the level
    # to logging.DEBUG or logging.WARN if you want to change the
    # amount of output.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    OUTDIR = "/tmp/random-agent-results"

    env = gym.make("Tetris-v0" if len(sys.argv) < 2 else sys.argv[1])
    env = monitor.Monitor(env, directory=OUTDIR, force=True)

    # This declaration must go *after* the monitor call, since the
    # monitor's seeding creates a new action_space instance with the
    # appropriate pseudorandom number generator.
    agent = RandomAgent(env.action_space)

    EPISODE_COUNT = 100
    MAX_STEPS = 200
    reward = 0
    done = False

    for i in range(EPISODE_COUNT):
        ob = env.reset()

        for j in range(MAX_STEPS):
            action = agent.act(ob, reward, done)
            ob, reward, done, _ = env.step(action)
            if done:
                break
            # Note there's no env.render() here.
            # But the environment still can open window and render
            # if asked by env.monitor: it calls env.render('rgb_array')
            # to record video.
            # Video is not recorded every episode,
            # see capped_cubic_video_schedule for details.

    # Dump result info to disk
    env.close()

    # Upload to the scoreboard. We could also do this from another
    # process if we wanted.
    logger.info("Successfully ran RandomAgent.")
    # gym.gym.upload(OUTDIR)
