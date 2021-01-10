from setuptools import find_packages, setup  # type: ignore[import]

setup(
    name="anime-ml",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyspark==3.0.1",
        "seaborn"
    ],
    url="https://github.com/thesammy2010/anime-ml",
    license="APACHE LICENSE, VERSION 2.0",
    author="thesammy2010",
    author_email="leoparkesneptune+github@gmail.com",
    description="Basic ML on data from MyAnimeList",
)
