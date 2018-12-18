# Flask SOAP Server Mock
A simple example of how to use [Flask](http://flask.pocoo.org/) to build a SOAP server from `WSDL` files.

## Pre-Requisites
Make sure you have locally installed:
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)

## Usage
Open your terminal and go to your directory `flask-soap-server-mock`. You can decide to deploy the server in two ways:

1. locally
```bash
~$ pipenv install
~$ ./bootstrap.sh
```

2. via Docker
```bash
# Build image
~$ docker build -t flasksoap:latest .
# Run the container
~$ docker run --name flask -d -p 5000:5000 flasksoap
```

You can now issue requests to your API as you prefer. An example is given by the provided SOAP client, which triggers sample requests to the server and parses returned responses.

```bash
~$ cd client
~$ pipenv install && pipenv shell
(client) ~$ ./cli.py --help
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --version            Show the version and exit.
  -H, --host TEXT      SOAP Web Server
  -p, --port TEXT      Web Server Port
  -U, --username TEXT  Username to login
  -P, --password TEXT  Password to login
  --help               Show this message and exit.

Commands:
  download
  edit
  login
```

### Example: Login
```bash
(client) ~$ ./cli.py login
Response code '0' with message 'Welcome back'
```

## Customisations
### Assign a public endpoint to your local flask application
When your SOAP client is hosted in an external machine, your flask server running locally requires a public URL to be reachable. An easy solution would be using [ngrok](https://ngrok.com/).
* If never used before, register and follow instructions to install and locally configure it
* In terminal execute `ngrok http 5000`
* Among printed output you should see a line starting with *Forwarding*, specifying something similar to `http://xyz.ngrok.io -> localhost:5000`
* Make sure that:
  * your SOAP binding location uses this hostname and port, and
  * your client points to this URL

### Add another `WSDL` service
* Add your `wsdl` file to `server/templates/wsdl`
* Make sure `wsdl` binding location matches `<soap12:address location="{{ binding }}" />`
* Integrate your new routes in `server/index.py` similarly to what's done in the example

> The binding automatically discovers the requesting host. Manual changes are possible.

### Add another SOAP response
Similarly to `response.xml`, create your own template in `server/templates` and refers to it when building your route(s) in `index.py`.

## Contributions
So, do you want to use this mock for your own testing? Great!
* Want to contribute? Even better! Feel free to create a [PR](https://github.com/edro15/flask-soap-server-mock/pulls)
* Found a bug? Open an [issue](https://github.com/edro15/flask-soap-server-mock/issues)

## License
MIT Licensed. See [LICENSE](https://github.com/edro15/flask-soap-server-mock/blob/master/LICENSE) for full details.
