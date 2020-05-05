# IMPORT STATEMENTS

from datetime    import datetime
from app         import db, login_manager
from flask_login import UserMixin

"""

From https://cryptography.io/en/latest/fernet/ :

"Fernet is built on top of a number of standard cryptographic primitives..."

Those "standard cryptographic primitives" include:

 - "AES in CBC mode with a 128-bit key for encryption; using PKCS7 padding."

 - "HMAC using SHA256 for authentication."

 - "Initialization vectors are generated using os.urandom()."

"""

from cryptography.fernet import Fernet

# DB TABLE CLASSES

# Physician
class Physician(UserMixin, db.Model):

  id       = db.Column(db.Integer,     primary_key=True, autoincrement="auto")
  key      = db.Column(db.LargeBinary())
  fname    = db.Column(db.String(256))
  lname    = db.Column(db.String(256))
  username = db.Column(db.String(256), index=True, unique=True)
  userpwd  = db.Column(db.String(256))

  records  = db.relationship("Record", backref="author", lazy="dynamic")

  # "__init__" overrides the usual constructor
  def __init__(self, fname, lname, username, userpwd):
    key = Fernet.generate_key()
    self.key = key
    f = Fernet(key)
    self.fname = fname#f.encrypt(fname.encode('utf-8'))
    self.lname = lname#f.encrypt(lname.encode('utf-8'))
    self.username = username#f.encrypt(username.encode('utf-8'))
    self.userpwd  = userpwd#f.encrypt(userpwd.encode('utf-8'))

  # "__repr__" defines representation when accessed via flask shell session
  def __repr__(self):
    return "(Physician: {lname}, {fname})".format(
      lname=self.lname,
      fname=self.fname) 

  # Returns Physician's Key
  def get_key(self):
    return self.key

  # Returns Physician's Key
  def get_password(self):
    return self.userpwd

  # Returns Physician's Records
  def get_records(self):
    records = Record.query.filter_by(phys_id=self.id)
    return records

# Sets callback for reloading a user from the session
@login_manager.user_loader
def load_user(id):

  return Physician.query.get(int(id))

# RECORD
class Record(db.Model):

  id             = db.Column(db.Integer,  primary_key=True, autoincrement="auto")
  phys_id        = db.Column(db.Integer,  db.ForeignKey('physician.id'))
  create_date    = db.Column(db.DateTime, index=True)
  last_edit_date = db.Column(db.DateTime, default=datetime.utcnow)
  
  patfname = db.Column(db.LargeBinary())
  patlname = db.Column(db.LargeBinary())
  patdob   = db.Column(db.LargeBinary())
  patdiag  = db.Column(db.LargeBinary())

  # "__repr__" defines representation when accessed via flask shell session
  def __repr__(self):

    return "(Creation Date: {create_date}, Patient: {lname}, {fname})".format(
      create_date = self.create_date,
      lname     = self.patlname,
      fname     = self.patfname)

  # Returns the record's id
  def get_id(self):
    return self.id

  # Setters used for updating patient information

  def set_create_date(self):
    self.create_date = datetime.utcnow()

  def set_last_edit_date(self):
    self.last_edit_date = datetime.utcnow()

  def set_patfname(self, patfname):
    self.patfname = patfname
    
  def set_patlname(self, patlname):
    self.patlname = patlname

  def set_patdob(self, patdob):
    self.patdob = patdob

  def set_patdiag(self, patdiag):
    self.patdiag = patdiag