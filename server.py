from json import JSONDecodeError

from geoalchemy2.functions import ST_AsGeoJSON
from sanic import Sanic, response
from sanic.response import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Imovel
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

    return response.json(features)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8070, debug=False, access_log=True)