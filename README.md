# nm_forwarder v2018121201
### A simple and highly configurable URL forwarding service.
---
## About
nm_forwarder is a small, simple but highly configurable URL forwarding service written in Python 3 using Flask. It allows the user to redirect using static or flexibile (wildcard) URLs using regular expressions to other sites using HTTP 301 or 302 codes. Or offer an iframe if its desired.

Written for **[New Motion](https://newmotion.com/)** by [Sacha Ligthert](https://github.com/ligthert/).


## Requirements

* Python 3.4 or higher
* Flask
* Requests

Install the dependencies by executing `pip3 install -r requirements.txt` in the project directory.


## Configuration
You can configure nm_forwarder by setting the **NM_FORWARDER_CONFIG** environment variable:

```sh
$ export NM_FORWARDER_CONFIG='{"debug":"True","port":"80","url_default":"http://www.example.com","url_status":"http://www.example.com/status","url_prometheus":"http://www.example.com/metrics","redirects":[{"from":"http://webserver.example.com/(.*)","to":"http://[1].example.com/webserver"},{"from":"http://services.example.com(.*)","to":"http://www.example.com/services[1]"},{"from":"http://stuff.example.com/","to":"http://foobar.com","type":"frame"}]}'
```

The variable is a JSON formatted string with the following elements, for example:
```json
{
    "debug": "True",
    "port": "80",
    "url_default": "http://www.example.com",
    "url_status": "http://www.example.com/status",
    "url_prometheus": "http://www.example.com/metrics",
    "redirects": [
        {
            "from": "http://webserver.example.com/(.*)",
            "to": "http://[1].example.com/webserver"
        },
        {
            "from": "http://services.example.com(.*)",
            "to": "http://www.example.com/services[1]",
            "type": "301"
        },
        {
            "from": "http://stuff.example.com/",
            "to": "http://foobar.com",
            "type": "frame"
        }
    ]
}
```

* **debug**: (optional) set to `true` if you want to enable debug
* **port**: TCP port number the forwarder will listen to
* **url_default**: Default URL to forward to if no redirects are matched
* **url_status**: status-url to check if an application is running an healthy
* **url_prometheus**: Prometheus exporter URL for collecting metrics
* **redirects**: an array with redirect configuration
 * **from**: URL to match for using regex ( `(.*)` for all your wildcard needs )
 * **to**: URL to redirect to, able to match on **from** using _[1]..[n]_ for a search/replace like function
 * **type**: (optional) "frame" to iframe the target url, "301" for a permanent redirect, "302" is the default method of redirect

## Behaviour
* The rule-engine will process a request sequentially in the order as provided by JSON.
* If a request matches a rule the request will be processed per that rule, send the redirect info to the client and terminate the connection.
* Processing a request is redirecting the client, rewrite if applicable.
* The `debug` variable can be set to from `true` to `TRUE`, any other string will be seen as false.
* When putting this app behind a series of proxies, ensure that the `Host` header is proxied and the `url_status` and `url_prometheus` are what it should be when being called by its full URL. It may take some time figuring this out.

## TODO
The following features are missing and will be added in the next version:

* Refactor it so r/python won't flip their lid.
* Add the ability to use a custom iframe instead of the one provided by nm_forwarder.
