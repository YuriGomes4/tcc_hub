from app import create_app
import os

from config import Config

# Creating the app.
app = create_app()

# Getting the port from the environment variable PORT or API_PORT.
port = os.environ.get('PORT', os.environ.get('API_PORT'))
#port = 80

app.config.from_object(Config)

from flask import Flask, send_file


@app.route('/.well-known/pki-validation/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)


# This is a way to run the app in production or development mode.
if __name__ == "__main__":
    if os.environ.get('APP_ENV', 'development') == "production":
        app.logger.info('Environment prod running. Port %s', port)
    else:
        app.run(debug=True, host='0.0.0.0', port=port)