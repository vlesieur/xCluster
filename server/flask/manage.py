from flask_script import Server, Manager, Shell

from application.app import app, db

manager = Manager(app)
manager.add_command('runserver', Server(host="0.0.0.0", port=8090))
manager.add_command('shell', Shell(make_context=lambda: {
    'app': app,
    'db': db
}))

if __name__ == '__main__':
    manager.run()