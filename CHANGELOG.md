# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2021-01-10

#### Added
- `analytics.py` to do some basic analysis on aggregate data and look at community recommendations
    - calculates most common genre, studio and how many shows are in currently watching over time and many more

#### Changed
- updated URL to capture more fields as per https://myanimelist.net/forum/?topicid=1886442&show=0#msg61649503
- added `anime_ml/data` to `.gitignore`

#### Removed
- initial ML with `scikit-learn` as will be transitioning to SparkML

#### Changed
- refactored the `model/model.py` file to allow for row-by-row users
- refactored the `model/objects.py` to remove unnecessary object hierarchy in place for a flat level object

#### Removed
- The `features.py` file as it is no longer needed


## [0.0.4] - 2020-12-26
#### Added
- added features in `models/features.pu`
- added genres to `models/objects.py`
- added methods in `main.py`

#### Changed
- refined methods in `request.py` due to API documentation

## [0.0.3] - 2020-12-23
#### Added
- requests methods inside `anime_ml/api/request` to get user profile, animelist and generic details about an API
- added a fixture in `anime_ml/model` to represent what an Anime object looks like from the API
- modelled the Anime object into Python Objects from the fixtures file
- added a directory `data` for data to be stored

#### Changed
- renamed folder `anime_ml/extract` to `anime_ml/api`

#### Removed
- docker folder as testing doesn't need to be in a Docker container


## [0.0.2] - 2020-12-23
#### Added
- Successful OAuth authorisation (via https://github.com/thesammy2010/oauth-redirect)
- Added token authorisation methods (modified from https://gitlab.com/-/snippets/2039434)

#### Removed
- Username and Password environment variables as all requests go through OAuth and the @me endpoint
can be used to obtain a user's details

## [0.0.1] - 2020-12-23
#### Added / Completed
- Initialised repo
- Generated OAuth2 tokens on https://myanimelist.net/
