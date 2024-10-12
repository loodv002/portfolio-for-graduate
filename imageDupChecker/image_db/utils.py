from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

import os
from datetime import datetime, timedelta
from typing import Optional, List

from .model import Base, ImageRecord

def createSession():
    DBpath = f'{os.path.dirname(__file__)}/image_record.db'
    engine = create_engine(f'sqlite:///{DBpath}?check_same_thread=False')

    Base.metadata.create_all(engine)

    Session = sessionmaker(engine)
    session = Session()
    return session

def recordExist(imagePath: str):
    session = createSession()
    record = session.query(ImageRecord).filter_by(imagePath=imagePath).first()
    session.close()
    return record is not None

def addRecord(imagePath: str, bitmapPath: str, counts: List[int]):
    session = createSession()
    
    newRecord = ImageRecord(
        imagePath = imagePath,
        bitmapPath = bitmapPath,
        count1 = counts[0],
        count2 = counts[1],
        count3 = counts[2],
        count4 = counts[3],
        count5 = counts[4],
        count6 = counts[5],
        count7 = counts[6],
        count8 = counts[7],
        count9 = counts[8],
        count10 = counts[9],
        count11 = counts[10],
        count12 = counts[11],
        count13 = counts[12],
        count14 = counts[13],
        count15 = counts[14],
        count16 = counts[15],
    )
    session.add(newRecord)
    session.commit()
    session.close()

def getRecordByCounts(counts) -> List[ImageRecord]:
    D = 2000

    session = createSession()
    records = session.query(ImageRecord) \
                     .filter(ImageRecord.count1.between(counts[0]-D, counts[0]+D)) \
                     .filter(ImageRecord.count2.between(counts[1]-D, counts[1]+D)) \
                     .filter(ImageRecord.count3.between(counts[2]-D, counts[2]+D)) \
                     .filter(ImageRecord.count4.between(counts[3]-D, counts[3]+D)) \
                     .filter(ImageRecord.count5.between(counts[4]-D, counts[4]+D)) \
                     .filter(ImageRecord.count6.between(counts[5]-D, counts[5]+D)) \
                     .filter(ImageRecord.count7.between(counts[6]-D, counts[6]+D)) \
                     .filter(ImageRecord.count8.between(counts[7]-D, counts[7]+D)) \
                     .filter(ImageRecord.count9.between(counts[8]-D, counts[8]+D)) \
                     .filter(ImageRecord.count10.between(counts[9]-D, counts[9]+D)) \
                     .filter(ImageRecord.count11.between(counts[10]-D, counts[10]+D)) \
                     .filter(ImageRecord.count12.between(counts[11]-D, counts[11]+D)) \
                     .filter(ImageRecord.count13.between(counts[12]-D, counts[12]+D)) \
                     .filter(ImageRecord.count14.between(counts[13]-D, counts[13]+D)) \
                     .filter(ImageRecord.count15.between(counts[14]-D, counts[14]+D)) \
                     .filter(ImageRecord.count16.between(counts[15]-D, counts[15]+D)) \
                     .all()
    return records