import warnings

from flask import Flask, request
import Astar
import convert_image_to_map

app = Flask(__name__)


@app.route('/findRoute')
def findRoute():
    ul = request.args['ul']
    rl = request.args['rl']
    path = request.args['path']
    warnings.filterwarnings('ignore')
    return Astar.Astar_main(ul,rl,path)


@app.route('/convertImageToMap')
def convertImageToMap():
    argv = request.args['path_name']
    return convert_image_to_map.convert_image_to_map_main(argv)

@app.route('/home')
def home():
    return "Server works well"

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

