                    Browser
                       |
                       |
                localhost:3000
                       |
                 +-------------+
                 |   Frontend  |
                 | React/Nginx |
                 +-------------+
                  /           \
                 /             \
        /api/dev/               /api/prod/
              /                   \
             v                     v
    +----------------+     +----------------+
    | Backend DEV    |     | Backend PROD   |
    | Flask          |     | Flask/Gunicorn |
    | Port 3001      |     | Port 3002      |
    +----------------+     +----------------+

           Docker Compose Network