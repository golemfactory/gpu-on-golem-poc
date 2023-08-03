#### Local development
To run local environment you can use Docker Compose with [docker-compose.yaml](https://github.com/imapp-pl/pawnshop-app/blob/main/docker-compose.yaml "docker-compose.yaml") as a basic configuration. 
For local development we are using following containers:

| name             | build from     | description                                      |
|------------------|----------------|--------------------------------------------------|
| proxy            | nginx:latest   | Proxy server (TODO for production)               |
| load_balancer    | haproxy:latest | Load balancer for routing requests to requestors |
| postgres         | postgres:15    | Database                                         |
| redis            | redis:7        | Celery backend (TODO)                            |
| backend          | ./backend      | API                                              |
| requestor-worker | ./backend      | Celery worker running golem requestors (TODO)    |
| celery-beat      | ./backend      | Celery beat for cron jobs (TODO)                 |

#### Build
`./backend/build_docker.sh`

#### Configure
Create file named `.env` based on `.env-example` and adjust variables if needed.

#### Run
```
docker compose up -d
```

#### Setup
```
docker compose exec backend bash
./manage.py migrate
./manage.py createsuperuser 
```

Now check http://localhost:8000 if it works.

Admin panel is available at http://localhost:8000/admin/.
