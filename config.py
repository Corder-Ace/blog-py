class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:!QAZ2wsx@localhost:3306/blog?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_AUTH_URL_RULE = '/api/v1/login'
    SECRET_KEY = "ace"