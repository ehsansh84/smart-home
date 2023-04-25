docker rm -f smart
docker build -t smart:latest .
docker run -d -p 8000:8000 --name smart smart:latest
