#!/usr/bin/python3
"""The User module"""
from models.basemodel import BaseModel, Base
from bcrypt import hashpw, checkpw, gensalt
from email.message import EmailMessage
from sqlalchemy import Column, String, ForeignKey
import os
import shutil
import smtplib


class User(BaseModel, Base):
    """The User model"""

    __tablename__ = "users"
    created_by = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(50), nullable=False)
    handle = Column(String(20), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    phone_number = Column(String(50))
    password = Column(String(250), nullable=False)
    role = Column(String(20), nullable=False, default="user")
    role_updater = Column(
        String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def hash_password(self, password: str = None) -> str:
        """Hashes a user's password"""
        if not password or type(password) is not str:
            return None
        return hashpw(password.encode("utf8"), gensalt()).decode("utf8")

    def is_valid_password(self, password: str = None) -> bool:
        """Verifies to ensure that password entered is the same in the DB"""
        if not password or type(password) is not str:
            return False
        if self.password is None:
            return False
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def display_name(self) -> str:
        """Display User name based on email/username/"""
        if self.email is None and self.username is None:
            return ""
        else:
            return "{} (@{})".format(self.name, self.username)

    def generate_password_token(self, user_id: str = None) -> str:
        ...
        """Generated a password token using uuid"""
        """from db.reload import storage

        if not user_id or type(user_id) is not str:
            return None
        user = storage.get_user(user_id)
        if not user:
            raise ValueError()
        token = generate_token()
        storage.update("User", user_id, reset_token=token)
        return token"""

    def update_password(self, token: str = None, password: str = None) -> None:
        """Updates a user's password"""
        from db.reload import storage

        user = storage.search_key_value("User", "reset_token", token)
        if not user:
            raise ValueError()
        user = user[0]
        storage.update(
            "User", user.id, password=self.hash_password(password), reset_token=None
        )

    def send_email_token(self) -> bool:
        """sends token to the user email"""
        from db.reload import storage

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            server.login("placerssocials@gmail.com", "plvp oyzo qjmy eonv")
            message = "Hi {}...\n\nYour verification token is {}.\n\nUse this to validate your email".format(
                self.display_name(), self.reset_token
            )

            msg = EmailMessage()
            msg["Subject"] = "OTP Verifiation"
            msg["From"] = "placerssocials@gmail.com"
            msg["To"] = self.email
            msg.set_content(message)

            server.send_message(msg)
            return True
        except smtplib.SMTPAuthenticationError:
            print(
                "Failed to authenticate with the SMTP server. Check your username and password."
            )
        except smtplib.SMTPRecipientsRefused:
            print("The recipient address was refused by the server.")
        except smtplib.SMTPSenderRefused:
            print("The sender address was refused by the server.")
        except smtplib.SMTPDataError:
            print("The SMTP server refused the email data.")
        except smtplib.SMTPConnectError:
            print("Failed to connect to the SMTP server.")
        except smtplib.SMTPException as e:
            print(f"An SMTP error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return False

    def verify_token(self, token: str = None) -> bool:
        """Verifies an email"""
        if not token or type(token) is not str:
            return False
        if token == self.reset_token:
            return True
        return False

    def change_profile_picture(self, file) -> str:
        """Changes a user's profile picture"""
        from db.reload import storage

        if not file:
            return None
        profile_pic_folder = "profile_pictures/"
        if not os.path.exists(profile_pic_folder):
            os.makedirs(profile_pic_folder)
        file_path = os.path.join(profile_pic_folder, f"{self.id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        self.profile_picture = file_path
        storage.save()
        return file_path
