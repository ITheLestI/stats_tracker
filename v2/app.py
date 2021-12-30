import os, sys, json
from flask import Flask, request

app = Flask(__name__)
app.secret_key="erfgLKJKLJGKLkjLKLGjlSSLKDgjl"

UPLOAD_FOLDER = './data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.chdir(os.path.dirname(sys.argv[0]))

@app.route('/', methods=['GET'])
def get():
    return "Hello world!", 200

@app.route('/swimmers', methods=['GET'])
def get_swimmers():
    request.args.get("swimmer", type=str, default="Москвин Антон")
        
    swimmers = json.load(open())
    return "Got users request", 200


@app.route('/', methods=['POST'])
def upload_data():
    if request.method == 'POST':
        if "file" not in request.files:
            return 418
        file = request.files["file"]

        if file:
            if not os.path.exists("./data"):
                os.mkdir("./data")
            i = 1
            #while os.path.exists(f"./data/data_{i}.txt"):
            #    i+=1
            file.save(f"./data/" + file.filename)
            
        else:
            return "Wrong file", 406
        
        return "File was received and saved", 200

@app.after_request
def apply_caching(resp):
    resp.headers.set('Access-Control-Allow-Origin', '*')
    resp.headers['Access-Control-Allow-Headers'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = '*'
    return resp   

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port= 5000)