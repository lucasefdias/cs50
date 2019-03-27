# HarvardX CS50 - Problem Set 8 - Mashup

## Project Summary

Mashup is a web app that enables the user to search for a location and see the latest news for the nearest locations. It uses Google News and Google Maps APIs. This project currently works only for United States locations.

## Stack

Mashup was built using:

* FrontEnd: HTML (+Jinja), CSS (+Bootstrap), JavaScript (+jQuery and typeahead.js)
* Backend: Flask
* Database : SQL (sqlite)

## Project structure

### application.py
This is the main file for the app. It handles app and db configuration and manages all routes.

### helpers.py
This is a helper module that provides all custom functions to `application.py`.

### requirements.txt
File for all project requirements.

### US.txt
File containing all information for US locations (used for database creation).

### mashup.db
This is the database file. Stores all SQL tables for location information.

### /templates
Templates directory that contains all pages for the web app (for this single-page app, only `index.html`).

### /static
Static directory that contains all the CSS and JS.
