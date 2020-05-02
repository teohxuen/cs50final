# CS50 Final Project

## Fitness60

Fitness60 is a web app that tracks your work outs, your IPPT results and your long term goals.

## List of Pages
All pages has a random quote at the foot of the page. The quote act to serve as a form of motivation. The quotes are obtained from type.fit's API and JS chooses a random quote for display

### Login Page
Logs in the users by checking if the hashed password and username matches the one in the database

### Registration Page
Users provide their birthday and their IPPT targets while registering. Checks are done to ensure that all entries are valid and that there will not be 2 users with the same username

### Index Page
At the index page, the server checks if the user have any exercises added. If the user do not have any exercises added he is automatically redirected to the exercise page. On the other hand if the user already has exercises with targets added, the server will choose a random exercise in which the user has yet to hit their target and display it in a card with the gap to target and the target itself to motivate the user. 
The index page is where the users add their workouts. There is a dropdown list for the user to choose the exercise and he can enter the count and any notes. 

### Goals Page
The goals page allows users to add or update their goals. Additionally, the users goals are displayed below the form for easy references. There are checks to ensure that the entry are valid (e.g.: Goal Date cannot be before today's date)

### Statistics Page
This page shows a table with rows for each exercises form the users. It shows data like the users target for each exercise, how far the user is from the target, how much the user need to do everyday to catch up to the target. This page aims to spur the user on.

### History Page
The history page list out the user's workout. A message will appear to encourage the user to work out.

### IPPT Page
This page allows the users to add/calculate their IPPT result or update their IPPT goals. Below the form there is a table which shows the user's past IPPT results as well as their IPPT Goal. The IPPT result is calculated client-side. To calculate the result, the server determines the age of the user based on his birthday in the databse. The form validates and format the data to ensure that the data entered are valid.

### New Exercise Page
This page allows a user to add a new exercise along with the exercise's Goal and Goal Date. Checks are present to ensure that the data entered is valid.

### Log out Page
Logs the user out and clear the users sessions

## Files in this repository
app.py
* Runs the web app

database.py
* Create the databse for this web app

helper.py
* Includes the helper functions

/static
* Contains favicon for the webpage
* JS to calculate the IPPT score
* CSS File

/templates
* All the HTML pages


## Built with
Python3, Flask, SQLite3