import numpy as np
import json
from lightfm import LightFM
import pickle

def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def load_mapping(path):
    with open(path, "r") as f:
        return json.load(f)

# # V0 Prédiction depuis un user pas de LOO, on compare des prédictions au réel
# def predict_top_k(user_id, model, user_mapping, item_mapping, k=5):
#     user_idx = user_mapping.get(user_id)
#     if user_idx is None:
#         return []

#     n_items = len(item_mapping)
#     scores = model.predict(user_idx, np.arange(n_items))
#     top_k = np.argsort(-scores)[:k]
#     item_index_to_id = {v: k for k, v in item_mapping.items()}
#     return [item_index_to_id[i] for i in top_k]

# V1 Prédictions avec LOO
def predict_top_k(user_id, model, user_mapping, item_mapping, clicked_articles, k=5):
    user_idx = user_mapping.get(user_id)
    if user_idx is None:
        return []

    item_index_to_id = {v: k for k, v in item_mapping.items()}
    item_id_to_index = item_mapping

    # Articles cliqués par l'utilisateur
    user_clicked = clicked_articles.get(user_id, [])
    if len(user_clicked) < 2:
        return []  # Trop peu d'info pour faire un LOO

    # Leave-one-out : on "retire" le dernier
    test_item_id = str(user_clicked[-1])
    train_items = set(map(str, user_clicked[:-1]))

    # Tous les items disponibles
    n_items = len(item_mapping)
    scores = model.predict(user_idx, np.arange(n_items))

    # Filtrage : on ne recommande pas les articles déjà "vus"
    filtered = [
        (i, s) for i, s in enumerate(scores)
        if item_index_to_id[i] not in train_items
    ]

    # Tri par score
    top_k = sorted(filtered, key=lambda x: -x[1])[:k]
    return [item_index_to_id[i] for i, _ in top_k]
