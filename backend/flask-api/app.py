from flask_cors import CORS
from src import create_app

application = create_app('0.1.5')
cors = CORS(application, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    ip = '0.0.0.0'
    port = application.config['APP_PORT']
    debug = application.config['DEBUG']

    application.run(
        host=ip, debug=debug, port=port, use_reloader=debug
    )
