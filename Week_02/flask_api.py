from flask import Flask
#from flask import jsonify
from flask import Response
import os
import sys
from sqlalchemy import Column, ForeignKey, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
import json

app = Flask(__name__)

Base = declarative_base()

class ErrorLog(Base):
    __tablename__ = 'errorlog'
    id = Column(Integer, primary_key=True)
    error_type = Column(String(250))
    error_name = Column(String(250))
    error_date = Column(DateTime, default=datetime.utcnow)

engine = create_engine('sqlite:///error_log.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

some_error = session.query(ErrorLog).first()
err_dict = dict()
js = { 'errors': [] }
for err in session.query(ErrorLog).all():
#   print(f'{err.error_date}: {err.error_type} - {err.error_name}')
    js['errors'].append({'date': str(err.error_date),'type': err.error_type, 'name': err.error_name})


@app.route("/")
def hello():
    return Response(json.dumps(js),  mimetype='application/json')
    