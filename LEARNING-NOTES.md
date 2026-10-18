Learning Notes
What I learned from this assessment
Before doing this task, I understood Docker mainly from an infrastructure/support point of view. This exercise helped me understand how multiple application services can communicate inside the same Docker Compose network.

Development vs Production Backend
I created two Flask backend services.

Development:

Runs Flask directly
Uses port 3001
Debug mode is enabled
Production:

Runs with Gunicorn
Uses port 3002
Debug mode is disabled
This helped me understand why development and production services should not always use the same runtime configuration.

Docker Networking
One important thing I learned was that the frontend container does not need to find the backend using localhost.

Inside Docker networking it can communicate using service names:

backend-dev:3001 backend-prod:3002

Nginx proxies the requests to these services.

Ports
Host ports used in my deployment:

Frontend: 3000 Development backend: 3001 Production backend: 3002

The frontend container internally listens on port 80, therefore the Compose mapping is:

3000:80

Troubleshooting I performed
During testing I checked:

docker compose ps docker compose logs docker network inspect curl http://localhost:3001/health curl http://localhost:3002/health

These checks helped me separate container problems from application and network problems.

One thing I would improve
The ticket information is currently stored in memory.

If the backend container is restarted, newly created tickets are lost.

For a real application I would add persistent storage such as a database rather than keeping ticket data only in application memory.