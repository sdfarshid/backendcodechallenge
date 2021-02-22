## Backend Code Challange 

In order to be considered for the Backend position, you must complete the following task. 

*Note: This task should take no longer than 2-3 hours at the most.*

### Prerequisites

- Experience with [PHP](http://www.php.net) Symfony framework
- Understanding of CSS frameworks and grid systems (Bootstrap, Pure, etc.)
- Database knowledge (MySQL, MongoDB, Postgres, etc.)

## Task

1. Fork this repository
2. Create a *source* folder to contain your code. 
3. In the *source* directory, please create a PHP web application using a Symfony framework
4. Your application should accomplish the following:
* Connect to the [Github API](http://developer.github.com/)
* Find the [nodejs/node](https://github.com/nodejs/node) repository
* Find the 25 most recent commits
* Create a model and store the 25 most recent commits in the database. Make sure to avoid any duplicates.
* Create a basic template and utilize a CSS framework (Bootstrap, Pure, etc.)
* Create a route and view which displays the recent commits by author from the database. 
* If the commit hash ends in a number, color that row light blue (#E6F1F6).
  
### Once Complete
1. Create a SETUP.md in the base directory with setup instructions.
2. Send us a pull request, we will review your code and get back to you

## Key Points We Are Looking For
* Demonstration of core MVC patterns
* Quality commit history
* Ability to use libraries
* Ability to create basic model and retrieve information from the databse
 
## Implementation and Conceptual Questions

Please answer this questions in a Markdown file and commit it to the repo.

Plase use english for the answers and you can use drawings for a better description (even pictures of by-hand drawings) 

1. How were you debugging this mini-project? Which tools?
2. How were you testing the mini-project?
3. Imagine this mini-project needs microservices with one single database, how would you draft an architecture? 

## Bonus Points
While not required any of the following will add some major bonus points to your submission:

* Setup an asset pipeline with Gulp, Grunt, etc.
* Use Angular
* Use Composer
* Use Docker
* Create a set of provsioning scripts with Puppet, Chef, Ansible, etc...
