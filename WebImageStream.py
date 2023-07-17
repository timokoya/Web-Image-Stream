import os
import time
from waitress import serve
from flask import Flask, Response

app = Flask(__name__)

# Generate images for the web server
def gen():
    i = 0

    # While loop because images might be added to the folder at runtime
    while True:

        #interval images are transmitted to the client
        time.sleep(1)

        # Get the images
        images = get_all_images()
        image_name = images[i]
        #photos_dir = self.logname + '/Photos/'
        im = open('images/' + image_name, 'rb').read()

        # Return the images
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + im + b'\r\n')
        
        # Track which image from the array that was displayed in the last iteration
        i += 1
        if i >= len(images):
            i = 0

# Read list of images 
def get_all_images():
    image_folder = 'images'
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]
    return images

# Define HTTP GET endpoint and return a Response object with image as content
@app.route('/slideshow')
def slideshow():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# A starting HTTP endpoint that serves a simple HTML page
@app.route('/')
def index():
    return "<html><head></head><body><h1>Slideshow of Images Captured by WAVYNOS! </h1><img src='/slideshow' style='width: 90%; height: 90%;'/>" \
           "</body></html>"


if __name__ == '__main__':
    
    # Run the development server
    #app.run(host='0.0.0.0', debug=True)
    
    # Run the production server, 
    serve(app, host="0.0.0.0", port=8080)