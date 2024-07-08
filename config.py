import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://M-HAMDY\\PC/El-Moustafadb?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
