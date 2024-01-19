'''
Flask  SQLALchemy : pip install Flask-SQLAlchemy
SQLALchemy : pip install SQLAlchemy
'''
##############################################################################################

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer,String,ForeignKey
from flask import Flask
from Connexion import Base , DB_URL
from Experience import Experience
from Ecolab import Ecolab

##############################################################################################

db = SQLAlchemy()

class Cellule(Base):
    __tablename__= 'cellules'
    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    experience_id = Column(Integer, ForeignKey('experience.id'))
    ecolab_id = Column(Integer,ForeignKey('ecolab.id'))
    #experience = relationship('Experience', back_populates='cellules')

    


Base.metadata.create_all(DB_URL)