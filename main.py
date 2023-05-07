import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import cv2


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'


def processImage(filename, operation):
    img = cv2.imread(f'uploads/{filename}')
    
    match operation:
        case 'cgray':
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f'static/{filename}'
            cv2.imwrite(newFilename, imgProcessed)
            return filename
        
        case 'cwebp':
            newFilename = f'static/{filename.split(".")[0]}.webp'
            cv2.imwrite(newFilename, img)
            return f'{filename.split(".")[0]}.webp'
        
        case 'cpng':
            newFilename = f'static/{filename.split(".")[0]}.png'
            cv2.imwrite(newFilename, img)
            return f'{filename.split(".")[0]}.png'
        
        case 'cjpg':
            newFilename = f'static/{filename.split(".")[0]}.jpg'    
            cv2.imwrite(newFilename, img)
            return f'{filename.split(".")[0]}.jpg'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.before_request
# def check(*args, **kwargs):
#     if not request.path.startswith('/main') or not request.path.startswith('/edit'):
#         return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Error!')
            return 'Error!'
        
        file = request.files['file']

        if file.filename == '':
            flash('No file selected!')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = filename.replace(' ', '')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, request.form.get('operation'))
            flash(f'Your image has been processed!', category='success')
            return send_from_directory('static', new)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
