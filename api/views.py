try:
        import Image
except ImportError:
        from PIL import Image
#import pytesseract
import requests
import datetime
import os
import tensorflow as tf
import sys
# Create your views here.

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView

  
GPSX = 38.3029
GPSY = 23.7535


class FileUploadView(APIView):
    parser_classes = (FileUploadParser, )
    permission_classes= (AllowAny, )

  

    def posttoorion(self, sensorid, field_score, fire_score, gps1, gps2):
        pts = datetime.datetime.now().strftime('%s')

        url = 'http://193.190.127.181:1026/v2/entities'
        headers = {'Accept': 'application/json', 'X-Auth-Token': 'QGIrJsK6sSyKfvZvnsza6DlgjSUa8t'}

        json = {
            "id": sensorid+pts,
            "type": "Raspberry_Pi",
            "nodeid": {
                "value": sensorid,
                "type": "id"
            },
            "timestamp": {
                "value": str(pts),
                "type": "time"
            },
            "fire_score": {
                "value":fire_score,
                "type":"tensorflow_score"
            },
            "field_score": {
                "value": field_score,
                "type": "tensorflow_score"
            },
            "gpsx": {
                "value": gps1,
                "type": "gps"
            },
            "gpsy": {
                "value": gps2,
                "type": "gps"
            }

        }

        json_bytes = sys.getsizeof(json)
        headers_bytes = sys.getsizeof(headers)
        total = json_bytes + headers_bytes

        # log network traffic (naive)
        print json_bytes,headers_bytes, total

        response = requests.post(url, headers=headers, json=json)
        print(str(response))
        return str(response)





    def post(self, request, filename, format='jpg'):
       
        temp_list = []
        src_img = request.data['file']
        dir = os.getcwd()
        filename = os.path.join(dir, '')
        dest_img = filename+"/"+src_img.name
        
        with open(dest_img, 'wb+' ) as dest:
            for c in src_img.chunks():
                dest.write(c)
        
        lines = open(dest_img).readlines()
        open(dest_img, 'wb+').writelines(lines[4:-1])

        to_ocr = Image.open(dest_img)
        image_data = tf.gfile.FastGFile(dest_img, 'rb').read()

        if os.path.isfile(dest_img):
            os.remove(dest_img)
        else:
            print("Error: temp file not found")
              

        # Loads label file, strips off carriage return  
        label_lines = [line.rstrip() for line
        #path file of retrained_labels
        in tf.gfile.GFile(filename+"/retrained_labels")]

        # Unpersists graph from file
        with tf.gfile.FastGFile(filename+"/retrained_graph.pb", 'rb') as f:

        # Unpersists graph from file
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

        # Feed the image_data as input to the graph and get first prediction
        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data}) 
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        
            for node_id in top_k:
                human_string = label_lines[node_id]
                print ('%s' % human_string)
                score = predictions[0][node_id]
                if human_string in ['field fire']:
                    #temp_list.append([human_string, score])
                    temp_list.insert(0,[human_string, score])
                if human_string in ['field']:
                    temp_list.insert(1,[human_string, score])
        

        #Send data to OCB
        fire = round(temp_list[0][1],5)
        field = 1-fire
        print fire
        return Response(self.posttoorion("edgy", field, fire, GPSX, GPSY)) # Post to OCB      
        #print "postoorion"
        # If we want to print everything in the list we need to change the next line to   
        #return Response(round(temp_list[0][1],5))