# IMPORT STATEMENTS

import os

# ESTABLISH ABSOLUTE PATH OF BASE DIRECTORY

basedir = os.path.abspath(os.path.dirname(__file__))

# CONFIGURATION CLASS

class Config(object):

  """
  Allows us to use the convenient "config.from_object()" in
   "__init__.py" and conduct configuration changes in one place
  """

  # Used for securely signing the session cookie
  SECRET_KEY = os.environ.get("SECRET_KEY") or "MarcusZimmermann"

  # The database URI that should be used for the connection
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
  "sqlite:///" + os.path.join(basedir, "Healthcrypt.db")

  # Flask-SQLAlchemy will track modifications of objects and emit signals
  SQLALCHEMY_TRACK_MODIFICATIONS = False
