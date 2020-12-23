# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2020-12-24
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
