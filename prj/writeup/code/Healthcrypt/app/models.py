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

# PHYSICIAN
class Physician(UserMixin, db.Model):

  id       = db.Column(db.Integer,     primary_key=True, autoincrement="auto")
  
  key      = db.Column(db.LargeBinary())
  
  fname    = db.Column(db.LargeBinary())
  lname    = db.Column(db.LargeBinary())
  
  username = db.Column(db.String(256), index=True, unique=True)
  userpwd  = db.Column(db.String(256))

  records  = db.relationship("Record", backref="author", lazy="dynamic")

  # "__init__" OVERRIDES DEFAULT CONSTRUCTOR
  
  def __init__(self, fname, lname, username, userpwd):
    
    key = Fernet.generate_key()
    
    self.key = key
    
    f = Fernet(key)
    
    self.fname = f.encrypt(fname.encode('utf-8'))
    self.lname = f.encrypt(lname.encode('utf-8'))
    
    self.username = username #f.encrypt(username.encode('utf-8'))
    self.userpwd  = userpwd  #f.encrypt(userpwd.encode('utf-8'))

  # "__repr__" FACILITATES DISPLAY VIA FLASK SHELL SESSION ACCESS

  def __repr__(self):

    return "(Physician: {lname}, {fname})".format(
      lname=self.lname,
      fname=self.fname) 

  # GETTERS USED TO RETRIEVE PHYSICIAN INFO

  def get_key(self):

    return self.key

  def get_password(self):

    return self.userpwd

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

  date_created       = db.Column(db.DateTime, index=True)
  date_last_modified = db.Column(db.DateTime, default=datetime.utcnow)

  patfname = db.Column(db.LargeBinary())
  patlname = db.Column(db.LargeBinary())
  patdob   = db.Column(db.LargeBinary())
  patdiag  = db.Column(db.LargeBinary())

  # "__repr__" FACILITATES DISPLAY VIA FLASK SHELL SESSION ACCESS
  
  def __repr__(self):

    return "(\n\
      Date of Creation:          {date_created}\n\
      Date of Last Modification: {date_last_modified}\n\
      Patient First Name:    {fname}\n\
      Patient Last  Name:    {lname}\n\
      Patient Date of Birth: {patdob}\n\
      Patient Diagnosis:     {patdiag}\n\
      )".format(
      date_created       = self.date_created,
      date_last_modified = self.date_last_modified,
      fname       = self.patfname.decode("utf-8"),
      lname       = self.patlname.decode("utf-8"),
      patdob      = self.patdob.decode("utf-8"),
      patdiag     = self.patdiag.decode("utf-8"))

  # GETTERS USED TO RETRIEVE PATIENT INFO
  
  def get_id(self):

    return self.id

  # SETTERS TO UPDATE PATIENT INFO

  def set_date_created(self):

    self.date_created       = datetime.utcnow()

  def set_date_last_modified(self):

    self.date_last_modified = datetime.utcnow()

  def set_patfname(self, patfname):

    self.patfname = patfname
    
  def set_patlname(self, patlname):

    self.patlname = patlname

  def set_patdob(self, patdob):

    self.patdob   = patdob

  def set_patdiag(self, patdiag):

    self.patdiag  = patdiag