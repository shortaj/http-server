# http-server

The step2 of this server client interaction now parses client requests and only accepts GET requests but has error codes for the invalid requests. These include 500(server error), 405(method error), 505(bad HTTP version), and 400(Bad Request). 