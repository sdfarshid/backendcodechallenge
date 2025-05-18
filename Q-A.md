### 1. How were you debugging this mini-project? Which tools?

I used different methods to debug this mini-project:

- I used the PyCharm debugger with breakpoints to stop and check the program during execution.
- I added a custom logger in the `utilities` folder. The logger helps to follow the program flow and catch any errors using `try/catch`.
- I used different log levels (like info and error) to better understand what happens at each step.
- For more advanced debugging, I used `docker exec` to enter the container and check running processes, logs, and the database state.  
  For example, I inspected the Postgresql file directly to see if the commits were saved correctly and if there were any duplicate entries.
- I also used browser network tools (DevTools) to see the API requests and responses and make sure the backend is working correctly.

These tools helped me find and fix problems more easily.
These tools helped me understand what the code was doing and fix issues step by step.
### 2. Please give a detailed answer on your approach to test this mini-project


Because the project is small, I mostly used manual testing. I ran the app and checked if the main features worked as expected.

I also created unit tests for important parts of the project, especially when I made many changes. I tested small components first and then checked how they worked together as a full flow.

For example, when I was working on fetching data from GitHub, I used `httpx` to send a simple request. I noticed it was very slow, so I added multithreading to make parallel requests. This helped make the process faster and prevented blocking.

To be sure the requests were running in parallel, I wrote tests for that part too. I also monitored the request times using HTTP logs to compare before and after changes.

Later, I added integration tests to check the full behavior of my services. These tests helped me make sure everything works together correctly, from fetching commits to saving and displaying them.

So, in this project, I used both manual testing and automated testing (unit and integration).

### 3. Imagine this mini-project needs microservices with one single database; how would you draft an architecture?

I tried to build this project based on Domain-Driven Design (DDD), and my goal was to make it ready for a microservice architecture. But because of time limits, I couldn't fully complete the structure.

In my previous project (an e-commerce platform), I used a similar approach with Microservices, DDD, and CQRS. You can see that project here:  
[https://github.com/sdfarshid/Microservice-DDD-CQRS](https://github.com/sdfarshid/Microservice-DDD-CQRS)

If we want to expand this current project into microservices (with one shared database), I would split it into services like:

- **Fetcher Service**: handles GitHub communication and gets commit data  
- **Author Service**: manages authors  
- **Commit Service**: stores and shows commits  
- **Frontend Service**: shows data to the user

All services use the same **Shared Database** (like PostgreSQL or even SQLite for testing).

I also recommend adding an **API Gateway**. This helps to:
- route requests to the correct service,
- manage access and authentication,
- support caching,
- collect logs and monitor traffic.

Because the services share some domain logic and command/query definitions (especially in DDD), we should create a `shared` folder or module. This way, we don’t duplicate the same logic across services.

Another possible solution is to use an **event-driven architecture** instead of direct API communication. For example, services can publish and listen to events using tools like RabbitMQ or Kafka. When one service finishes a task, another service can react by receiving the event. This makes services more independent (decoupled).

However, because we still use a shared database, we need a good data manager or some central control to make sure everything stays consistent.
### 4. How would your solution differ if, instead of saving to a Database, you had to call another external API to store and receive the commits?

Because I used a DDD structure, the main business logic will not change.

I already defined repository interfaces in the domain layer, so I can just create a new repository class in the `infrastructure` layer. This new class will call the external API instead of the database.

Since I used dependency injection and the Dependency Inversion Principle, I don’t need to change my services or handlers. I just swap the implementation.

For example, the new repository will act as an adapter: it will fetch data from the external API and convert it into my internal model structure.

Then the existing services like `AuthorService` and `CommitService` can use this new repository without any change.

So the only change will be at the infrastructure level, and the rest of the system will keep working the same way.
