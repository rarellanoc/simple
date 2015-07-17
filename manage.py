from flask.ext.script import Manager


from app import app
from app.model import db

manager = Manager(app)
manager.add_option('-c', '--config', dest='config', required=False)

@manager.command
def initdb():
    """initialize database"""
    
    
    
    
    db.drop_all()
    db.create_all()

if __name__ == "__main__":
    
    manager.run()
