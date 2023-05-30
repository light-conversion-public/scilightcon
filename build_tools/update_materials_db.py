import pytest

@pytest.skip("Required for syncing before production")
def update_materials_db():
    import pymongo
    import pickle
    import os
    # set $env:CONN_STR to read-only connection string to toolbox-mongo.db

    CONN_STR = os.environ['CONN_STR']

    client = pymongo.MongoClient(CONN_STR)

    db = client['Toolbox']
    collection = db['Materials']

    cursor = collection.find({})

    materials = {element['Key'] : element['Value'] for element in cursor}

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../scilightcon/datasets/data/toolbox_materials.pkl'), 'wb') as f:
        pickle.dump(materials, f)