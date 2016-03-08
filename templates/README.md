![MakeAlong](https://raw.githubusercontent.com/ltaziri/Hackbright-FinalProject/master/static/README_Images/Homepage.png)

# MakeAlong

#### Bringing the world together one project at a time. 
MakeAlong is a python web app created by Leilani Taziri as her Hackbright Academy capstone project. 
In the MakeAlong online community, crafters can create a group for a craft project and invite their friends to work through the project with them.       

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
Python, Flask, Jinja, SQLAlchemy, PostgresSQL, Javascript, JQuery, AJAX, Bootstrap, Delorean, Selenium, Twitter API, SendGrid API, Flask-Uploads, Chart.js, Flipchart.js

(Dependencies are listed in requirements.txt)

### <a name="user"></a>User Homepage
---
Crafters can opt into numerous groups based on their interests. Their homepage serves as a dashboard to view all participating groups. There is also a message board on the right that shows pending group invites and user admin messages. All of this information is retrieved from the PostgressSQL database via multiple SQLAlchemy database queries in Flask. 

![User Homepage](https://raw.githubusercontent.com/ltaziri/Hackbright-FinalProject/master/static/README_Images/User.png)

### <a name="group"></a>Group Homepage
---
Once on the group’s page, users can get information about the pattern that the group is working on (either via a link or a downloadable PDF) and information about other users in the group. As users progress through a pattern they can post comments, photos and videos to the comment area of the group page. The contents of each comment are stored to the PostgressSQL database so they will be shown for the duration of the group. Users can also see a Twitter feed of the group's hashtag which is achieved via an API call to the Twitter API. 

![Group Homepage](https://raw.githubusercontent.com/ltaziri/Hackbright-FinalProject/master/static/README_Images/group.png)

### <a name="patternpoll"></a>Creating a Pattern Poll
---
To start a group, a user selects a pattern for the group or creates a pattern poll in which other members can vote on a selection of patterns. The user chooses how many days they want the poll to stay open and at the end of that time period, or when everyone in the group has voted, they can approve the winning pattern. While pattern voting is in process, the pattern poll is rendered on the group page using chart.js and vote information from an AJAX call to the server. The flip clock is rendered with flipclock.js and an AJAX call to the server to get a calculation of the time remaining for the poll. 

![Vote](https://github.com/ltaziri/Hackbright-FinalProject/blob/master/static/README_Images/voting.gif?raw=true)

###  <a name="invite"></a>Sending an Invite
---
From the group page, more users can easily be invited using the invite form. Upon submission an email is sent to the invitee using the SendGrid API. 

###  <a name="userexperience"></a>Improving User Experience
---
The goal of MakeAlong is to create an interactive experience that promotes and encouranges participants to participate in groups. In order to improve the user's experience, a number of javascript enhancements have been added to make interaction seamless. 
1. Modal windows for the user profile/profile update as well as the invite form allowing the user to view and update information without needing to navigate to a new window. 
![Update Profile](https://github.com/ltaziri/Hackbright-FinalProject/blob/master/static/README_Images/Update_profile.gif?raw=true)

![Send Email](https://github.com/ltaziri/Hackbright-FinalProject/blob/master/static/README_Images/Send_invite.gif?raw=true)
2. Use of an AJAX call on the user homepage when a user accepts an invite. This AJAX call updates the database on the server side and renders the new group in the browser without requiring a page refresh. 
![Add Group](https://github.com/ltaziri/Hackbright-FinalProject/blob/master/static/README_Images/Accept_invite.gif?raw=true)
3. Advanced comment handling on the group page. Users can input both text and photos in the comments section. Additionally, text is parsed through to find all of the links in the text and convert them into clickable links. Lastly, YouTube links are identified and rendered in an embedded iframe. All of this is done via an AJAX call that sends the comment to the database and renders it in the browser.  
![Youtube](https://github.com/ltaziri/Hackbright-FinalProject/blob/master/static/README_Images/Youtube.gif?raw=true)

### <a name="v2"></a>Version 2.0
---
Ideas for the next version of a MakeAlong include implementing a friend's graph data structure that would connect users that have been in groups with each other. This would allow for a friends feed that could contain information on new groups that friends have started or joined and their twitter activity relating to all MakeAlong groups. 

### <a name="author"></a>Author
---
Leilani Taziri is a Software Engineering Fellow at Hackbright Academy. 

**Github** http://github.com/ltaziri   
**Linkedin** https://www.linkedin.com/in/leilanitaziri