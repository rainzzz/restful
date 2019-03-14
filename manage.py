from flask_script import Manager

from admin.app import create_app

app = create_app('dev')
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
