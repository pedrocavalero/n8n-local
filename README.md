This project aims to run n8n locally using Docker.

## Prerequisites

- Docker
- Docker Compose

## How to run

1. Clone the repository
2. Run colima start
3. Run `docker-compose up -d`
4. Open `http://localhost:5678` in your browser

## How to stop

1. Run `docker-compose down`
2. Run `colima stop`

## How to restart

1. Run `docker-compose down`
2. Run `docker-compose up -d`
3. Open `http://localhost:5678` in your browser



