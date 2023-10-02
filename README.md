## Backend Coding Challenge 

In order to be considered for the Backend position, you must complete the following task. 

### Prerequisites

- Experience with PHP as well as Symfony or other frameworks (e.g. Laravel) 
- Database knowledge (MySQL, MongoDB, Postgres, etc.)

## Task

1. Fork this repository
2. Create a *source* folder to contain your code. 
3. In the *source* directory, please create a PHP web application
4. Your application should accomplish the following:

* Connect to the [Github API](http://developer.github.com/)

* Find the [nodejs/node](https://github.com/nodejs/node) repository

* Find the 1000 most recent commits (only hashes)

* Create a model and store the 1000 most recent commits in the database. Make sure to avoid any duplicates.

* Create a route and view which displays the recent commits by author from the database. 

* Keep your solution flexible enought to be able to later on provide support for the bitbucket-api/gitlab-api etc...

  
### Once Complete
1. Create a SETUP.md in the base directory with setup instructions.
2. Create a private repository on GitHub and grant the access to jobs@circunomics.com.
3. Please let us know that you have completed the challege (send email to jobs@circunomics.com).

## Key Points We Are Looking For
* Scalable solution
* Ability to use libraries
* Ability to create basic model and retrieve information from the databse
* Use Composer
* Use Docker
* Needs to have tests
 
## Implementation and Conceptual Questions

Please answer this questions in a Markdown file and commit it to the repo.

Plase use english for the answers and you can use drawings for a better description

1. How were you debugging this mini-project? Which tools?
2. Please give a detailed answer on your approach to test this mini-project.
3. Imagine this mini-project needs microservices with one single database, how would you draft an architecture? 
4. How would your solution differ when all over the sudden instead of saving to a Database you would have to call another external API to store and receive the commits.
  
