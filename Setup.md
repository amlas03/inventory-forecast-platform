\# 🚀 Development Environment Setup Guide



This guide will help you set up your local development environment for the \*\*Inventory Forecast Platform\*\* project.



\## 📋 Prerequisites



Before starting, make sure you have:

\- A GitHub account with access to this repository

\- Windows/Mac/Linux machine

\- Internet connection



---



\## Step 1: Clone the Repository



Open your terminal (Git Bash on Windows, Terminal on Mac/Linux) and run:

```bash

\# Navigate to where you want the project

cd ~/Documents



\# Clone the repository

git clone https://github.com/amlas03/inventory-forecast-platform.git



\# Enter the project folder

cd inventory-forecast-platform

```



---



\## Step 2: Install Node.js and npm



\### Check if already installed:

```bash

node --version

npm --version

```



If you see version numbers (Node v18+ required), you're good! Skip to Step 3.



\### If not installed:

1\. Download from: \[https://nodejs.org/](https://nodejs.org/)

2\. Choose the \*\*LTS version\*\* (18.x or higher)

3\. Install and restart your terminal

4\. Verify installation:

```bash

node --version  # Should show v18.x or higher

npm --version

```



---



\## Step 3: Install Docker Desktop



\### Check if already installed:

```bash

docker --version

docker-compose --version

```



If you see version numbers, skip to Step 4.



\### If not installed:

1\. Download from: \[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

2\. Install Docker Desktop

3\. \*\*Start Docker Desktop\*\* (important!)

4\. Wait until Docker is fully running (whale icon in system tray)

5\. Verify installation:

```bash

docker --version

docker-compose --version

docker ps  # Should show an empty table

```



---



\## Step 4: Start PostgreSQL 15



Run this command to create and start the PostgreSQL container:

```bash

docker run --name dev-postgres -e POSTGRES\_PASSWORD=postgres123 -e POSTGRES\_DB=inventory\_db -p 5432:5432 -d postgres:15

```



\*\*What this does:\*\*

\- Creates a PostgreSQL 15 database

\- Password: `postgres123`

\- Database name: `inventory\_db`

\- Port: 5432



\### Verify it's running:

```bash

docker ps

```



You should see `dev-postgres` in the list with status "Up".



---



\## Step 5: Start Redis 7



Run this command to create and start the Redis container:

```bash

docker run --name dev-redis -p 6379:6379 -d redis:7

```



\*\*What this does:\*\*

\- Creates a Redis 7 cache

\- Port: 6379



\### Verify both containers are running:

```bash

docker ps

```



You should see both `dev-postgres` and `dev-redis` with status "Up".



---



\## Step 6: Configure Git Identity



Configure your Git identity (required for commits):

```bash

git config --global user.email "your-email@example.com"

git config --global user.name "Your Full Name"

```



\*\*Example:\*\*

```bash

git config --global user.email "john.doe@example.com"

git config --global user.name "John Doe"

```



---



\## ✅ Verification Checklist



Run these commands to verify everything is set up correctly:

```bash

\# Check Node.js

node --version          # Should show v18.x or higher



\# Check npm

npm --version           # Should show 9.x or higher



\# Check Docker

docker --version        # Should show Docker version



\# Check containers are running

docker ps               # Should show dev-postgres and dev-redis

```



---



\## 🔄 Daily Usage



\### Starting Docker containers (if stopped):

```bash

docker start dev-postgres

docker start dev-redis

```



\### Stopping Docker containers:

```bash

docker stop dev-postgres

docker stop dev-redis

```



\### Checking container status:

```bash

docker ps               # Shows running containers

docker ps -a            # Shows all containers (including stopped)

```



---



\## 🆘 Troubleshooting



\### Docker "cannot connect to daemon" error

\*\*Solution:\*\* Make sure Docker Desktop is running. Open Docker Desktop and wait for it to start.



\### Port already in use

\*\*Solution:\*\* Another service is using the port. Either:

\- Stop the conflicting service

\- Or change the port in the docker run command (e.g., `-p 5433:5432`)



\### "Permission denied" errors

\*\*Solution:\*\* Run your terminal as Administrator (Windows) or use `sudo` (Mac/Linux).



---



\## 📞 Need Help?



If you encounter any issues:

1\. Check this troubleshooting section

2\. Ask in the team Discord/Slack

3\. Check Docker Desktop logs (Settings → Troubleshoot)



---



\## 🎯 What's Next?



Once your environment is set up, you're ready to:

\- Set up the backend (Spring Boot)

\- Set up the frontend (React)

\- Set up the ML pipeline (Python)



Good luck! 🚀

