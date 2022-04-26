# -*- coding: utf-8 -*-

"""
    Example of gym_tetris environment usage with random actions agent
"""

import logging
import gym

# important import for env usage!
import gym_tetris

# gym.wrappers.monitor is now deprecated ->
# -> so video_recorder and stats_recorder will be used
from gym.wrappers.monitoring import video_recorder, stats_recorder
import numpy as np


class RandomAgent:
    """The world's simplest agent!"""

    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, *_):
        """Randomly chooses an action from avaliable action space"""
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

    OUTDIR = "./../../random-agent-results"

    env = gym.make("Tetris-v0", state_mode="matrix")
    env.reset()
    # env = monitor.Monitor(env, directory=OUTDIR, force=True)
    vid = video_recorder.VideoRecorder(
        env=env, path=OUTDIR + "/tetris.mp4", enabled=True
    )
    stats = stats_recorder.StatsRecorder(
        directory=OUTDIR, file_prefix="tetris",
    )

    # This declaration must go *after* the monitor call, since the
    # monitor's seeding creates a new action_space instance with the
    # appropriate pseudorandom number generator.
    agent = RandomAgent(env.action_space)

    EPISODE_COUNT = 100
    MAX_STEPS = 200
    reward = 0
    done = False

    for i in range(EPISODE_COUNT):
        stats.before_reset()
        ob = env.reset()
        vid.capture_frame()
        # print(ob)
        stats.after_reset(ob)

        for j in range(MAX_STEPS):
            action = agent.act(ob, reward, done)
            stats.before_step(action)
            ob, reward, done, info = env.step(action)
            vid.capture_frame()
            # print(ob)
            stats.after_step(
                observation=ob, reward=reward, done=done, info=info
            )
            if done:
                break
            # Note there's no env.render() here.
            # But the environment still can open window and render
            # if asked by env.monitor: it calls env.render('rgb_array')
            # to record video.
            # Video is not recorded every episode,
            # see capped_cubic_video_schedule for details.
        stats.save_complete()

    # Dump result info to disk
    vid.close()
    stats.close()
    env.close()

    logger.info("Successfully ran RandomAgent.")
    # Upload to the scoreboard. We could also do this from another
    # process if we wanted.
    # gym.gym.upload(OUTDIR)
