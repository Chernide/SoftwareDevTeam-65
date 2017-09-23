# SoftwareDevTeam-65
**Team Name:** Aqua Blue   
**Members:** Krishna Dholakiya, Eoin Doherty, Austin Argueso-Nott, Denver Chernin, Albert Huang, Tyler Bagala  
**Description:**

  A web-based platform that displays unbiased political information relevant to user location. We will also provide information on local politicians, policies, and events. Based on zipcode and/or geolocation we will present a collection of local representatives and their platforms. We strive to achieve political literacy and increase political
engagement within our community. 

  As we make progress and gain experience this project will grow. We would like to have spectrum quizzes to tag the information presented to users. This will not bias our site as we will provide information on both sides of every issue to insure well rounded political awareness. We will do rigorous research to insure that the news platforms we pull from will be credible and unbiased. The website will notify the users when upcoming elections are near making sure they are registered to vote and know of their local voting locations. 
  
**Vision Statement:**

We strive to achieve political literacy and increase political engagement locally and at a larger scale. 

**Motivation:**  

  With the recent presidential election being the first in which we could participate, we realized there is a certain level of noise surrounding the actual signal. In which we mean, there is a lot of information good and bad and filtering that information is difficult. Most news companies tend to focus on federal levels while local community government is just as important. 

**Risks:**

      1. Remaining unbaised
      2. APIs could potential have dirty data/not enough data 
      3. User information security (can be linked to political affliation) 
      4. Identifying political affliation being inaccurate 

**Risk Mitigation Plan:**  
**Version Control:**  

  Our version control is going to be github and git. Using branches for each feature along with a testing branch. We want to use pull requests to merge each feature into testing branch with group approval. 
  
**Development Method:**  

  We plan on using the agile methodology. This will have a weekly scrum on Saturdays and a stand-up over Slack during the work week to keep group involvement. 
  
**Collaboration Tool:**  
 
  Our main collaboration tool is going to be Slack. Through slack we have implemented GitHub and Trello. We have created a GitHub channel to create a log of all activity. Trello is going to be used for organize, prioritize, delegate features and tasks. 
  
**Proposed Architecture:**  

We're planning on splitting this app up into two key components: the API layer and the front-end application. The API layer, which we plan on writing using some Python framework (such as [Flask](http://flask.pocoo.org/)), will grab relevant data from various existing APIs around the internet, and serve them at REST API endpoints. It'll also handle all interfacing with the MySQL database and authentication. The front-end application, written in HTML/CSS/JavaScript (likely using some framework like [React](https://facebook.github.io/react/)), will send the user's location to that API layer and receive relevant data, and will then display it in a clean, intuitive interface.
  
