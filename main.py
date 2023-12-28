# run.py
from app import create_app
from app import db
import logging

app = create_app()
#app.logger.info('SQLALCHEMY_DATABASE_URI: %s', app.config['SQLALCHEMY_DATABASE_URI'])
print('server is starting!\nSQLALCHEMY_DATABASE_URI: %s', app.config['SQLALCHEMY_DATABASE_URI'])

if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=False)
