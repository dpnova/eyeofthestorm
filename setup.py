from setuptools import find_packages, setup
import os.path

classifiers = [
    "Development Status :: 1 - Alpha",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]


setup(
    name="eyeofthestorm",
    version="0.1",
    packages=find_packages(),
    install_requires=["Twisted >= 12.1.0"],
    author="David Novakovic",
    author_email="dpn@dpn.name",
    classifiers=classifiers,
    description="A REST library for the Cyclone framework.",
    url="http://github.com/dpnova/eyeofthestorm",
    long_description=file('README.md').read()
)
