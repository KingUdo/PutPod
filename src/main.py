from flask import Flask, request, jsonify, abort, make_response, render_template, redirect, send_from_directory
from misc.database import DATABASE_SESSION
import hashlib
from objects.files import Files
import logging
import datetime

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

# server setup
app = Flask(__name__)
app.config["DEBUG"] = 0

@app.route('/<file_name>', methods=['PUT', 'GET'])
def main_put_route(file_name):

    source_ip = request.headers.get('X-Remote-Ip')

    if request.method == 'PUT':

        logging.debug("Got a put request from {}".format(source_ip))
        file = request.stream.read()
        file_hash = hashlib.md5(file).hexdigest()

        with open('malware/{}'.format(file_hash), 'wb') as f:
            f.write(file)

        # Add file to the DB
        session = DATABASE_SESSION()
        new_file = Files(date=datetime.date.today().strftime("%Y-%m-%d"),
                         hash=file_hash,
                         name=file_name,
                         source_ip=source_ip)
        session.add(new_file)
        session.commit()
        session.close()

        return ""

    else:

        session = DATABASE_SESSION()

        query = session.query(Files)
        query = query.filter(Files.source_ip == source_ip)
        query = query.filter(Files.name == file_name)
        result = query.first()

        if result:
            logging.debug("Got a GET request for {} from {} which matches => sending file".format(result.hash, source_ip))
            return send_from_directory("malware", result.hash)
        else:
            logging.debug("Got request from {} not machining in DB => not sending anything".format(source_ip))
            abort(404)

    abort(404)

@app.after_request
def after_request(response):
    response.headers.set('Server', '')

    return response



if __name__ == '__main__':

    app.run(debug=False, host="0.0.0.0", port=8080)