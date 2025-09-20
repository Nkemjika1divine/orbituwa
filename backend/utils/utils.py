#!/usr/bin/python3
"""Utility module"""
import random
import re


def check_if_word_exists(word: str = None, sentence: str = None) -> bool:
    """Uses regex to check if a word exists in another string"""
    if not word or not sentence:
        return False

    pattern = re.compile(re.escape(word), re.IGNORECASE)
    if pattern.search(sentence):
        return True
    return False


def sort_dict_by_values(dictionary, reverse: bool = True):
    """Sorts a dictionary by value"""
    return {
        keys: values
        for keys, values in sorted(
            dictionary.items(), key=lambda item: item[1], reverse=reverse
        )
    }


def generate_token():
    """Generates a randon 6 digit number and returns it"""
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 9))
    return otp


def get_user_by_email(email: str):
    """Finds a user by the email address"""
    from db.reload import storage

    users = storage.all("User")
    if users:
        for user in users.values():
            if user.email == email:
                return user
    return None
