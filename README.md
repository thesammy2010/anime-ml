# anime-ml
> https://myanimelist.net/profile/TheSammy2010

> TheSammy2010's machine learning model decision model

> Goal: Make a model that, given an anime, will tell me whether I'll like it or not

depends on https://github.com/thesammy2010/oauth-redirect via Google Cloud Run

### High level steps:
1. Extract data from API
   1. authenticate
   2. request data
2. Transform data and build features
   1. create objects to represent the data
   2. create new features based on the data
   3. save features to a vector/matric/ML-friendly file
3. Make some models
   1. Linear regression
   2. Logistical regression
4. Show performance and results
    1. CLI with input
    2. Matplotlib/Seaborn to show affinity for results
