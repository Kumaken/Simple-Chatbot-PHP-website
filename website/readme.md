#run php locally:
php -S localhost:8000

#WHEN USING AJAX : 
    to prevent :
        "Access to XMLHttpRequest at 'https://python-nlp-chatbot.herokuapp.com/api/halo' from origin 'http://localhost:8000' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource."
        -reason:
            this is because we are trying to access api on heroku which has different
            combis of protocol(http), host(heroku.com), and port(8080). this triggers
            same origin security policy from chrome. (NOTE POSTMAN IS FINE FOR THIS)
            Cors can fix this. (cross-origin resource sharing)
    INSTALL: 
    (https://chrome.google.com/webstore/detail/allow-control-allow-origi/nlfbmbojpeacfghkpbjhddihlkkiljbi?hl=en-US)

    to allow control allow origin.
        OR APPLY THIS to your flask api:
        from flask import Flask
        from flask.ext.cors import CORS, cross_origin

        app = Flask(__name__)
        cors = CORS(app, resources={r"/foo": {"origins": "*"}})
        app.config['CORS_HEADERS'] = 'Content-Type'