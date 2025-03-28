from flask import Flask
from .create_app import create_app_def

app = create_app_def()

if __name__ == '__main__':
    app.run(debug=True)
