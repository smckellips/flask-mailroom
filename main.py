import base64
import os

from flask import Flask, redirect, render_template, request, session, url_for
from passlib.hash import pbkdf2_sha256

from model import Donation, Donor

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()
app.url_map.strict_slashes = False

@app.before_request
def clear_trailing():
    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('donate.jinja2', session=session)
    donation_amt = request.form.get('donate-amt', None)
    donor = Donor.get(Donor.name == session['user'])
    donation = Donation.create(donor=donor, value=donation_amt)
    donation.save()

    return redirect(url_for('all'))

@app.route('/donations')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    if request.method ==  'POST':
        try:
            name = request.form.get('name', None)
            user = Donor.get(Donor.name == name)
        except Donor.DoesNotExist:
            return render_template('filter.jinja2', error="Incorrect username or password.")
        return render_template('donations.jinja2', donations=Donation.select().where(Donation.donor == user))
    return render_template('filter.jinja2')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method ==  'POST':
        try:
            name = request.form.get('name', None)
            user = Donor.get(Donor.name == name)
            # user = User.select().where(User.name == request.form['name']).get()
            if user and pbkdf2_sha256.verify(request.form.get('password'), user.password):
                session['user'] = user.name
                return redirect(url_for('all'))
        except Donor.DoesNotExist:
            return render_template('login.jinja2', error="Incorrect username or password.")
        return render_template('login.jinja2', error="Incorrect username or password.")
    return render_template('login.jinja2')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user')
    return redirect(url_for('login'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

