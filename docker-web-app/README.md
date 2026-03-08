This is a simple Flask application running in a Docker container.

#Simple Dockerized Flask App:

Features:

-This was built with Python 3.12 and Flask
-Dockerized for easy deployment
-Returns a simple message at `/` endpoint

#How To Run Using Docker:

```bash
docker build -t flask-portfolio-app .
docker run -p 5000:5000 flask-portfolio-app

##Health Endpoint:

Check if the app is running:

```bash
curl http://localhost:5000/health
