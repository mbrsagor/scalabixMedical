# ScalabixMedical Version 1.0 Walkthrough

> This document outlines the architecture and implementation details for the ScalabixMedical hospital management system (Version 1.0), which includes two microservices: user_service and doctor_service.

#### Verification Instructions
> I have successfully fixed the Docker build issues and started the containers! The following issues have been resolved:
> 1. `PostgreSQL` initialization script had `#!/bin/bash` but Alpine uses `sh`.
> 2. `user_service` was missing `email-validator` for Pydantic's `EmailStr`.

> You can verify everything is working by checking the container logs or API endpoints:

```bash
git clone ...
cd scalabixMedical
docker compose up -d --build
```

> Check that the containers are healthy. You can use the logs command if there are issues:
```bash
docker compose logs -f
```

> API Endpoints for Verification:

```bash
User Service Health Check: http://localhost:8001/health
Doctor Service Health Check: http://localhost:8002/health
User Registration & Login: Use POST http://localhost:8001/api/v1/auth/register and POST http://localhost:8001/api/v1/auth/login to get a JWT token.
Create a Doctor Profile: Using the JWT token, use POST http://localhost:8002/api/v1/doctors/ with { "user_id": <id>, "specialization": "Cardiology" }. The Doctor service will transparently request authorization from the User service.
The OpenAPI Swagger UI is available at:

User Service UI: http://localhost:8001/docs
Doctor Service UI: http://localhost:8002/docs
```

##### Project structure:

```bash
scalabixMedical/
├── docker-compose.yml (Main orchestration)
├── postgres-init/
│   └── init-multiple-dbs.sh (Creates user_db and doctor_db)
├── user_service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   └── app/
│       ├── api/          (API endpoints/Routers)
│       ├── core/         (Config, Settings, Security)
│       ├── db/           (Database Connection, Session)
│       ├── models/       (SQLAlchemy Models)
│       ├── repositories/ (Database Operations)
│       ├── schemas/      (Pydantic Models)
│       ├── services/     (Business Logic, HTTPX calls)
│       └── utils/        (Helper Functions)
└── doctor_service/
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py
    └── app/
        ├── api/
        ├── core/
        ├── db/
        ├── models/
        ├── repositories/
        ├── schemas/
        ├── services/     (Business Logic, HTTPX calls)
        └── utils/
└── appointment_service/
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py
    └── app/
        ├── api/
        ├── core/
        ├── db/
        ├── models/
        ├── repositories/
        ├── schemas/
        ├── services/     (Business Logic, HTTPX calls)
        └── utils/
```
