# import cv2
# import pytesseract
# import numpy as np
from flask import request, render_template, Blueprint

# Define the Blueprint
ocr_routes = Blueprint('ocr', __name__)


# @ocr_routes.route('/', methods=['GET', 'POST'])
# def upload_picture():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file.filename == '':
#             return "No selected file"
#         if file:
#             # Convert string data to numpy array
#             npimg = np.frombuffer(file.read(), np.uint8)
#             # Convert numpy array to image
#             image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
#             gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#             text = pytesseract.image_to_string(gray, lang='heb')
#             print(text)
#             return render_template('ocr_results.html', text=text)
#     return render_template('ocr_upload.html')
