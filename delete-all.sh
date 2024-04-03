docker container rm postgres_db
docker container rm django
docker container rm react


docker network rm client-server
docker network rm backend

docker volume rm docker_db_data