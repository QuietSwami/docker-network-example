# Docker Container Basics: Understanding Bridge and Overlay Networks

## Objectives

- Learn the differences between **Bridge** and **Overlay** networks in Docker.
- Understand how containers in different networks can communicate.

## Introduction to Docker Networks

Docker networks allow containers to communicate with each other. There are different types of networks, but we'll focus on two:

1. **Bridge Network:** Works on a single Docker host (your computer or server). Containers in the same bridge network can communicate, while those in different bridge networks need some special setup to talk to each other.

2. **Overlay Network:** Designed for Docker Swarm, which allows containers on different physical or virtual machines to communicate as if they are on the same network.

### When to Use Each Network

- **Bridge Network:** Use this when all your containers are on the same machine.
- **Overlay Network:** Use this when your containers are spread across multiple machines (in a Docker Swarm).

Now, let's look at some examples to make this clearer.

## Example 1: Using a Bridge Network

In this example, we’ll set up a simple application with three containers: one RabbitMQ service and two other services (app1 and app2). We'll connect these services using two separate bridge networks.

### Bridge Network Docker Compose File

Here’s the `docker-compose.yaml` file for setting up our containers:

```yaml
version: '3.8'

services:
  rabbitmq:
    image: rabbitmq:3-management
    container_name: rabbitmq
    ports:
      - "5672:5672"     # RabbitMQ default messaging port
      - "15672:15672"   # RabbitMQ management console
    networks:
      - app-network-1
      - app-network-2

  app1:
    image: franciscomendonca/auto-messaging:1.0.1
    restart: on-failure
    environment:
      - START_WITH_MESSAGE=true   # Start by sending a message
      - RABBITMQ_HOST=rabbitmq
    depends_on:
      - rabbitmq
    networks:
      - app-network-1

  app2:
    image: franciscomendonca/auto-messaging:1.0.1
    container_name: app2
    restart: on-failure
    environment:
      - START_WITH_MESSAGE=false  # Wait for a message before responding
      - RABBITMQ_HOST=rabbitmq
    depends_on:
      - rabbitmq
    networks:
      - app-network-2

networks:
  app-network-1:
    driver: bridge
    attachable: true
  app-network-2:
    driver: bridge
    attachable: true
```

### Running the Bridge Network Example

1. Save the above YAML code in a file named `docker-compose.yaml`.
2. Open your terminal and navigate to the directory containing `docker-compose.yaml`.
3. Run the following command to start the services:
    ```bash
    docker-compose up -d
    ```
4. To check if everything is running smoothly, use:
    ```bash
    docker ps
    ```
5. To see logs for any service (e.g., `app1`):
    ```bash
    docker logs app1
    ```

This setup allows `app1` and `app2` to communicate with `rabbitmq` because they are attached to networks (`app-network-1` and `app-network-2`). However, since they are on different bridge networks, they can't directly communicate with each other unless we set up additional network rules.

## Example 2: Using an Overlay Network in Docker Swarm

### What Is an Overlay Network?

An overlay network allows containers to communicate across different machines (nodes) in a Docker Swarm. You can think of it as a virtual network that spans across multiple Docker hosts.

### Prerequisites for Overlay Networks

You need a Docker Swarm cluster with at least three virtual machines (VMs). Let’s call them **VM1**, **VM2**, and **VM3**. You can use cloud services (like AWS or Azure) or local VMs.

### Overlay Network Docker Compose File

Here’s the `docker-compose.yaml` for the overlay network setup:

```yaml
version: '3.8'

services:
  rabbitmq:
    image: rabbitmq:3-management
    container_name: rabbitmq
    ports:
      - "5672:5672"     # RabbitMQ default messaging port
      - "15672:15672"   # RabbitMQ management console
    networks:
      - app-network-1
      - app-network-2

  app1:
    image: franciscomendonca/auto-messaging:1.0.1
    restart: on-failure
    environment:
      - START_WITH_MESSAGE=true   # Start by sending a message
      - RABBITMQ_HOST=rabbitmq
    depends_on:
      - rabbitmq
    networks:
      - app-network-1

  app2:
    image: franciscomendonca/auto-messaging:1.0.1
    container_name: app2
    restart: on-failure
    environment:
      - START_WITH_MESSAGE=false  # Wait for a message before responding
      - RABBITMQ_HOST=rabbitmq
    depends_on:
      - rabbitmq
    networks:
      - app-network-2

networks:
  app-network-1:
    driver: overlay
    attachable: true
  app-network-2:
    driver: overlay
    attachable: true
```

### How to Set Up and Run the Overlay Network Example

1. **Create Virtual Machines (VMs):** Set up three VMs (VM1, VM2, VM3).
2. **Install Docker on Each VM:**
    ```bash
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```
    If you run into permission issues, use:
    ```bash
    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker
    ```
3. **Initialize Docker Swarm on VM1:**
    ```bash
    docker swarm init
    ```
    - Copy the command it gives (starting with `docker swarm join ...`) and run it on **VM2** and **VM3** to add them to the swarm.
4. **Copy the `docker-compose.yaml` to VM1:**
    ```bash
    scp -i .ssh/<KEY_NAME> docker-compose.yaml <USER>@<VM1_IP>:/home/<USER>
    ```
5. **Deploy the Stack on VM1:**
    ```bash
    docker stack deploy -c docker-compose.yaml mystack
    ```
6. **Check the Status and Logs:**
    ```bash
    docker stack services mystack
    docker stack logs app1
    ```

And that's it! You've now deployed an application using Docker Swarm and overlay networks. In this setup, `app1` and `app2` can communicate across different VMs.

### Summary

- **Bridge Networks** are great for communication on a single Docker host.
- **Overlay Networks** enable container communication across multiple hosts in a Docker Swarm.
  
By following this tutorial, you should now have a basic understanding of how to use bridge and overlay networks in Docker!