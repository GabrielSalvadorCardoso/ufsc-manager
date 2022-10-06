from json import JSONDecodeError

import sqlalchemy
from geoalchemy2.functions import ST_AsGeoJSON
from sanic import Sanic, response
from sanic.response import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Imovel, Solicitacao, HistoricoStatus
import json
from sanic_cors import CORS, cross_origin
# from shapely_geojson import dumps, Feature
# from geoalchemy2.shape import to_shape
from environs import Env
env = Env()
env.read_env()  # read .env file, if it exists
port = env.str("DB_PORT", None)
host = env.str("DB_HOST", None)
user = env.str("DB_USER", None)
password = env.str("DB_PASS", None)
DB_URL = env.str("DB_URL", None)



# engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/postgres', echo=True)
engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# app = Sanic("MyHelloWorldApp")
app = Sanic(__name__)
CORS(app)

@app.route("/solicitacao", methods=["POST"])
async def create_solicitacao(request):



    solicitacao = Solicitacao(
        # numero_os=Column('numero', Integer(), nullable=False)  # Número da OS
        tipo="Elétrica",
        natureza="Corretiva",
        responsavel="EZEQUIEL JOSÉ VIEIRA",
        # data_abertura = Column('data_abertura', DateTime(), nullable=False)  # Data Abertura | Entreda
        interessado="AIRTON COSTA",
        detalhamento="Solicitação: Manutenção da iluminação em virtude de lâmpadas sem funcionamento. Contato: Augusto - manutencao.ced@contato.ufsc.br - 4568 Local: Sala 002, LANTEC, térreo do Bloco A do Centro de Ciências da Educação (CED). Imóvel: CED06-CED - Bloco A Ambiente: Sigla: 002 A / SIP: 7684 / Nome: CED002 A- Núcleo de Formação e Avaliação- LANTEC",
        # n_ufsc = Column('n_ufsc', Integer(), nullable=False)  # Solicitação | Número UFSC (000000/YYYY)
        assunto="1434 - Manutenção SEOMA",
        grupo_assunto="351 - Manutenção",
        setor_origem="DMPI/SEOMA",
        setor_responsavel="DMPI/SEOMA",
        imovel_id=2, #todo: imovel deve vir do frontend
        # historico_status_id=historico_status.id,
        geom="SRID=4674;POINT (-48.519734144210815 -27.60110715979902)"
        # geom="SRID=4674;POLYGON ((-48.51986825466156 -27.600850447903003, -48.51995408535004 -27.601744183017527, -48.51956248283386 -27.601772706358624, -48.519492745399475 -27.60087421754827, -48.51986825466156 -27.600850447903003))"
    )

    session.add(solicitacao)
    # session.commit()
    session.flush()
    print(solicitacao.id)

    historico_status = HistoricoStatus(status="ANDAMENTO", solicitacao_id=solicitacao.id)
    session.add(historico_status)
    session.commit()

    return response.json(body=None, status=201)

