# -industrial-risk
[![Deploy](https://www.herokucdn.com/deploy/button.svg)]

# Capstone Project

Predict the risk given a description of the task

## Docker Installation


### Pre-Requisite

- For windows, install [Docker desktop](https://www.docker.com/get-started)
  
- For Ubuntu, Follow instructions [here](https://docs.docker.com/engine/install/ubuntu/) 

### Build Docker image

Go to the containing folder and run below command in command line

    `docker build -t risk-predictor-app .`

 <sub>Note: Add sudo if you are running Docker with root</sub>

### Run Docker Image

    `docker run -p 5000:5000 -t risk-predictor-app`


## Ubuntu OS


## Pre-Requisite

- Python 3

- pip3
   
    <sub>install using
   `sudo apt-get install python3-pip`</sub>

###  Installation

! Recommended to install virtual environment for python. (Might be pre-installed)

#### 1. Virtual Environment [optional]

1. Installation
   
    `sudo pip3 install virtualenv`
   
2. Create virtual environment on repo
   
   `virtualenv -p python3 ./risk_predictor_venv`

3. Activate the virtual environment
    
    `source risk_predictor_venv/bin/activate`

#### 2. Install dependencies

You can install dependencies from the requirements.txt file

    `pip -r requirements.txt`

#### 3.Install Postman [for testing]

Download Postman from their [downloads page](https://www.postman.com/downloads/) for your OS

<sub>Note: Postman collection is available in the repository for importing</sub>

#### 4. Server.py

In the last line, change 

`app.run(port=5000,host='0.0.0.0', debug=True)`

to use the localhost address 127.0.0.1

`app.run(port=5000,host='127.0.0.1', debug=True)`

### Run the Application Server

    `python3 server.py`


## APIs Available


When running docker : use host address: 172.17.0.2:5000

when running as standalone python, you can use 127.0.0.1:5000

E.g.: 127.0.0.1:5000\isalive  or 172.17.0.2:5000\isalive

|API   |type| Description |Expected Request Body|Expected Response|
|------|-----|---         | --------            |-----            |
|/isalive | GET |  Checks if the service is available.| |```{"status": "Live"}``` |
|/predict | POST | Description of task is passed as JSON and the service returns the accident level category from 0 to 4|```{"text":"This is a sample description of task"}```|```{"prediction":"Don't worry, there is little risk (Category II)"}```|

## Web Application

Access the application at address `localhost:5000`  

![Web Application](Docs/Screenshots/webApp.png "Industrial Risk Predictor Chat-Bot")



