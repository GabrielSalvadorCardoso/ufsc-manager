import datetime

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Imovel(Base):
   __tablename__ = 'imovel'
   __table_args__ = {'schema': 'public'}

   id = Column('id', Integer(), primary_key=True, nullable=False)
   nome = Column('nome',String(length=100),nullable=True)
   geom = Column('geom',Geometry(geometry_type='MULTIPOLYGON', srid=4674, from_text='ST_GeomFromEWKT', name='geometry'),nullable=True)

class Solicitacao(Base):
   __tablename__ = 'solicitacao'
   __table_args__ = {'schema': 'public'}

   id = Column('id', Sequence('solicitacao_id_seq'), primary_key=True, nullable=False)
   numero_os = Column('numero_os', Sequence('solicitacao_numero_os_seq'), nullable=False) # Número da OS
   tipo = Column('tipo', String(length=50), nullable=False)  # Tipo (Elétrica | Hidráulica | Infraestrutura)
   natureza = Column('natureza', String(length=50), nullable=False) # Tipo (Corretiva | Preventiva | Evolutiva)
   responsavel = Column('responsavel', String(length=100), nullable=False) # Responsável
   data_abertura = Column('data_abertura', DateTime(), default=datetime.datetime.now(), nullable=False) # Data Abertura | Entreda
   interessado = Column('interessado', String(length=100), nullable=False) # Solicitante | Interessado | Interessado na UFSC
   detalhamento = Column('detalhamento', String(length=500), nullable=False) # Detalhamento | Descrição
   n_ufsc = Column('n_ufsc', Sequence('solicitacao_n_ufsc_seq'), nullable=False)  # Solicitação | Número UFSC (000000/YYYY)
   assunto = Column('assunto', String(length=100), nullable=False) # Assunto (0000 - Manutenção SEOME)
   grupo_assunto = Column('grupo_assunto', String(length=100), nullable=False) # Grupo de assunto (000 - Manutenção)
   setor_origem = Column('setor_origem', String(length=100), nullable=False) # Setor origem
   setor_responsavel = Column('setor_responsavel', String(length=100), nullable=False) # Setor responsável
   geom = Column('geom',Geometry(geometry_type='POINT', srid=4674, from_text='ST_GeomFromEWKT', name='geometry'),nullable=True)
   imovel_id = Column(Integer, ForeignKey(f'public.imovel.id', ondelete="CASCADE"))


class HistoricoStatus(Base):
   __tablename__ = 'historico_status'
   __table_args__ = {'schema': 'public'}

   id = Column('id', Integer(), primary_key=True, nullable=False)
   data_hora = Column('data_hora', DateTime(), default=datetime.datetime.now(), nullable=False)
   status = Column('status', String(length=20), nullable=False)  # Status Atual (FINALIZADA | ANDAMENTO | JUSTIFICADA)
   solicitacao_id = Column(Integer, ForeignKey(f'public.solicitacao.id', ondelete="CASCADE"))

# class StatusSolicitacao(Base):
#    __tablename__ = 'status_solicitacao'
#    __table_args__ = {'schema': 'public'}
#
#    id = Column('id', Integer(), primary_key=True, nullable=False)
#    status = Column('status', String(length=20), nullable=False) # Status Atual (FINALIZADA | ANDAMENTO | JUSTIFICADA)

# """
# 1. Qual o papel do responsável?
# """
