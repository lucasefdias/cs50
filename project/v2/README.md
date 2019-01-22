# HarvardX CS50 - Week 11 - Final Project - Stage 50


## Student: Lucas Emidio Fernandes Dias
## edX ID: Lucasefdias
## Course: Harvard: CS50 - CS50's Introduction to Computer Science


## Project Summary

STAGE 50 is a social network for music professionals. It enables their users to:

- Manage their account info (e-mail and password)
- Customize their profile with personal info, location, occupations, instruments and external pages (website, YouTube, Spotify and others)
- Connect with other users and manage connections
- Send private messages to other users
- Create, edit and delete posts to be exhibited to all users in their feed
- Create, edit and delete comments on user posts
- Search users by name, instrument, role, entity/band and location


## Stack

Stage 50 was built using:

- FrontEnd: HTML (+Jinja), CSS (+Bootstrap), JavaScript (+jQuery)
- Backend: Flask
- Database : SQL (sqlite)

## Project structure


### application.py

This is the main file for the app. It handles app and db configuration and manages all routes.

### helpers.py

This is a helper module that provides all custom functions to application.py.

### requirements.txt

File for all project requirements (Python modules).

### project.db

This is the database file. Stores all SQL tables for retrieving user information.

### /templates

Templates directory that contains all pages for the web app.

### /static

Static directory that contains all the CSS and JS.

### /static/profie_pics

Directory for storing all user profile pictures.


## Future Improvements

- Add "interests" entry to profile for better searchability.
- Add "music styles" entry to profile to better classify musical interest and user matching.
- Refactor application and structure everything using Blueprints to create independent packages.
  This aims for a more organized and maintainable application.
- Add icons to profile entries to make the application more visually appealing.