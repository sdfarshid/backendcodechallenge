### 1. How were you debugging this mini-project? Which tools?

I used different methods to debug this mini-project:

- First, I used the PyCharm debugger with breakpoints to stop and check parts of the code during runtime.
- I also added custom logger functions to track and log what happens in the program. These logs helped me follow the flow and find problems. You can find the logger code in the `utilities` folder.
- For some parts of the code, I checked the network activity in the browser developer tools to see the API requests and responses.

These tools helped me understand what the code was doing and fix issues step by step.
### 2. Please give a detailed answer on your approach to test this mini-project

Because the project is small, I used manual testing for most parts. I ran the app and checked if the features worked as expected.

Also, I created some unit tests for important parts, especially when I made many changes. I tried to connect smaller parts and then test the whole flow.

For example, when I worked on fetching data from GitHub, I first used `httpx` to send a basic request. I saw that it was slow, so I decided to use multithreading to make parallel requests. This helped the program to not be blocked and work faster.

After that, I tested smaller parts again to make sure everything worked correctly. So I used both manual and automated tests in this project.
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
