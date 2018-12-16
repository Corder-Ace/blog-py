import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:949223@localhost:3306/blog?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
