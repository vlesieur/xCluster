from flask_script import Server, Manager, Shell
import os
from application.app import app, db

manager = Manager(app)
port = int(os.environ.get('PORT', 5000))
manager.add_command('runserver', Server(threaded=True, host="0.0.0.0", port=port))
manager.add_command('shell', Shell(make_context=lambda: {
    'app': app,
    'db': db
}))

if __name__ == '__main__':
    manager.run()