from flask import Flask, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()], id="File")
    submit = SubmitField("Upload File")
    submit_delete = SubmitField("Delete File")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', "POST"])
@app.route('/index', methods=['GET', "POST"])
def index():
    form = UploadFileForm()
    message = None
    file_path = None  # this one is path of uploaded file

    file_path = session.get('file_path', None)


    if form.validate_on_submit():
        if file_path == None:
            file = form.file.data  # First grab the file
            filename = file.filename

            if allowed_file(filename):
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                       secure_filename(file.filename)))  # Then save the file

                file_path = " static/files/" + filename
                session['file_path'] = file_path  # Store the file path in session
                absolute_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             secure_filename(filename))
                print(f"absolute_path: {absolute_path}")

                message = "File has been successfully uploaded!"
            else:
                message = "Invalid file extension. Please upload a PNG, JPG, or JPEG file."
        else:
            message = "Only 1 file can be uploaded at the time"


    elif form.submit_delete.data:
        print(f"file_path: {file_path}")
        file_to_delete = request.form.get('current_file')

        print(f"file to delete:{file_to_delete}")
        # file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
        #                        secure_filename(os.path.basename(file_to_delete)))
        if file_to_delete:
            file_name = os.path.basename(file_to_delete)

            absolute_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                         secure_filename(file_name))

            if os.path.exists(absolute_path):
                os.remove(absolute_path)
                session.pop('file_path', None)  # Remove the file path from the session
                file_path = None

                message = "File has been successfully deleted!"
            else:
                message = "File not found. Could not delete."

    return render_template('index.html', form=form, message=message, file_path=file_path)


if __name__ == "__main__":
    app.run(debug=True)
