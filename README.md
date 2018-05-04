# Honours - Project - Sentibrand 
This repository contains all the code and data used for the honours project:

** A real-time web application for brand analysis, that provides a visual sentiment analysis of Twitter’s content. ** 

## Functional Requirements that have been satisfied by the project:

### 3.1.1	User authentication:

* The user will be able to uniquely register to the Sentibrand.
* The user will be able to log in to the Sentibrand.
* The user will be able to edit his account within the system.
* The user will be able to log out of the application.

### 3.1.2	Single search (real-time phrase tracking):

* The user will only be able to access Single Search screen after he gets authenticated.
* The user will input a phrase that he is interested in into text field.
* The user will select an interval in seconds which will be used to pull tweets from Twitter.
* Collected data will be presented to the user on the following figures: map, charts, list of tweets,  and general statistics about the collected data including a number of tweets,  a number of collected locations and average polarity. of the data set.
  Points will be drawn on the heat map based on geolocation of tweet.
* The user will be able to see the most negative tweet.
* The user will be able to see the most positive tweet.
* The user will be able to quit the current search and start a new one.

### 3.1.3	Tracking and storing historic results:

* The user will be able to create and add up to 5 searched phrases.
* For each added phrase the user will be able to specify the name.
* For each added phrase the user will be able to specify the when the Sentibrand will start tracking the searched phrase.
* For each added phrase the user will be able to specify when the Sentibrand will stop tracking the searched phrase.
* Collected data will be presented to the user on the following figures: charts, list of tweets,  and general statistics about the collected data including number of tweets,  number of collected locations and average polarity.
  Points will be drawn on the map based on geolocation of tweet. (if provided)
* The user will be able to see the most negative tweet.
* The user will be able to see the most positive tweet.
* The user will be able to select a specific range of time from a slider.
* The user will only be able to access the page  after he gets authenticated.


## Main libraries and technologies used to develop the application:

* Python 3
* Django
* PostgreSQL
* Redis
* Celery
* jQuery
