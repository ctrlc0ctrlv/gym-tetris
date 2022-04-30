from setuptools import setup, find_packages
import sys
import os.path

# Don't import gym module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "gym_tetris"))

setup(
    name="gym_tetris",
    version=0.2,
    description="This package allows to play Tetris as a gym environment.",
    url="https://github.com/ctrlc0ctrlv/gym-tetris",
    author="ctrlc0ctrlv",
    author_email="vrbyov12@gmail.com",
    license="",
    packages=[
        package for package in find_packages() if package.startswith("gym")
    ],
    zip_safe=False,
)
