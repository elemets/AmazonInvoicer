from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()

class Invoice(Base):
    __tablename__ = 'invoice'
    
    order_number = Column('order_number', String, primary_key=True)
    invoice_number = Column('invoice_number', String, unique=True)
    date_of_purchase = Column('date_of_purchase', DateTime)
    market_origin = Column('origin', String)
    title = Column('title', String)
    invoice_submitted = Column("invoice_submitted", Boolean, default=False)    
    
engine = create_engine('sqlite:///invoices.db', echo=True)


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()



session.close()