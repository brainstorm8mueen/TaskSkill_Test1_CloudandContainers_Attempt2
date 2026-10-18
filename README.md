# Multi-Environment Ticket Management Deployment

Task Skill Test 1: Cloud and Containers, Attempt 2. This repository deploys three containers: a Flask development backend, a Gunicorn-hosted Flask production backend, and an optimized React/Nginx frontend.

## Architecture

```text
Browser -> localhost:3000 -> Nginx frontend
                              |-- /api/dev/*  -> backend-dev:3001
                              `-- /api/prod/* -> backend-prod:3002
Direct host access: localhost:3001 and localhost:3002
Docker bridge network: multienv-network
```

## Environment specification and assumptions

- Deployment target: local computer or Ubuntu EC2 instance.
- Docker Engine 24+ and Docker Compose v2 are recommended.
- Ports 3000, 3001, and 3002 must be available.
- Ticket data is in memory and resets when a backend container is recreated.
- The supplied `.env` files contain non-secret runtime settings only.
- The assessment lists `http://[IP]:300` once; this is treated as a typo because all other requirements specify frontend port **3000**.

## Quick start

```bash
git clone https://github.com/brainstorm8mueen/TaskSkill_Test1_CloudandContainers_Attempt2.git
cd TaskSkill_Test1_CloudandContainers_Attempt2
docker compose config
docker compose up --build -d
docker compose ps
```

Open:
- Frontend dashboard: `http://localhost:3000`
- Development page: `http://localhost:3000/dev`
- Production page: `http://localhost:3000/prod`
- Development backend: `http://localhost:3001/health`
- Production backend: `http://localhost:3002/health`

For EC2, replace `localhost` with the instance public IP or DNS name.

## Ubuntu / EC2 installation

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl git
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker "$USER"
```

Log out and back in after the group change. A `t3.small` or larger is a practical assessment host. In the EC2 security group, allow SSH TCP/22 only from your public IP and TCP/3000 from the evaluator's approved IP range. Ports 3001 and 3002 can remain private unless direct API evidence is required; if opened, restrict them to the evaluator's IP, not `0.0.0.0/0`.

## Verification

```bash
docker compose ps
curl -fsS http://localhost:3001/health
curl -fsS http://localhost:3002/health
curl -fsS http://localhost:3000/health
curl -fsS http://localhost:3000/api/dev/tickets
curl -fsS http://localhost:3000/api/prod/tickets
docker compose logs --tail=50 backend-dev backend-prod frontend
docker network inspect taskskill_test1_cloudandcontainers_attempt2_multienv-network
```

Expected: all containers are `Up`/healthy, health calls return healthy responses, and both ticket calls return their matching environment.

Create a ticket through the frontend or test directly:

```bash
curl -i -X POST http://localhost:3001/api/tickets -H 'Content-Type: application/json' -d '{"title":"Development API test"}'
curl -i -X POST http://localhost:3002/api/tickets -H 'Content-Type: application/json' -d '{"title":"Production API test"}'
```

## Troubleshooting

```bash
# Find port conflicts
sudo ss -lntp | grep -E ':3000|:3001|:3002'
# Rebuild without cache
docker compose build --no-cache
# Inspect status and logs
docker compose ps -a
docker compose logs --tail=100
# Clean restart (removes containers/network, not source files)
docker compose down
docker compose up --build -d
```

- Frontend shows connection error: verify both backend containers are healthy and inspect frontend/backend logs.
- Port already allocated: stop the conflicting process or change only the host side of the Compose mapping.
- EC2 page unavailable: verify the instance is running, Docker publishes `3000:80`, and the security group permits TCP/3000 from your source IP.
- Compose command missing: install the `docker-compose-plugin` package and use `docker compose`, not legacy `docker-compose`.

## Evidence and submission

Store genuine screenshots in `evidence/` using its checklist. Update `submission/submission-info.txt` if deploying to EC2, then replace `localhost` with the public IP/DNS and set the actual deployment status.

## VIVA points

- Compose creates one user-defined bridge network; services resolve one another by service name.
- Nginx serves the React production build and proxies `/api/dev` and `/api/prod` to the correct backend.
- Development runs Flask directly with debug enabled; production uses Gunicorn, two workers, and a non-root user.
- Health checks gate frontend startup and make service state visible.
- Environment-specific values are supplied with separate `.env` files.
- Backend validation returns HTTP 400 for a blank ticket title and JSON 404 responses for unknown endpoints.

## Stop the deployment

```bash
docker compose down
```
