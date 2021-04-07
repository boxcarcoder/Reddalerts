import re

def checkPhoneNumberFormat(phone_num):
    # get pure numerical representation.
    


    # check for letters
    phone_num_lowercase = phone_num.lower()
    contains_letters = phone_num_lowercase.islower()
    if contains_letters == True:
        return True



