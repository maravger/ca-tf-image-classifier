# ca-tf-image-classifier
1. docker build command:
docker build -t filename .


2. docker run command: 
docker run -i -p 8000:8000 filename


3. Command for curl: 

curl --interface YOURINTERFACE -s -X POST -F "file=@PATHTOYOURIMAGE.jpg;type=image/jpeg" http://127.0.0.1:8000/ca_tf/imageUpload/IMAGENAME.jpg

for example:
curl --interface enp7s0 -s -X POST -F "file=@/home/abdul/Documents/Dsgit/ca-tf-image-classifier/test_data/iphone.jpg;type=image/jpeg" http://127.0.0.1:8000/ca_tf/imageUpload/iphone.jpg





4. json_to_csv.py
a. change path of .txt file you want to open. 
b. output.json has our flattened json
c. include the keys you want to include to your csv.
d. module for epoch convertion timestamps  