@app.route("/solicitacao", methods=["GET"])
async def retrieve_solicitacoes(reqest):
    rows = session.query(
        Solicitacao.id,
        Solicitacao.numero_os,
        Solicitacao.tipo,
        Solicitacao.natureza,
        Solicitacao.responsavel,
        Solicitacao.data_abertura,
        Solicitacao.interessado,
        Solicitacao.detalhamento,
        Solicitacao.assunto,
        Solicitacao.grupo_assunto,
        Solicitacao.setor_origem,
        Solicitacao.setor_responsavel,
        Solicitacao.imovel_id,
        # Solicitacao.historico_status_id,
        ST_AsGeoJSON(Solicitacao.geom)
    ).filter().with_entities(
        Solicitacao.id,
        Solicitacao.numero_os,
        Solicitacao.tipo,
        Solicitacao.natureza,
        Solicitacao.responsavel,
        Solicitacao.data_abertura,
        Solicitacao.interessado,
        Solicitacao.detalhamento,
        Solicitacao.assunto,
        Solicitacao.grupo_assunto,
        Solicitacao.setor_origem,
        Solicitacao.setor_responsavel,
        Solicitacao.imovel_id,
        # Solicitacao.historico_status_id,
        ST_AsGeoJSON(Solicitacao.geom)
    )

    features = []
    for row in rows:
        # row.historico_status_id

        historicos = session.query(HistoricoStatus).filter(HistoricoStatus.solicitacao_id == row.id)
        historico_status = [{"id": h.id, "data_hora": h.data_hora.isoformat(), "status": h.status } for h in historicos]


        feature = {
            "type": "Feature",
            "properties": {
                "id": row.id,
                "numero_os": row.numero_os,
                "tipo": row.tipo,
                "natureza": row.natureza,
                "responsavel": row.responsavel,
                "data_abertura": row.data_abertura.isoformat(),
                "interessado": row.interessado,
                "detalhamento": row.detalhamento,
                "assunto": row.assunto,
                "grupo_assunto": row.grupo_assunto,
                "setor_origem": row.setor_origem,
                "setor_responsavel": row.setor_responsavel,
                "imovel_id": row.imovel_id,
                "historico_status": historico_status
            },
        }
        for attribute_val in list(row):
            try:
                converted_val = json.loads(attribute_val)
                if type(converted_val) == dict:
                    feature["geometry"] = converted_val
                else:
                    continue
            except (JSONDecodeError, TypeError):
                continue
        features.append(feature)

    feature_collection = {
        "type": "FeatureCollection",
        "features": features
    }
    return response.json(feature_collection)

@app.route("/imoveis", methods=["POST"])
async def create_imovel(request):
    name = "Reitoria"
    feature = {
      "type": "Feature",
      "properties": {
          "nome": name
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -48.51986825466156,
              -27.600850447903003
            ],
            [
              -48.51995408535004,
              -27.601744183017527
            ],
            [
              -48.51956248283386,
              -27.601772706358624
            ],
            [
              -48.519492745399475,
              -27.60087421754827
            ],
            [
              -48.51986825466156,
              -27.600850447903003
            ]
          ]
        ]
      }
    }

    wkt_feature = "SRID=4674;POLYGON ((-48.51986825466156 -27.600850447903003, -48.51995408535004 -27.601744183017527, -48.51956248283386 -27.601772706358624, -48.519492745399475 -27.60087421754827, -48.51986825466156 -27.600850447903003))"

    project = Imovel(nome=name, geom=wkt_feature)
    session.add(project)
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
    return response.json(body=None, status=201)

@app.route("/imoveis", methods=["GET"])
async def retrieve_imoveis(request):
    rows = session.query(
        Imovel.id,
        Imovel.nome,
        ST_AsGeoJSON(Imovel.geom)
    ).filter().with_entities(
        Imovel.id,
        Imovel.nome,
        ST_AsGeoJSON(Imovel.geom)
    )

    features = []
    for row in rows:
        feature = {
            "type": "Feature",
            "properties": {
                "id": row.id,
                "nome": row.nome,
            },
        }
        for attribute_val in list(row):
            try:
                converted_val = json.loads(attribute_val)
                if type(converted_val) == dict:
                    feature["geometry"] = converted_val
                else:
                    continue
            except (JSONDecodeError, TypeError):
                continue
        features.append(feature)

    feature_collection = {
        "type": "FeatureCollection",
        "features": features
    }

    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'MultiPolygon',
            'coordinates': [
                [
                    [
                        [-5e6, 6e6],
                        [-3e6, 6e6],
                        [-3e6, 8e6],
                        [-5e6, 8e6],
                        [-5e6, 6e6],
                    ],
                ],
                [
                    [
                        [-2e6, 6e6],
                        [0, 6e6],
                        [0, 8e6],
                        [-2e6, 8e6],
                        [-2e6, 6e6],
                    ],
                ],
                [
                    [
                        [1e6, 6e6],
                        [3e6, 6e6],
                        [3e6, 8e6],
                        [1e6, 8e6],
                        [1e6, 6e6],
                    ],
                ],
            ],
        },
    },

    return response.json(feature_collection)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8070, debug=False, access_log=True)