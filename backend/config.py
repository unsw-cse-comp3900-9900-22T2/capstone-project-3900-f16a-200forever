DEBUG = True
PORT = "8080"
SECRET = "200200"
TRAP_HTTP_EXCEPTIONS = True
# adjust database uri for ur machine
SQLALCHEMY_DATABASE_URI= "mysql+pymysql://admin:1234qwer@db.cf2aeefa3bna.ap-southeast-2.rds.amazonaws.com:3306/dev"
# SQLALCHEMY_DATABASE_URI= "mysql+pymysql://root:iampassword@localhost:3306/movie"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "SECRETKEYYYYYY"
SESSION_TYPE = "redis"
SESSION_REDIS = "redis://localhost:6379"
SESSION_PERMANENT = False
EMAIL='19167640706@163.com'
MAIL_PASS='CLHVHYHNZXFYPFYU'
SMTP_SERVER = 'smtp.163.com'