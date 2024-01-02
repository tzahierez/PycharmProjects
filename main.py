# run.py
import os

from app import create_app
from app import db
import logging

app = create_app()
#app.logger.info('SQLALCHEMY_DATABASE_URI: %s', app.config['SQLALCHEMY_DATABASE_URI'])
print('server is starting!\nSQLALCHEMY_DATABASE_URI: %s', app.config['SQLALCHEMY_DATABASE_URI'])
print(f'server is starting!\nSQLALCHEMY_DATABASE_URI: {app.config["SQLALCHEMY_DATABASE_URI"]}\n'
      f'OPENAI_API_KEY: {os.getenv("OPENAI_API_KEY")}\n'
      f'UPLOAD_FOLDER" {app.config["UPLOAD_FOLDER"]}\n')

x=os.getenv("OPENAI_API_KEY")
print('OPENAI_API_KEY: %s', x)
print(app.config)

if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=False)
