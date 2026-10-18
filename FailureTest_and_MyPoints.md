Failure Test:
I stopped only the development backend to understand how service failure affects the application.
---

docker compose stop backend-dev

The development API became unavailable while the production backend remained independent.

I then restarted the development service:
---

docker compose start backend-dev

and confirmed its health endpoint again.



My Points:
---

What I would change for a real production deployment
This assessment is designed for local deployment, but for a real production environment I would consider:

Store tickets in a persistent database instead of application memory.
Keep secrets outside the Git repository.
Add HTTPS/TLS.
Restrict externally exposed backend ports.
Add centralized application logging and monitoring.
Add automated build and deployment testing.
Add persistent data backup and recovery