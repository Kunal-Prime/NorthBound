docker run hello-world
docker images
docker ps -a
docker run -it python:3.11 python
docker run -d -p 8080:80 --name web nginx
docker exec -it web bash
docker stop web
docker rm web