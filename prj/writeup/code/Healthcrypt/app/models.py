# IMPORT STATEMENTS

from datetime    import datetime
from app         import db, login_manager
from flask_login import UserMixin

# DB TABLE CLASSES

# Physician
class Physician(UserMixin, db.Model):

  id       = db.Column(db.Integer,     primary_key=True)
  fname    = db.Column(db.String(128))
  lname    = db.Column(db.String(128))
  username = db.Column(db.String(128), index=True, unique=True)
  userpwd  = db.Column(db.String(128))

  records  = db.relationship("Record", backref="author", lazy="dynamic")

  def __repr__(self):
    return "(Physician: {lname}, {fname})".format(
      lname=self.lname,
      fname=self.fname) 

  def set_password(self, pw):
    self.userpwd = pw

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

  id             = db.Column(db.Integer,  primary_key=True)
  phys_id        = db.Column(db.Integer,  db.ForeignKey('physician.id'))
  create_date    = db.Column(db.DateTime, index=True)
  last_edit_date = db.Column(db.DateTime, default=datetime.utcnow)
  
  patfname = db.Column(db.String(128))
  patlname = db.Column(db.String(128))
  patdob   = db.Column(db.String(128))
  patdiag  = db.Column(db.String(250))

  def __repr__(self):

    return "(Timestamp: {timestamp}, Physician: {lname}, {fname})".format(
      timestamp = self.timestamp,
      lname     = self.username,
      fname     = self.username)

  def get_id(self):
    return self.id

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