# Clearing PDF folder
rm -rf ./pdf

docker image rm webpagesdownloader_app
docker-compose up --build