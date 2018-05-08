try:
        import Image
except ImportError:
        from PIL import Image
import datetime
import os
import sys
import tensorflow as tf

import time
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from api.models import Tasks_Interval

GPSX = 38.3029
GPSY = 23.7535


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, )
    permission_classes = (AllowAny, )

    def posttoorion(self, sensorid, size, duration, field_score, fire_score, gps1, gps2):
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
            "size": {
                "value": size,
                "type": "bytes"
            },
            "duration": {
                "value": duration,
                "type": "seconds"
            },
            "fire_score": {
                "value": fire_score,
                "type":" tensorflow_score"
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

        # response = requests.post(url, headers=headers, json=json)
        # print(str(response))
        # return str(response)

    def post(self, request, filename, format='jpg'):
        stats = Tasks_Interval.objects.first()

        if not stats:
            b = Tasks_Interval(number_to_accept=100,
                               submitted=0,
                               finished=0,
                               rejected=0,
                               total_time=0)
            b.save()
            stats = Tasks_Interval.objects.first()
        print stats.finished
        number_to_accept = stats.number_to_accept
        count = stats.submitted
        bound = number_to_accept - count
        print (bound)

        if bound <= 0:
            start_time = request.data['start_time']
            src_img = request.data['file']
            r = Tasks_Interval.objects.first()
            finished = r.finished
            r.finished = finished + 1
            r.save()

            return Response("Rejected")

        else:
            s = Tasks_Interval.objects.first()
            submitted = s.submitted
            s.submitted = submitted + 1
            s.save()

            size = request.data['size']
            start_time = request.data['start_time']
            temp_list = []
            src_img = request.data['file']
            dirr = os.getcwd()
            filename = os.path.join(dirr, '')
            dest_img = filename+src_img.name

            with open(dest_img, 'wb+' ) as dest:
                for c in src_img.chunks():
                    dest.write(c)
            image_data = tf.gfile.FastGFile(dest_img, 'rb').read()
            if os.path.isfile(dest_img):
                os.remove(dest_img)
            else:
                print("Error: temp file not found")

            # Loads label file, strips off carriage return
            label_lines = [line.rstrip() for line
                           # path file of retrained_labels
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
                predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
                # Sort to show labels of first prediction in order of confidence
                top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        
                for node_id in top_k:
                    human_string = label_lines[node_id]
                    score = predictions[0][node_id]
                    if human_string in ['field fire']:
                        # temp_list.append([human_string, score])
                        temp_list.insert(0,[human_string, score])
                    if human_string in ['field']:
                        temp_list.insert(1,[human_string, score])
               
            # Send data to OCB
            fire = round(temp_list[0][1],5)
            field = 1-fire
            end_time = time.time()  # * 1000
            duration = float(end_time) - float(start_time)
            duration = round(duration, 3)

            # return Response(self.posttoorion("edgy", size, duration, field, fire, GPSX, GPSY)) # Post to OCB
            f = Tasks_Interval.objects.first()
            if not f:
                b = Tasks_Interval(number_to_accept=100,
                                   submitted=0,
                                   finished=0,
                                   rejected=0,
                                   total_time=0)
                b.save()
                f = Tasks_Interval.objects.first()
            print f.finished
            finished = f.finished
            f.finished = finished + 1
            total_time = f.total_time
            f.total_time = total_time + duration
            f.save()
        return Response(round(temp_list[0][1], 5))














