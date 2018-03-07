
try:
        import Image
except ImportError:
        from PIL import Image
#import pytesseract
import datetime
import os
import tensorflow as tf
# Create your views here.

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView

class FileUploadView(APIView):
    parser_classes = (FileUploadParser, )
    permission_classes= (AllowAny, )

    def post(self, request, filename, format='jpg'):
        
        src_img = request.data['file']
        dest_img = '/home/abdul/Documents/Dsgit/ca-tf-image-classifier/'+src_img.name
        
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
        in tf.gfile.GFile("/home/abdul/Documents/Dsgit/ca-tf-image-classifier/retrained_labels")]

        # Unpersists graph from file
        with tf.gfile.FastGFile("/home/abdul/Documents/Dsgit/ca-tf-image-classifier/retrained_graph.pb", 'rb') as f:
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
                score = predictions[0][node_id]
                return Response('%s (score = %.5f)' % (human_string, score))


