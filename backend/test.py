from db.reload import storage
from models.user import User

"""user = User(name="m", handle="dshdua", email="a@b.c", password="hdhfsat")
print("Preparing to add")
storage.new(user)
print("added\npreparing to save")
storage.save()
print("saved")"""


print(storage.count("User"))
