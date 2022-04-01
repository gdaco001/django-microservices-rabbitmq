# The Challenge Implementation

This project has been developed following Test Driven Development for its most important features. Also, Docker has been used to serve the api service, stock service, MongoDB and the GUI for MongoDB (mongo-express). 

It is necessary to authenticate into the system in order to access all endpoints of the api service. JWT was used as the authentication method.

## How to run the project

Please, follow the steps below to run the project on a Linux operating system.
### Step 0: Install Docker and Docker Compose

__Skip__ this step if you already have Docker and Docker Compose installed on your operating system.

**Update packages**: 
```shell
sudo apt update && sudo apt upgrade -y
```
**Install prerequisite packages**: 
```shell
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```
**Add the GPG key from the official Docker repository**: 
```shell 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
**Add the official Docker repository to APT sources**: 
```shell 
sudo add-apt-repository \
"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```
**Update the Ubuntu packages list**: 
```shell 
sudo apt update
```
**Verify the Docker repository**: 
```shell 
apt-cache policy docker-ce
```
**Install Docker Comunity Edition**: 
```shell 
sudo apt install docker-ce
```
**Check the status installation status**: It should return __active (running)__
```shell
sudo systemctl status docker
```
**Install Docker Compose**:
```shell
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
**Apply executable permissions for the downloaded binary**:
```shell
sudo chmod +x /usr/local/bin/docker-compose
```
**Check if Docker Compose has been successfully installed**:
```shell
docker-compose --version
```
**Create the docker group**:
```shell
sudo groupadd docker
```
**Add your user to the docker group**:
```shell
sudo usermod -aG docker $USER
 ```
 **Activate changes to the group**:
```shell
newgrp docker 
 ```
Docker is now installed and ready to use in your machine. It is, however, recommended to log-off and log back in so group changes take effect. If you are on a virtual machine, it is recommended to shut down and start it again.

## Step 0.5: Set Environment Variables

Some environment variables must be set in order to properly run the project. Please, copy the variables below to the __.dev.env__ file and proceed to the next steps.

```
MONGODB_SERVER=mongodb
MONGODB_ENABLE_ADMIN=true
MONGODB_ADMINUSERNAME=root
MONGODB_ADMINPASSWORD=pass12345
BASICAUTH_USERNAME=user
BASICAUTH_PASSWORD=user123
DJANGO_ADMIN_USER=user
DJANGO_ADMIN_PASS=user123
RABBITMQ_DEFAULT_USER=user
RABBITMQ_DEFAULT_PASS=user123
MONGO_INITDB_DATABASE=stock_service_db
MONGO_INITDB_USERNAME=gabriel
MONGO_INITDB_PASSWORD=costa123
DB_HOST=mongodb
DB_PORT=27017
SECRET_KEY_API_SERVICE=b!+q)h#vk3lz+lep2@d5=t*m7$grwtkl_(k-f9bt@75k-=omn4
SECRET_KEY_STOCK_SERVICE=8lry=eih0=6unsro-d)x7%l)e3&dlvb_aclwnzl%6+!gj6q8vz
```

### Step 1: Build Images
Images can be built separately by running:
```shell
$ make build-api
$ make build-stock
```

Or all images can be built altogether by running:
```shell
$ make build-all
``` 

### Step 2: Deploy Images

Services can be deployed separately by running:
```shell
$ make deploy-api
$ make deploy-stock
```
The ```make deploy-api``` command is responsible for deploying the __api service__, __RabbitMQ__, __database__ and the __database GUI__ containers. The ```make deploy-stock``` will only deploy the __stock service__ container.

All services can be deployed altogether by running:
```shell
$ make deploy-all
```

It is also possible to shutdown the services separately or in a batch by running:
```shell
$ make shutdown-api
$ make shutdown-stock
$ make shutdown-all
```

It is recommended to run the commands below in order to properly deploy the project.

```shell
$ make build-all
$ make deploy-all
```
If you run the `docker ps` command, you should see the containers up and running.

__Please, make sure the database container is up before running the automated tests.__

### Step 3: Login and access endpoints

A superuser will be created once the __api service__ is properly __deployed__ by running the commands from the previous step. To create a regular user, please go to the admin page at:
 ```shell
http://localhost:8000/admin
```
And login with:
```shell
username: user
password: user123
```
Also, there is a database GUI available at the link below. It can be accessed with the credentials above.
 ```shell
http://localhost:8081
```
Send a __POST__ request to:
 ```shell
http://localhost:8000/login
```
With the arguments:
```
{
  "username": "user",
  "password": "user123"
}
```
To authenticate yourself into the system. The response should look like this:
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0ODE3NjQ2OSwiaWF0IjoxNjQ4MDkwMDY5LCJqdGkiOiJhM2U1ODJlYzY3MTM0YzQ0ODQ2ZTYyYjI4MGFhMzdjNyIsInVzZXJfaWQiOjF9.zQeSN0WIZZ3c_ODr3dmF1kKPT0kXbevchZxf5ddGJdk",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ4MDkwMzY5LCJpYXQiOjE2NDgwOTAwNjksImp0aSI6ImFmZjY1ZjRkOTI0ZDRhMTNiOGI2OGRhYTZlODJjMDYyIiwidXNlcl9pZCI6MX0.5aqvZN-uNacTAIHTT1XQOxLkpQQu9Mc4EnwC6FLaB2I"
}
```
Copy the content of the __access__ key and paste it to your __Authorization__ header as:
```
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ4MDkwMzY5LCJpYXQiOjE2NDgwOTAwNjksImp0aSI6ImFmZjY1ZjRkOTI0ZDRhMTNiOGI2OGRhYTZlODJjMDYyIiwidXNlcl9pZCI6MX0.5aqvZN-uNacTAIHTT1XQOxLkpQQu9Mc4EnwC6FLaB2I
```
Now, you should be able to access all endpoints of the __api service__ as described on the previous sections, once you are logged in as a superuser.
## Commits Pattern

* **test**: indicates any type of creation or alteration of test codes.
* **feat**: indicates the development of a new feature to the project.
* **refactor**: used when there is a code refactoring that does not have any kind of impact on the system's business logic/rules.
* **style**: used when there are formatting and style changes to the code that do not change the system in any way.
* **fix**: used when there are errors that are generating bugs in the system.
* **chore**: indicates changes to the project that do not affect the system or test files. These are developmental changes.
* **docs**: used when there are changes to the project documentation.
* **build**: used to indicate changes that affect the project's build process or external dependencies.
* **perf**: indicates a change that has improved system performance.
* **ci**: used for changes to CI configuration files.
* **revert**: indicates the reversal of a previous commit.