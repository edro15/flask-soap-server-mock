import base64
import os

from flask import Flask, request, make_response, send_file, render_template

app = Flask(__name__)
is_env_docker = os.environ.get('RUNNING_IN_DOCKER', False)
app.config.from_object('server.config.DockerConfig' if is_env_docker else 'server.config.LocalConfig')

api_handler = app.config['API_HANDLER']
static_wsdl_dir = app.config['WSDL_PATH']


def handle_get(body):
    response = make_response(body)
    response.headers["Content-Type"] = "text/xml; charset=utf-8"
    return response



@app.route(api_handler + '/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/EditBook', methods=['POST'])
def edit():
    template = render_template('response.xml',
                                name="editBook",
                                namespace="http://service.operations.example.com",
                                code=0,
                                msg="Not implemented yet")
    return handle_get(template)

@app.route('/Authentication', methods=['POST'])
def login():
    template = render_template('response.xml',
                                name="login",
                                namespace="http://schema.auth.example.com",
                                code=0,
                                msg="Welcome back")
    return handle_get(template)

@app.route('/Download', methods=['POST'])
def download():
    filename = "server/static/SplunkITSI.jpg"
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    template = render_template('response_file.xml',
                                name="getFile",
                                filename=filename,
                                filecontent=encoded_string,
                                filesize=os.path.getsize(filename))
    return handle_get(template)

@app.route(api_handler + '/editBook', methods=['GET'])
def get_wsdl_edit():
    template = render_template(static_wsdl_dir + 'EditBook.wsdl',
                                binding="{}EditBook".format(request.host_url))
    return handle_get(template)

@app.route(api_handler + '/login', methods=['GET'])
def get_wsdl_auth():
    template = render_template(static_wsdl_dir + 'Authentication.wsdl',
                                binding="{}Authentication".format(request.host_url))
    return handle_get(template)

@app.route(api_handler + '/getFile', methods=['GET'])
def get_wsdl_download():
    template = render_template(static_wsdl_dir + 'Download.wsdl',
                                binding="{}Download".format(request.host_url))
    return handle_get(template)


if __name__ == "__main__":
    app.run()
