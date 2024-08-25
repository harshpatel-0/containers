from flask import Flask, request, redirect, render_template, url_for
import boto3

app = Flask(__name__)

s3_client = boto3.client('s3')
bucket_name = 'hw07-harsh'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = file.filename
        s3_client.upload_fileobj(file, bucket_name, filename)
        return redirect(url_for('list_files'))

@app.route('/files')
def list_files():
    files = []
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        files = response.get('Contents', [])
    except Exception as e:
        print(e)
    return render_template('table.html', files=files)

@app.route('/files/<filename>')
def file(filename):
    file_url = s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket_name, 'Key': filename},
                                                ExpiresIn=3600)
    return render_template('display_image.html', url=file_url)

if __name__ == '__main__':
    app.run(debug=True)
