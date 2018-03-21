# Tensorflow-based Image Classification Service

An image classification service, developed using Google’s Tensorflow deep learning framework, where the “Inception v3” Deep Neural Network was retrained in order to classify images of fields as “fire-containing” or not. This service is meant to be containerized and deployed on a Docker platform installed on Fog and or Cloud servers, or executed as a native standalone application at the Edge. Containers were selected instead of Virtual Machines, as a means of virtualization, because of their overall lower overhead, smaller footprint and lightweight vertical scalability. For the asynchronous communication of both the Edge and the Fog layer with Cloud, the NGSI mechanism (OCB) is leveraged.

The model can be easily retrained to match your specific classification needs.

## OCB server side install

## Native execution
Create virtual environment:
```bash
pip install --upgrade virtualenv 
virtualenv --system-site-packages .
source ./bin/activate
```

Install required libraries and run:
```bash
pip install -r requirements.txt
./classify.py IMAGE
```

## Docker install
1. build:
```bash
docker build -t ca-tf .
```

2. run as a server:
```bash
docker run -i -p 8000:8000 ca-tf
```

3. Test using one of the predifined scenarios
```bash
cd client_scenarios/
client_scenario_2.py
```

## Convert OCB json data to CSV
In json_to_csv.py
1. change path of .txt file you want to convert. 
2. output.json contains your flattened json.
3. include the keys you want to include to your csv. 
