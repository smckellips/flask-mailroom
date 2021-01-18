import random

from model import db, Donor, Donation 
from passlib.hash import pbkdf2_sha256
db.connect()

# This line will allow you "upgrade" an existing database by
# dropping all existing tables from it.
db.drop_tables([Donor, Donation])

db.create_tables([Donor, Donation])

alice = Donor(name="Alice", password=pbkdf2_sha256.hash("password"))
alice.save()

bob = Donor(name="Bob", password=pbkdf2_sha256.hash("password"))
bob.save()

charlie = Donor(name="Charlie", password=pbkdf2_sha256.hash("password"))
charlie.save()

donors = [alice, bob, charlie]

for x in range(30):
    Donation(donor=random.choice(donors), value=random.randint(100, 10000)).save()

