from db import Base
from sqlalchemy import event
from sqlalchemy import Column, Float, String, Text, Integer
from elasticsearch import Elasticsearch


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    cve_id = Column(String)
    cvss_score = Column(Float)
    version = Column(String)
    description = Column(Text)
    product_name = Column(String)

def after_entry_insert(mapper, connection, target):
    es = Elasticsearch()
    es.index(index="vulnerability", doc_type="entry", id=target.id,body={"cve_id": target.cve_id, "cvss_score": target.cvss_score, "version": target.version, "description": target.description, "product_name": target.product_name})


def after_entry_update(mapper, connection, target):
    pass

event.listen(Entry, 'after_insert', after_entry_insert)
event.listen(Entry, 'after_update', after_entry_insert)
