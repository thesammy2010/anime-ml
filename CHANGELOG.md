# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - 2020-12-23
## Added
- requests methods inside `anime_ml/api/request` to get user profile, animelist and generic details about an API
- added a fixture in `anime_ml/model` to represent what an Anime object looks like from the API
- modelled the Anime object into Python Objects from the fixtures file
- added a directory `data` for data to be stored

## Changed
- renamed folder `anime_ml/extract` to `anime_ml/api`

## Removed
- docker folder as testing doesn't need to be in a Docker container


## [0.0.2] - 2020-12-23
## Added
- Successful OAuth authorisation (via https://github.com/thesammy2010/oauth-redirect)
- Added token authorisation methods (modified from https://gitlab.com/-/snippets/2039434)

## Removed
- Username and Password environment variables as all requests go through OAuth and the @me endpoint
can be used to obtain a user's details

## [0.0.1] - 2020-12-23
## Added / Completed
- Initialised repo
- Generated OAuth2 tokens on https://myanimelist.net/
