import os
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

MAIL_USERNAME = os.environ.get("MAIL")  # "bsmchk20@gmail.com"
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")  # "marketpassword1"
MAIL_DEFAULT_SENDER = os.environ.get("MAIL")  # "bsmchk20@gmail.com"
