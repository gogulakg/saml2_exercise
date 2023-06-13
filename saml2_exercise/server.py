from flask import Flask

APP_PORT = 8989
# idp metadata url: https://test-idp-o365.geant.org/saml2/idp/metadata.php

app = Flask('saml2-exercise')
app.debug = True
app.secret_key = 'hack me'


@app.route('/')
def default():
    return '<h1>Hello, World!</h1>'


if __name__ == "__main__":
    app.run(host='::', port=str(APP_PORT))
