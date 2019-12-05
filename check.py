import os
MAIL_USERNAME = os.environ.get('EMAIL_USER')
MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

print(MAIL_USERNAME)
print(MAIL_PASSWORD)
