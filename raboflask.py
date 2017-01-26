import os
from flask import Flask, request, redirect, url_for, render_template, flash, make_response, send_from_directory
from werkzeug.utils import secure_filename
from main import qif_return

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)
#app.run(host= '0.0.0.0')
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'geheim'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global filenameglob

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            filenameglob = filename

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

           # return redirect(url_for('uploaded_file', filename=filename))
            print(filename)
            return redirect(url_for('download'))


    return render_template('raboflask.html')



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



@app.route('/download', methods=['GET'])
def download():
    qif_return('uploads/' + filenameglob)

    with open("static/transactions.qif") as infile:
        qif = infile.read()
        response = make_response(qif)

    with open("static/transactions.qif", 'w') as privacyfile:
        privacyfile.write("")

    with open("uploads/" + filenameglob, 'w') as privacyfile:
        privacyfile.write("")

    
    response.headers["Content-Disposition"] = "attachment; filename=transactions.qif"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')