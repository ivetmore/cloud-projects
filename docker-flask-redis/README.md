# Production Ready Flask API on AWS ECS (Fargate) with ALB and ElastiCache

This project is a containerized Flask API deployed to AWS using ECS (Fargate), an Application Load Balancer, and ElastiCache (Redis).

It demonstates how to take a simple local Docker app and deploy it using cloud infrastucture with secure networking and load balancing.

## Live Application:

Live application URL here: http://docker-flask-redis-alb-1836018808.us-east-2.elb.amazonaws.com

## Endpoints

- `/` - Returns a greeting message.
- `/count` - Redis-backed request counter.
- `/health` - Returns health check (Flask and Redis connectivity).
- `/metrics` - Returns request metrics.

Example `/health` reponse when Redis is unavailable:

```json

{"status":"DEGRADED","redis":"not connected}"
```


## Project Overview

This project demonstates deploying a containerized Flask API to AWS using production-style cloud architecture.

Instead of running locally with `docker run`, the app is:

-Built into a Docker image
-Pushed to Amazon ECR
-Deployed to Amazon ECS (Fargate)
-Exposed to the internet through an Application Load Balancer
-Connected to Amazon ElastiCache (Redis Serverless)

The goal of this project was to understand how containerized applications run in real cloud environments and how networking and security are configured between services.
 
## Architecture Overview

Internet
   ↓
Application Load Balancer (Port 80)
   ↓
ECS Service (Fargate)
   ↓
Docker Container (Flask App)
   ↓
Amazon ElastiCache (Redis Serverless)

## Networking and Security

-Internet traffic is allowed only to the ALB (Port 80).
-The ALB forwards traffic to ECS on Port 5000.
-ECS can connect to Redis on Port 6379.
-Direct public access to the ECS container is blocked.

This setup uses security group referencing to enforce least-privilege access between services.

## Technologies Used

The application is built with:
-Flask (Python API)
-Amazon ElastiCache (Redis Serverless)
-Docker
-Amazon ECS (Fargate)
-Amazon ECR
-AWS Security Groups and VPC Networking 
-Application Load Balancer (ALB)

## What I Learned

-How to deploy a Docker container to AWS ECS (Fargate).
-How Application Load Balancers route traffic to containers.
-How to integrate Redis using ElastiCache.
-How to configure security group sto control service-to-service access.
-How to debug cloud networking and deployment issues.
-How task defintiions and service revisions work in ECS.

## Notes

This app is designed to run in a degraded mode when Redis is not available (useful during development). In that case, `health` will return a DEGRADED status instead of failing entirely. 


