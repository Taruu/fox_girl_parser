import sqlalchemy
from sqlalchemy import create_engine
from database_function.driver import FoxGirlDatabase
import pickle
import time

class database_worker:
    def __init__(self):
        self.sessionWorker = FoxGirlDatabase()


    """Ну все что user"""
    def add_fox(self):
        self.sessionWorker

