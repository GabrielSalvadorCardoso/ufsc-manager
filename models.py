from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Imovel(Base):
   __tablename__ = 'imovel'
   __table_args__ = {'schema': 'public'}

   id = Column('id', Integer(), primary_key=True, nullable=False)
   nome = Column('nome',String(length=100),nullable=True)
   geom = Column('geom',Geometry(geometry_type='MULTIPOLYGON', srid=4674, from_text='ST_GeomFromEWKT', name='geometry'),nullable=True)

# class Solicitacao(Base):
#    pass