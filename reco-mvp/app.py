import streamlit as st
import pandas as pd
import json
import plotly.express as px
from lambda_handler import load_model, load_mapping, predict_top_k

# Chargement des fichiers
model = load_model("model/lightfm_model_user_item.pkl")
user_mapping = load_mapping("model/user_mapping.json")
item_mapping = load_mapping("model/item_mapping.json")
clicked_articles = json.load(open("user_clicked_articles.json"))
# embeddings_df = pd.read_csv("article_embeddings_2d.csv")
embeddings_df = pd.read_csv("article_embeddings_3d.csv")

# Interface Streamlit
st.title("Système de recommandation - MVP local")

# Remplacement du menu déroulant par une saisie manuelle
user_input = st.text_input("Identifiant utilisateur")
st.caption("Entrez un ID entre 0 et 322887 — attention les utilisateurs avec < 3 interactions sont filtrés.")

if user_input and user_input in clicked_articles:

    user_id = user_input
    # top_k_items = predict_top_k(user_id, model, user_mapping, item_mapping) # V0
    top_k_items = predict_top_k(user_id, model, user_mapping, item_mapping, clicked_articles)

    # Conversion des IDs en chaînes
    clicked = set(map(str, clicked_articles[user_id]))
    recommended = set(map(str, top_k_items))
    relevant_items = clicked.union(recommended)

    # Préparation des données pour affichage
    embeddings_df["item_id"] = embeddings_df["article_id"].astype(str)
    filtered_df = embeddings_df[embeddings_df["item_id"].isin(relevant_items)].copy()

    # Définir couleur, forme et taille
    def get_properties(item_id):
        if item_id in clicked and item_id in recommended:
            return "green", "diamond", 12  # Cliqué et recommandé
        elif item_id in clicked:
            return "blue", "circle", 6     # Cliqué
        elif item_id in recommended:
            return "orange", "circle", 12  # Recommandé

    filtered_df[["color", "symbol", "size"]] = filtered_df["item_id"].apply(
        lambda x: pd.Series(get_properties(x))
    )

    # # Tracé Plotly 2D avec forme et taille personnalisées
    # fig = px.scatter(
    #     filtered_df,
    #     x="x", y="y",
    #     color="color",
    #     symbol="symbol",
    #     size="size",
    #     hover_name="item_id",
    #     color_discrete_map={"blue": "blue", "orange": "orange", "green": "green"},
    #     title="Visualisation des recommandations vs clics"
    # )
    # fig.update_layout(showlegend=False)
    # st.plotly_chart(fig)
    fig = px.scatter_3d(
    filtered_df,
    x="x", y="y", z="z",                # coordonnées 3D
    color="color",
    symbol="symbol",
    size="size",
    hover_name="item_id",
    color_discrete_map={"blue": "blue", "orange": "orange", "green": "green"},
    title="Recommandations vs clics (3D)"
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)


    # Légende personnalisée (conservée)
    st.markdown("🔵  article cliqué")
    st.markdown("🟠  article recommandé")
    st.markdown("🟢  article cliqué **et** recommandé")

    # Résumés
    st.markdown("### 📄 Résumé")
    st.markdown(f"**Articles cliqués** : {sorted(map(int, clicked_articles[user_id]))}")
    # Mise en forme : recommandations avec surlignage si clic
    top_k_items_display = []
    for item in top_k_items:
        if item in clicked:
            top_k_items_display.append(f"<span style='color:green; font-weight:bold'>{int(item)}</span>")
        else:
            top_k_items_display.append(str(int(item)))
    joined = ", ".join(top_k_items_display)
    st.markdown(f"**Articles recommandés** : {joined}", unsafe_allow_html=True)


elif user_input:
    st.warning("Utilisateur inconnu. Veuillez saisir un identifiant valide.")
