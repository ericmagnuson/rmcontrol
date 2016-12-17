from setuptools import setup, find_packages

setup(
    # Application name:
    name="RMControl",

    # Version number (initial):
    version="1.0.1",

    # Application author details:
    author="Eric Magnuson",
    author_email="eric@ericmagnuson.me",

    # Packages
    packages=find_packages(exclude=['tests*']),

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/ericmagnuson/rmcontrol",

    license="LICENSE.txt",

    description="A python app to control an RM2 from BroadLink.",

    long_description=open("readme.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask",
        "broadlink"
    ],
)
