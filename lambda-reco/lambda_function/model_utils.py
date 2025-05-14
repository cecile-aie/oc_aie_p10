import boto3
import pickle
import json
import numpy as np

# Configuration S3 (tu peux aussi passer par un fichier config.json ou les variables d'env)
BUCKET = "mycontent-reco-assets"
PREFIX = "reco/"  # Dossier dans le bucket

s3 = boto3.client("s3")


def load_pickle_s3(key):
    response = s3.get_object(Bucket=BUCKET, Key=PREFIX + key)
    return pickle.loads(response["Body"].read())


def load_json_s3(key):
    response = s3.get_object(Bucket=BUCKET, Key=PREFIX + key)
    return json.loads(response["Body"].read())


def load_model_from_s3():
    model = load_pickle_s3("lightfm_model_user_item.pkl")
    user_map = load_json_s3("user_mapping.json")
    item_map = load_json_s3("item_mapping.json")
    clicked = load_json_s3("user_clicked_articles.json")
    return model, user_map, item_map, clicked


def predict_top_k(user_id, model, user_mapping, item_mapping, clicked_articles, k=5):
    user_idx = user_mapping.get(user_id)
    if user_idx is None:
        return []

    item_index_to_id = {v: k for k, v in item_mapping.items()}
    item_id_to_index = item_mapping

    user_clicked = clicked_articles.get(user_id, [])
    if len(user_clicked) < 2:
        return []

    test_item_id = str(user_clicked[-1])
    train_items = set(map(str, user_clicked[:-1]))

    n_items = len(item_mapping)
    scores = model.predict(user_idx, np.arange(n_items))

    filtered = [
        (i, s) for i, s in enumerate(scores)
        if item_index_to_id[i] not in train_items
    ]

    top_k = sorted(filtered, key=lambda x: -x[1])[:k]
    return [item_index_to_id[i] for i, _ in top_k]
