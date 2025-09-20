#!/usr/bin/python3
"""Module for functions for emails"""
import aiosmtplib
from os import environ
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib

load_dotenv()


async def send_welcome_email(recipient_email: str, display_name: str):
    message = EmailMessage()
    message["From"] = environ.get("MAIL_USERNAME")
    message["To"] = recipient_email
    message["Subject"] = "Welcome to Orbituwa"
    message.set_content(f"Hi {display_name}...\n\nWelcome to Orbituwa")

    await aiosmtplib.send(
        message,
        hostname=environ.get("MAIL_HOST"),
        port=environ.get("MAIL_PORT"),
        username=environ.get("MAIL_USERNAME"),
        password=environ.get("MAIL_PASSWORD"),
        start_tls=True,
    )
