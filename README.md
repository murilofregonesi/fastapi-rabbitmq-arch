# Message Broker Application

Simple **API architecture** based on a **Producer** and a **Consumer** communicating through a message broker.

The main technologies involved are:
- [x] **FastAPI** as web framework
- [ ] **RabbitMQ** as message broker
- [x] **SQLAlchemy** as ORM
- [x] **Docker** as environment builder
- [ ] **Nginx** as HTTP server

## Running via Docker
- Create a `producer/.env` file based on the example available.
- Run `sudo docker-compose up --build --force` on the repository root.
- The producer API interface will be available on `http://0.0.0.0:8000/docs`
