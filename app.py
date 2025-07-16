import os
import shutil
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from zipfile import ZipFile
import docker

# Creating docker client
docker_client = docker.from_env()

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__name__)), "uploads") 
HOSTING_PATH = os.path.join(os.path.dirname(os.path.abspath(__name__)), "hosting")
DOCKER_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__name__)), "Dockerfile temp/Dockerfile")

ALLOWED_EXTENSIONS = {"zip"}

from flask import Flask, render_template, request, redirect, url_for
port = 8080
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    global port

    # validating the file and sanitizing the filename
    uploaded_file = request.files['file']
    file_name = secure_filename(uploaded_file.filename)
    if uploaded_file.filename != '':

        # Saving it to the system
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        uploaded_file.save(file_path)

        # Extracting the file and saving it to hosting folder
        dir_name = file_name.split(".")[0]
        hosting_location = os.path.join(HOSTING_PATH, dir_name)
        ZipFile(file_path).extractall(hosting_location)

        # copying over the docker file
        shutil.copyfile(DOCKER_FILE_PATH, os.path.join(hosting_location,"Dockerfile"))

        # running docker build
        docker_client.images.build(path=hosting_location, tag=dir_name)
        docker_client.containers.run(dir_name, detach=True, ports={'80/tcp': port})
        port += 1

        return render_template('output.html', port=port-1)

    return redirect(url_for('index'))

if __name__ == '__main__':

    app.run(debug=True)