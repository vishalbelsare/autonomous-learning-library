from setuptools import find_packages, setup

GYM_VERSION = "0.29.1"
PETTINGZOO_VERSION = "1.24.2"


extras = {
    "atari": [
        "gymnasium[atari, accept-rom-license]~={}".format(GYM_VERSION),
    ],
    "box2d": [
        "gymnasium[box2d]~={}".format(GYM_VERSION),
    ],
    "pybullet": [
        "pybullet>=3.2.2",
        "gym>=0.10.0,<0.26.0",
    ],
    "mujoco": [
        "gymnasium[mujoco]~={}".format(GYM_VERSION),
    ],
    "ma-atari": [
        "PettingZoo[atari, accept-rom-license]~={}".format(PETTINGZOO_VERSION),
        "supersuit~=3.9.1",
    ],
    "test": [
        "black>=24.1.1",  # linting/formatting
        "isort>=5.13.2",  # sort imports
        "flake8>=7.0.0",  # more linting
        "torch-testing>=0.0.2",  # pytorch assertion library
    ],
    "docs": [
        "sphinx>=3.2.1",  # documentation library
        "sphinx-autobuild>=2020.9.1",  # documentation live reload
        "sphinx-rtd-theme>=0.5.0",  # documentation theme
        "sphinx-automodapi>=0.13",  # autogenerate docs for modules
    ],
    "comet": [
        "comet-ml>=3.28.3",  # experiment tracking using Comet.ml
    ],
}

extras["all"] = (
    extras["atari"]
    + extras["box2d"]
    + extras["mujoco"]
    + extras["pybullet"]
    + extras["ma-atari"]
    + extras["comet"]
)
extras["dev"] = extras["all"] + extras["test"] + extras["docs"]

setup(
    name="autonomous-learning-library",
    version="0.9.1-alpha.4",
    description=("A library for building reinforcement learning agents in Pytorch"),
    packages=find_packages(),
    url="https://github.com/cpnota/autonomous-learning-library.git",
    author="Chris Nota",
    author_email="cnota@cs.umass.edu",
    entry_points={
        "console_scripts": [
            "all-atari=all.scripts.atari:main",
            "all-classic=all.scripts.classic:main",
            "all-continuous=all.scripts.continuous:main",
            "all-multiagent-atari=all.scripts.multiagent_atari:main",
            "all-plot=all.scripts.plot:main",
            "all-watch-atari=all.scripts.watch_atari:main",
            "all-watch-classic=all.scripts.watch_classic:main",
            "all-watch-continuous=all.scripts.watch_continuous:main",
            "all-watch-multiagent-atari=all.scripts.watch_multiagent_atari:main",
        ],
    },
    install_requires=[
        "gymnasium~={}".format(GYM_VERSION),  # common environment interface
        "numpy>=1.22.3",  # math library
        "matplotlib>=3.5.1",  # plotting library
        "opencv-python-headless>=4.0.0",  # used by atari wrappers
        "torch>=1.11.0",  # core deep learning library
        "tensorboard>=2.8.0",  # logging and visualization
        "cloudpickle>=2.0.0",  # used to copy environments
    ],
    extras_require=extras,
)
