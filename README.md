# Social-Networking

## Setup

1. Install Virtual Environment
   - cd Social-Networking/
#### Ubuntu
```
    sudo apt update
    sudo apt install python3-venv
    python3 -m venv env
    source env/bin/activate
```
#### Windows
```
    python -m venv env
    env\Scripts\activate
```
2. Install Requirements
```
    pip install -r requirements.txt
```
## Run

1. Enter into the project directory
```
    cd social_networking_project
```
   - Make sure you're in the root directory of your Django 
project where manage.py is located.

#### Ubuntu
```
    python3 manage.py runserver
```
#### Windows
```
    python manage.py runserver
```
2. Access the Swagger UI of the API
   - Open your web browser and navigate to:
```
    localhost:8000/swagger/
```

