import csv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///mydatabase.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Station(Base):
    __tablename__ = 'clean_stations'
    id = Column(Integer, primary_key=True)
    station = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    elevation = Column(String)
    name = Column(String)
    country = Column(String)
    state = Column(String)

    measures = relationship("Measure", back_populates="station")

class Measure(Base):
    __tablename__ = 'clean_measure'
    id = Column(Integer, primary_key=True)
    station_id = Column(Integer, ForeignKey('clean_stations.id'))
    date = Column(Date)
    precip = Column(String)
    tobs = Column(String)

    station = relationship("Station", back_populates="measures")

Base.metadata.create_all(engine)

# Завантаження даних з файлу clean_stations.csv
with open('clean_stations.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        station = Station(station=row['station'], latitude=row['latitude'], longitude=row['longitude'], elevation=row['elevation'], name=row['name'], country=row['country'], state=row['state'])
        session.add(station)

# Завантаження даних з файлу clean_measure.csv
with open('clean_measure.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        date = datetime.strptime(row['date'], '%Y-%m-%d').date()
        measure = Measure(station_id=row['station'], date=date, precip=row['precip'], tobs=row['tobs'])
        session.add(measure)

session.commit()
