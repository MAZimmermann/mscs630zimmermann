# IMPORT STATEMENTS

from app import app, db

from app.models import Physician, Record

# SHELL CONTEXT CONFIGURATIONS

# "flask shell" starts an interactive Python shell

# The configurations below allow
#  immediate interaction with application data.
#  Specificially, the Physician and Record tables.

@app.shell_context_processor
def make_shell_context():

  return {'db': db, 'Physician': Physician, 'Record': Record}
