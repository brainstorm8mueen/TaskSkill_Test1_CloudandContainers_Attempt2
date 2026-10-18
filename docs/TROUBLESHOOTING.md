Troubleshooting Notes
Test 1 - Check containers
Command:

docker compose ps

Purpose: I used this to confirm whether all three containers were running.

Test 2 - Backend API verification
Commands:

curl.exe http://localhost:3001/health curl.exe http://localhost:3002/health

Purpose: This allowed me to test each backend independently of the React frontend.

Test 3 - Container logs
Command:

docker compose logs --tail=30

Purpose: If the frontend failed to connect, I could check whether the issue was coming from Nginx, development backend or production backend.

Test 4 - Docker networking
Command:

docker network ls docker network inspect

Purpose: I used this to verify that all three containers were attached to the same Docker network.