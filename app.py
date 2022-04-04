from flask import Flask
from flask import request, render_template
from mbta import *

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def hello():
    return render_template("index.html")

@app.route('/data', methods = ['POST', 'GET'])
def data():
    formdata = request.form
    userinput = formdata['Address'] + ', ' + formdata['City'] + ', ' + formdata['State']
    customurl = urlbuild(userinput)
    mapinfo = pullmap(customurl)
    coords = pullcoords(mapinfo)
    listcoords = list(coords)
    mbtacustom = mbtaurl(listcoords)
    mbtainfo = mbta(mbtacustom)
    closeststation = mbta_closest(mbtainfo)
    isitaccess = mbta_wheel(mbtainfo)
    return 'The closest station to you is ' + closeststation + ' and ' + isitaccess

@app.errorhandler(404)
def error404(error):
    return 'This is not a valid webpage please go back to http://127.0.0.1:5000/'
        



if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask


# app = Flask(__name__)


# @app.route('/')
# def hello():
#     return 'Hello World!'


# if __name__ == '__main__':
#     app.run(debug=True)



