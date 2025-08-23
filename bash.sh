clear
docker-compose down
docker rmi backend-postgres
docker rmi backend-backend
docker-compose up --build
