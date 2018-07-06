try:
        import Image
except ImportError:
        from PIL import Image
import datetime
import os
import sys
import tensorflow as tf
import time
import csv
from django.db import transaction,OperationalError

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from api.models import Tasks_Interval
from celery import task
from api import tasks

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

    def gen_password( temp=8, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"):
        random_bytes = os.urandom(8)
        len_charset = len(charset)
        indices = [int(len_charset * (ord(byte) / 256.0)) for byte in random_bytes]
        return "".join([charset[index] for index in indices])

    def post(self, request, filename, format='jpg'):

        with transaction.atomic():
            stats = Tasks_Interval.objects.select_for_update().first()

            # for stand-alone version. It is useless if it is monitoring by a real Controller
            if not stats:
                b = Tasks_Interval(number_to_accept=100,
                                   submitted=0,
                                   finished=0,
                                   rejected=0,
                                   total_time=0)
                try:
                    b.save()
                except OperationalError:
                    print("DB locked: concurrency avoided")
                stats = Tasks_Interval.objects.select_for_update().first()

        number_to_accept = stats.number_to_accept
        count = stats.submitted
        bound = number_to_accept - count
        if bound <= 0:
            start_time = request.data['start_time']
            start_process_time = time.time()
            src_img = request.data['file']
            with transaction.atomic():
                r = Tasks_Interval.objects.select_for_update().first()
                rejected = r.rejected
                r.rejected = rejected + 1
                try:
                    r.save()
                except OperationalError:
                    print("DB locked: concurrency avoided")
            return Response("Rejected")

        else:
            skata = tasks.post_submitted(request,filename)
#            with transaction.atomic():
#                s = Tasks_Interval.objects.select_for_update().first()
#                submitted = s.submitted
#                s.submitted = submitted + 1
#                try:
#                    s.save()
#                except OperationalError:
#                    print("DB locked: concurrency avoided")

            size = request.data['size']
            start_time = request.data['start_time']
            start_process_time = time.time()
            temp_list = []
            src_img = request.data['file']
            dirr = os.getcwd()
            filename = os.path.join(dirr, '')
            dest_img = filename + self.gen_password() + src_img.name

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

            with transaction.atomic():
                f = Tasks_Interval.objects.select_for_update().first()

                # for stand-alone version. It is useless if it is monitoring by a real Controller
                if not f:
                    b = Tasks_Interval(number_to_accept=100,
                                       submitted=0,
                                       finished=0,
                                       rejected=0,
                                       total_time=0)
                    try:
                        b.save()
                    except OperationalError:
                        print("DB locked: concurrency avoided")

                    f = Tasks_Interval.objects.select_for_update().first()

                finished = f.finished
                f.finished = finished + 1
                total_time = f.total_time
                f.total_time = total_time + duration
                
                transmission_time = f.transmission_time
                computation_time = f.computation_time
                f.transmission_time = transmission_time + duration - (end_time-start_process_time) 
                f.computation_time = computation_time + end_time - start_process_time
                #print duration
                #print (end_time - start_process_time)
                try:
                    f.save()
                except OperationalError:
                    print("DB locked: concurrency avoided")


#                filename = "csvs/logger"
#                with open(filename, 'a') as myfile:
#                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#                    if (os.path.getsize(filename)== 0):
#                        wr.writerow(["transmission_time","computation_time","total_time"])
 #                   wr.writerow([duration-(end_time-start_process_time),end_time-start_process_time,duration])

#            with transaction.atomic():
#                h = Tasks_Interval.objects.select_for_update().first()
#                if not f:
#                    b = Tasks_Interval(number_to_accept=100,
#                                       submitted=0,
#                                       finished=0,
#                                       rejected=0,
#                                       total_time=0)
#                    try:
#                        b.save()
#                    except OperationalError:
#                        print("DB locked: concurrency avoided")
#                    f = Tasks_Interval.objects.select_for_update().first()
#
 #               transmission_time = f.transmission_time
 #               computation_time = f.computation_time
 #               f.transmission_time = transmission_time + duration - (end_time-start_process_time) 
  #              f.computation_time = computation_time + end_time - start_process_time
   #             try:
   #                 f.save()
    #            except OperationalError:
     #               print("DB locked: concurrency avoided")
                

        return Response(round(temp_list[0][1], 5))



            
