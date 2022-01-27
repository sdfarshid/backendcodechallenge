## Backend Coding Challenge 

In order to be considered for the Backend position, you must complete the following task. 

### Prerequisites

- Experience with [PHP](http://www.php.net), Symfony or other frameworks (e.g. Laravel) 
- Database knowledge (MySQL, MongoDB, Postgres, etc.)
- Basic understanding of HTML/CSS

## Task

1. Fork this repository
2. Create a *source* folder to contain your code. 
3. In the *source* directory, please create a PHP web application using a Symfony framework
4. Your application should accomplish the following:

* Connect to the [Github API](http://developer.github.com/)

* Find the [nodejs/node](https://github.com/nodejs/node) repository

* Find the 1000 most recent commits

* Create a model and store the 1000 most recent commits in the database. Make sure to avoid any duplicates.

* Create a basic template and utilize plain HTML/CSS or Bootstrap

* Create a route and view which displays the recent commits by author from the database. 

* If the commit hash ends in a number, color that row light blue (#E6F1F6).

* Keep your solution flexible enought to be able to later on provide support for the bitbucket-api/gitlab-api etc...

  
### Once Complete
1. Create a SETUP.md in the base directory with setup instructions.
2. Please let us know that you have completed the challege and grant access to the repo to jobs@circunomics.com

## Key Points We Are Looking For
* Scalable solution
* Ability to use libraries
* Ability to create basic model and retrieve information from the databse
* Use Composer
* Use Docker
* Quality commit history
 
## Implementation and Conceptual Questions

Please answer this questions in a Markdown file and commit it to the repo.

Plase use english for the answers and you can use drawings for a better description (even pictures of by-hand drawings) 

1. How were you debugging this mini-project? Which tools?
2. How were you testing the mini-project?
3. Imagine this mini-project needs microservices with one single database, how would you draft an architecture? 
4. How would your solution differ when all over the sudden instead of saving to a Database you would have to call another external API to store and receive the commits.


## Bonus Points
While not required any of the following will add some major bonus points to your submission:

* Setup an asset pipeline with Gulp, Grunt, etc.

* Create a set of provsioning scripts with Puppet, Chef, Ansible, etc...

* Functional and/or unit test