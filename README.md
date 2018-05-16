# Tensorflow-based Image Classification Service

An image classification service, developed using Google’s Tensorflow deep learning framework, where the “Inception v3” Deep Neural Network was retrained in order to classify images of fields as “fire-containing” or not. This service is meant to be containerized and deployed on a Docker platform installed on Fog and or Cloud servers, or executed as a native standalone application at the Edge. Containers were selected instead of Virtual Machines, as a means of virtualization, because of their overall lower overhead, smaller footprint and lightweight vertical scalability. For the asynchronous communication of both the Edge and the Fog layer with Cloud, the NGSI mechanism (OCB) is leveraged.

The model can be easily retrained to match your specific classification needs.
This repo is a Dockerized Django Rest-Api service, able to cooperate with Edgy-Controller (repo: https://github.com/maravger/edgy-controller.git) for offloading TensorFlow based applications in the network edge. This service is able to manage requests from clients and send ctucial data back to the controller, necessary for the scaling algorithm explained in the aforementioned repo.     
You can choose either Docker execution or native execution! 

## Docker Execution
First of all make sure you have Docker installed. If not, head to https://docs.docker.com/install/

Build:
```bash
docker build -t ca-tf .
```

Run the service as a server:
```bash
docker run -it -p 8000:8000 ca-tf
```

You are good to go. Test the service using one of the predifined client scenarios:
```bash
cd client_scenarios/
client_scenario_2.py
```

*Make sure to change the IPs within the scripts, to match your server's installation.
Also, it's neccessary that you add your server's IP to ca_tf/settings.py -> ALLOWED_HOSTS.
*

## Native Installation and Execution

Then, install pip and virtualenv:
```bash
sudo apt-get install python-pip python-dev python-virtualenv # for Python 2.7
sudo apt-get install python3-pip python3-dev python-virtualenv # for Python 3.n
```

Clone the existing repo:
```bash
git clone https://github.com/maravger//ca-tf-image-classifier.git
```

Create a Virtualenv environment by issuing one of the following commands:
```bash
virtualenv --system-site-packages . # for Python 2.7
virtualenv --system-site-packages -p python3 . # for Python 3.n
```
Activate the Virtualenv environment by issuing the following command:
```bash
source ./bin/activate
```
...and install the requirements:
```bash
pip install -r requirements.txt
```

Now you can run the service nativelly
```bash
chmod +x /entrypoint.sh
./entrypoint.sh
```



## Local execution of the Image-Classifier Service for testing
```bash
./classify.py IMAGE
```

## Additional script for converting OCB json data to CSV.
In json_to_csv.py:
1. change path of .txt file you want to convert. 
2. output.json contains your flattened json.
3. include the keys you want to include to your csv. 

