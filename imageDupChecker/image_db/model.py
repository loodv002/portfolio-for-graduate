from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ImageRecord(Base):
    __tablename__ = 'image_record'

    imagePath = Column(String(255), primary_key=True)
    bitmapPath = Column(String(255))
    count1 = Column(Integer)
    count2 = Column(Integer)
    count3 = Column(Integer)
    count4 = Column(Integer)
    count5 = Column(Integer)
    count6 = Column(Integer)
    count7 = Column(Integer)
    count8 = Column(Integer)
    count9 = Column(Integer)
    count10 = Column(Integer)
    count11 = Column(Integer)
    count12 = Column(Integer)
    count13 = Column(Integer)
    count14 = Column(Integer)
    count15 = Column(Integer)
    count16 = Column(Integer)


    def __str__(self):
        return f'ImageRecord({self.Path}, {self.bitmapPath})'
    def __repr__(self):
        return str(self)