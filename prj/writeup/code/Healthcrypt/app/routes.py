# IMPORT STATEMENTS ----- ----- ----- ----- -----

from flask         import render_template, flash, redirect, url_for, request, session

from flask_login   import login_user, logout_user, current_user, login_required

from werkzeug.urls import url_parse

from app           import app, db

from app.forms     import LoginForm, RegistrationForm, RecordForm

from app.models    import Physician





# TO-DO: Redirect entirely instead of just loading
#  templates for certain requests





# ROUTES ----- ----- ----- ----- -----

# LOGIN  ----- ----- ----- ----- -----
@app.route("/",      methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():

  if current_user.is_authenticated:
    
    physician = current_user
    
    records = current_user.get_records().all()
    
    return render_template("physician.html",
      physician=physician, records=records)

  form = LoginForm()

  if form.validate_on_submit():

    physician = Physician.query.filter_by(username=form.username.data).first()

    if physician is None or not physician.get_password():

      flash("Invalid username or password.")

      return redirect(url_for("login"))

    login_user(physician)

    next_page = request.args.get("next")

    if not next_page or url_parse(next_page).netloc != "":

      next_page = url_for("physician", username=physician.username)

    return redirect(next_page)

  return render_template("login.html", form=form)





# LOGOUT    ----- ----- ----- ----- -----
@app.route("/logout")
def logout():

  logout_user()

  return redirect(url_for("login"))





# PHYSICIAN ----- ----- ----- ----- -----
@app.route('/physician/<username>')
@login_required
def physician(username):

  form = RecordForm()

  if form.validate_on_submit():

    record = Record(patfname=form.patfname.data, author=current_user)

    db.session.add(record)

    db.session.commit()

    flash("Your record was successfully submitted")

    physician = Physician.query.filter_by(username=username).first_or_404()
  
    records = current_user.get_records().all()
  
    return render_template('physician.html', physician=physician,
      records=records)
  
  physician = current_user
  
  records = current_user.get_records().all()
  
  return render_template("physician.html", physician=physician,
    records=records)





# REGISTER  ----- ----- ----- ----- -----
@app.route("/register", methods=["GET", "POST"])
def register():

  if current_user.is_authenticated:

    physician = current_user.username

    return redirect(url_for("physician", username=physician))

  form = RegistrationForm()

  if form.validate_on_submit():

    physician = Physician(username=form.username.data,
      fname=form.fname.data,
      lname=form.lname.data)

    physician.set_password(form.userpwd.data)

    db.session.add(physician)

    db.session.commit()

    flash("Registration completed!")

    return redirect(url_for("login"))

  #else:

    #return render_template("register.html", form=form)

  return render_template("register.html", form=form)
