#!/usr/bin/env python
import os
import sys
import requests
try:
        import Image
except ImportError:
        from PIL import Image


url1 = '/home/abdul/Documents/Dsgit/ca-tf-image-classifier/test_data/fire.jpg'
urlpost = 'http://127.0.0.1:8000/ca_tf/imageUpload/fire.jpg'



files = {'file': open(url1,'rb')}

values={'name': 'SKATA'}
   # 'yourname': (None, 'Daniel'),

r= requests.post(urlpost,files=files,data=values)
print(r.text)
#response = requests.post('http://127.0.0.1:8000/ca_tf/imageUpload/fire.jpg', files=files)

