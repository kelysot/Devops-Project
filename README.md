## Flask App with Auto Scaling, Load Balancer and S3 private bucket.
### Project Description

This project demonstrates a Flask web application that captures user details (name and email) and stores them in a database. 
<br/>
The application includes the following features:

1. Displays a personalized greeting to the user.
2. Shows an image stored in an S3 bucket.
3. Dockerized for containerized deployments.
4. Deployed on an EC2 instance with auto-scaling and load balancing.
5. Accesses a private S3 bucket using IAM roles.


### Table of Contents
- [Prerequisites](#prerequisites)
- [Create Template](#create-template)
- [Create Auto Scaling](#create-auto-scaling)
- [Create Load Balancer](#create-load-balancer)
- [Final Results](#final-results)


### Prerequisites
- python 3
- pip
- Flask
- Docker
- AWS account with access to EC2, S3, and IAM services
- Git
  

### Create Template
- **Operating System:** Amazon Linux 2
- **Instance Type:** t2.micro
- **IAM Role:**
  Assign the `S3ReadOnlyAccess` permission to the instance role
![ec2 role](/images/ec2-role.png)

  
- **User data:**

  ```
  #!/bin/bash
  
  
  # Update package lists and install git and Docker
  sudo yum update -y
  sudo yum install git -y
  sudo yum install docker -y 
  
  # Start and enable Docker service
  sudo systemctl start docker
  sudo systemctl enable docker
  sudo yum update -y
  
  # Install and start docker-compose 
  sudo curl -L "https://github.com/docker/compose/releases/download/v2.11.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
  
  # Clone the project repository
  git clone https://github.com/kelysot/Devops-Project.git
  
  # Navigate to the project directory
  cd Devops-Project
  
  # Set up environment variables in .env file
  echo "S3_BUCKET_NAME=YOUR_BUCKET_NAME" >> .env
  echo "S3_IMAGE_KEY=YOUR_IMAGE_NAME" >> .env
  
  # Run the docker-compose file
  sudo docker-compose up --build
  ```
Remember to swap **YOUR_BUCKET_NAME** and **YOUR_IMAGE_NAME** with your real bucket and image names!


- Ensure the S3 bucket is private.
![block public access](/images/block-public-access.png)

- If you try using the url of the image you will receive this error:
![access denied](/images/access-denied-s3.png)
  

    
      
- **Security Group:**
  - Allow inbound traffic on ports 22 (SSH), 80 (HTTP), and 5555 (application).
![security group](/images/security-group.png)


### Create Auto Scaling

![auto scaling](/images/auto-scaling.png)

You should see your instances scale up:
![running ec2](/images/running-ec2.png)


### Create Load Balancer

![load balncer path](/images/load-balncer-path.png)

Remember to register the instance to the new target group with the correct port:
![target group status](/images/target-group-status.png)

When your load balancer up and connect to your target group you can use the load balancer DNS for access the app:
![load balncer](/images/load-balncer.png)


### Final Results
When your run the app on localhost:
- The create new user page:
![create new user](/images/create-new-user.png)


- The user details page:
![localhost](/images/localhost.png)

When your run the app on docker container:
![running container](/images/running-container.png)

Running the app on EC2
- The running process on EC2:
![running ps](/images/running-ps.png)

- The app on EC2:
![running on ec2](/images/running-on-ec2.png)
