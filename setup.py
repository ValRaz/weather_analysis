from setuptools import setup, find_packages

setup(
    name="weather_app",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages("src"),
)