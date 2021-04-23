import re
def formatPhoneNum(phone_num):
    # get numerical values of phone number
    return re.sub('[^0-9]', '', phone_num)

