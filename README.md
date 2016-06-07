
![MakeAlong](https://raw.githubusercontent.com/ltaziri/Hackbright-FinalProject/master/static/README_Images/Homepage.png)


#### Bringing the world together one project at a time. 
MakeAlong is a python web app created by Leilani Taziri as her Hackbright Academy capstone project. In theMakeAlong online community, crafters can create a group for a craft project and invite their friends to work through the project with them.        

#### Demo now available

> http://makealong.herokuapp.com/
email login: demo@makealong.com
password: trydemo

*note: all actions that would trigger changes to the database have been disabled in the demo. You can still play around with the AJAX calls referenced in the [User Experience section](#userexperience) but the changes will go away on page refresh*

## Table of Contents
---
* [Technologies Used](#technologiesused)
* [User Homepage](#user)
* [Group Homepage](#group)
* [Creating a Pattern Poll](#patternpoll)
* [Sending an Invite](#invite)
* [Improving User Experience](#userexperience)
* [Version 2.0](#v2)
* [Author](#author)

### <a name="technologiesused"></a>Technologies Used 
---
Python, Flask, Jinja, SQLAlchemy, PostgreSQL, JavaScript, JQuery, AJAX, Bootstrap, Delorean, Selenium, TwitterAPI, SendGrid API, Flask-Uploads, Chart.js, Flipchart.js

(Dependencies are listed in requirements.txt)

### <a name="user"></a>User Homepage
---
Crafters can opt into numerous groups based on their interests. Their homepage serves as a dashboard to view all the groups they are participating in. There is also a message board that shows pending group invites and user admin messages. All of this information is retrieved from the Postgres database via multiple SQLAlchemy database queries in Flask. 

![User Homepage](https://raw.githubusercontent.com/ltaziri/Hackbright-FinalProject/master/static/README_Images/User.png)

### <a name="group"></a>Group Homepage
---
Once on the group’s page, users can get information about the pattern that the group is working on (either via a link or a downloadable PDF) and information about other users in the group. As users progress through a pattern they can post comments, photos and videos to the comment area of the group page. The contents of each comment are stored to the Postgres database so they will be shown for the duration of the group. Users can also see a Twitter feed of the group's hashtag which is achieved via an API call to the Twitter API. 

![Group Homepage](https://raw.githubusercontent.com/ltaziri/Hackbright-FinalProject/master/static/README_Images/group.png)

### <a name="patternpoll"></a>Creating a Pattern Poll
---
To start a group, a user selects a pattern for the group or creates a pattern poll which allows other members to vote on a selection of patterns. The admin user chooses how many days they want the poll to stay open and at the end of that time period, or when everyone in the group has voted, they can approve the winning pattern. While pattern voting is in process, the pattern poll is rendered on the group page using Chart.js and vote information from an AJAX call to the server. The flip clock is rendered with FlipClock.js and an AJAX call to the server to get a calculation of the time remaining for the poll. 

![Vote](https://github.com/ltaziri/Hackbright-FinalProject/blob/master/static/README_Images/voting.gif?raw=true)

###  <a name="invite"></a>Sending an Invite
---
From the group page, more users can easily be invited using the invite form. Upon submission an email is sent to the invitee using the SendGrid API. 

###  <a name="userexperience"></a>Improving User Experience
---
The goal of MakeAlong is to create an interactive experience that promotes and encouranges participants to participate in groups. In order to improve the user's experience, a number of javascript enhancements have been added to make interaction seamless. 


* Advanced comment handling on the group page. Users can input both text and photos in the comments section. Links in the text are parsed and converted into clickable links, and an embedded iframe preview of any YouTube links is rendered. All of this is done via an AJAX call that sends the comment to the database and renders it in the browser.  

 ![Youtube](https://github.com/ltaziri/Hackbright-FinalProject/blob/master/static/README_Images/Youtube.gif?raw=true)


* Modal windows for the user profile/profile update as well as the invite form allowing the user to view and update information without needing to navigate to a new window. 

 ![Update Profile](https://github.com/ltaziri/Hackbright-FinalProject/blob/master/static/README_Images/Update_profile.gif?raw=true)

 ![Send Email](https://github.com/ltaziri/Hackbright-FinalProject/blob/master/static/README_Images/Send_invite.gif?raw=true)


* Use of an AJAX call on the user homepage when a user accepts an invite. This AJAX call updates the database on the server side and renders the new group in the browser without requiring a page refresh. 

 ![Add Group](https://github.com/ltaziri/Hackbright-FinalProject/blob/master/static/README_Images/Accept_invite.gif?raw=true)



### <a name="v2"></a>Version 2.0
---
Ideas for the next version of a MakeAlong include implementing a friend's graph data structure that would connect users that have been in groups with each other. This would allow for a friend's feed that could contain information on new groups that friends have started or joined and their twitter activity relating to all MakeAlong groups. 

### <a name="author"></a>Author
---
Leilani Taziri is a Software Engineer in the San Francisco Bay Area and a recent graduate of Hackbright Academy. 

Hiring? 
Connect with Leilani:

**[GitHub - github.com/ltaziri](http://github.com/ltaziri)**

**[Linkedin - linkedin.com/in/leilanitaziri](https://www.linkedin.com/in/leilanitaziri)** 

**[Twitter - @leilani_taziri](https://twitter.com/leilani_taziri)** 