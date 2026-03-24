# ScalabixMedical Deployment 🚀

> Welcome! In this guide, I’ll demonstrate how to deploy the ScalabixMedical microservices backend API (FastAPI) using GitHub Actions with a complete CI/CD workflow. CI/CD (Continuous Integration and Continuous Deployment) helps automate the development process, making it faster, more reliable, and easier to maintain.

### Setup:

#### Dependencies

- Create IAM user 
    - Then assign administrator permission to the user.
    - After that, navigate to the security credentials section to create access keys.
    - Finally, you can see and copy the Access Key ID and Secret Access Key.

- Create EC2 machine
- Create ECR (Elastic Container Registry) repositories for your microservices (e.g., `user-api` and `doctor-api`)

###### Install Docker on EC2 machine:

```bash
sudo apt-get update
sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
sudo chown $USER /var/run/docker.sock
```

> Download Docker Compose as binary

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
docker-compose version
```

### GitHub Repo Settings
> Go to the GitHub repo settings -> Actions -> Runners. After that, select Ubuntu and paste the setup commands into your EC2 terminal. 
> 
> Once the runner is successfully connected to your EC2 instance, populate the following Environment Secrets under the `Secrets and variables -> Actions` menu:

- `AWS_ACCESS_KEY_ID` = *your access key value*
- `AWS_SECRET_ACCESS_KEY` = *your secret key value*
- `AWS_REGION` = *ap-south-1* *(adjust to your region)*
- `AWS_ECR_LOGIN_URI` = *<your-aws-account-id>.dkr.ecr.ap-south-1.amazonaws.com*
- `ECR_REPOSITORY_NAME` = *scalabix-medical*

> If GitHub action runner goes offline manually via terminal:

```bash
cd actions-runner/
 ./run.sh
```

> Manually create the database node (if deploying the Postgres DB independently from docker-compose):

```bash
docker run -d \
  --name postgres_db \
  --network host \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -v pg_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15-alpine
```
*(Note: Use your `init-multiple-dbs.sh` script to recreate the `user_db` and `doctor_db` logical databases within this container)*

###### Local docker server run like this:

```bash
docker compose up -d --build
```

### Container Operations

> If you want to dive into a specific microservice container follow these instructions:

```bash
docker exec -it user_service_app /bin/sh
```
or for the Doctor Service:
```bash
docker exec -it doctor_service_app /bin/sh
```

> Only show clean formatted container status:
```bash
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Image}}"
```
