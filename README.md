# IoT Project

This project aims to develop an application for processing GPS location data from IoT devices. Device data is collected via TCP protocol, queued, and then processed by a consumer. The processed data is stored in a database, and various API services are provided.

## Table of Contents

- [Technology Stack](#technology-stack)
- [Django Project Setup](#django-project-setup)
  - [Development Environment](#development-environment)
  - [Database Setup](#database-setup)
  - [Database Migrations](#database-migrations)
- [Running Docker](#running-docker)
- [API Testing](#api-testing)
- [IoT Project Setup](#iot-project-setup)
  - [Creating `.env` File](#creating-env-file)
  - [Running the Project](#running-the-project)
  - [Testing](#testing)

## Technology Stack

- **Language:** Python
- **Web Framework:** Django
- **Database:** PostgreSQL
- **Message Broker:** RabbitMQ
- **Cache and Task Queue:** Redis, Celery
- **Containerization:** Docker
- **GraphQL:** Implemented
- **Version Control:** Git

## Django Project Setup

### Development Environment

1. **Clone the Repository:**

- `git clone https://github.com/maliksari/drf-iot-project.git`

- `cd django-iot-project`

2.  **Set Up Python Virtual Environment:**

- `python3 -m venv venv `
- `source venv/bin/activate  # Linux/Mac`
- `venv\Scripts\activate     # Windows`

3. **Install Required Packages:**
- `pip install -r requirements.txt`

## Database Setup 
After setting up PostgreSQL, create a `local_conf.py` file in the `django-iot-project/common` directory with the following configuration. Adjust the database settings as per your environment:

```
SECRET_KEY = 'django-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        # 'HOST': 'host.docker.internal' for Docker
        'PORT': '5432',
    }
}
```

## Database Migrations
Apply Django database migrations with the following commands:
```
python manage.py makemigrations
python manage.py migrate
```
## Running Docker

1. **Build Docker Image:**
- Build the Docker image for the application:
```
docker build -t django-iot-app .
docker run -p 8000:8000 django-iot-app
```
2. **Test URL**
- Access the API endpoint for testing using the following URL:
```
 http://localhost:8000/app/v1/graphql/
```

## API Testing
You can test the following GraphQL queries and mutations:
1. **Create Device:**

```
mutation {
  createDevice(name: "New Device") {
    device {
      id
      name
    }
  }
}
```
2. **Update Device:**
```
mutation {
  updateDevice(id: 1, name: "Updated Device") {
    device {
      id
      name
    }
  }
}
```
3. **Delete Device:**
```
mutation {
  deleteDevice(id: 1) {
    success
  }
}
```
4. **Get Latest Location for Each Device:**
```
query {
  allDevicesWithLastLocation {
    device {
      id
      name
    }
    lastLocation {
      id
      latitude
      longitude
      createdOn
    }
  }
}
```
5. **Get All Locations for a Specific Device:**
```
query {
  getDeviceLocations(id: 1) {
    device {
      id
      name
    }
    locations {
      id
      latitude
      longitude
      createdOn
    }
  }
}
```

## Run Test 

```
 python manage.py test
```

## IoT Project Setup

The IoT project is located in the same directory as the Django project.

**Creating `.env` File**

Create a `.env` file in the **`iot-tcp`** directory with the following content. This uses the same database as the Django project:

```
DATABASE_NAME=db_name
DATABASE_USER=db_user
DATABASE_PASSWORD=password
DATABASE_HOST=host.docker.internal # for docker
DATABASE_PORT=5432
# DATABASE_HOST=localhost
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0
```
## Running the Project
1. Navigate to **`iot-tcp`** Directory:
```
cd iot-tcp
```
2. **Start Docker Compose:**
Build and start the Docker containers:
```
docker-compose up --build
```

## Testing

To test the application, run the client_test.py script located in the **`iot-tcp/`** directory.

**Note:** Add the IDs of the devices you have created in the following line within **`client_test.py`**:

```
device_ids = [1, 3, 4, 6, 8, 9]  # Device IDs
```


### Steps to Send Data

1. **Open Telnet Connection:**

   Start Telnet and connect to the TCP server running on `localhost` at port `9999`. Use the following command:

```
telnet localhost 9999
```
2. **Data format**
```
{device_id} {latitude} {longitude}
```
***Example***
```
1 37.7749 -122.4194
```
