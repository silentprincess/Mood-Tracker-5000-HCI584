# Ponder
## Sarah Hernandez - Summer 2022 - HCI 584
### A mood tracking web application developed for HCI 584 at Iowa State University.

All logos and images/gfx were also created by me- please do not use them for any other purpose besides playing with my code or showing it to someone else.

**CHECK README FOR BASIC INSTRUCTIONS ON HOW TO USE APP/WALKTHROUGH**
**CODE NOTED WITH HOW IT WORKS**

In order to run the app, you must pip install the following packages via your terminal:

- flask
- flask_sqlalchemy
- flask_login
- flask_bcrypt
- flask_wtf
- wtforms
- email validator

Known issues and deficiencies are listed here:

1. (Major Issue) I could not figure out how to create a database linked to the user using SQLAlchemy, so I had to switch over to pandas for the sake of the project being finished. Lines 49-59 are essentially useless, because they are for a linked mood database that does not exist. It's basically the skeleton of a table... you have to add the muscle. 

2. (Minor Issue) I could not figure out how to add the frog images to sit above the button. Might be a simple fix, not sure.

3. (Minor Issue) I think to be more efficient I could have automatically logged the user in after registering. 

4. (Major/Minor Issue) I did not get a chance to add an error message on the login page for if a password or username is entered incorrectly or does not exist. So if a user enters the wrong information, it goes nowhere but does not notify the user.

Future Work: 

- Definitely needs a lot of UI upgrades, just didn't have time to do them.

-Need to address the issues listed above. 








