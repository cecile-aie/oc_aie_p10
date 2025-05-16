# 📚 Application de recommandation de contenu - MVP

Ce projet est un système de recommandation de contenu implémenté dans le cadre du parcours AI Engineer OpenClassrooms. Il démontre un MVP complet de bout en bout avec un déploiement serverless.

---

## 🎯 Objectif

Proposer à un utilisateur identifié les 5 articles les plus pertinents à recommander, en fonction de ses interactions passées.

---

## 🧪 Approches explorées

### 1. 🔍 Content-Based Filtering
- Basé sur les embeddings d’articles (réduits par PCA)
- Similarité calculée entre clics passés et articles non vus

### 2. 👥 Collaborative Filtering avec Surprise
- Tests avec SVD, SVD++, KNNBasic
- Plusieurs représentations des interactions implicites
- Evaluation pédagogique en 2 temps : transformation des clics + choix d’algorithme

### 3. 💡 Collaborative Filtering implicite avec `implicit`
- Modèles ALS, BPR, logistic
- Métriques : Hit@5, MAP@5, NDCG@5, RMSE
- Pipeline leave-one-out + grid search

### 4. 🧬 Tentatives hybrides (LightGBM, LightFM)
- Intégration des embeddings comme `item_features`
- Tests avec hybridation via LightFM Dataset API

---

## ✅ Choix final

> Le modèle retenu pour le MVP est **LightFM** avec **matrice user-item uniquement**, pour sa simplicité, sa vitesse et sa bonne expressivité implicite.

---

## ⚙️ Architecture technique

| Composant                  | Implémentation                                                               |
| -------------------------- | ---------------------------------------------------------------------------- |
| 🔍 Recommandation          | `LightFM` sans OpenMP, en production avec Lambda                             |
| 🗺️ Visualisation          | Graphe `Plotly 3D` interactif dans une page HTML statique                    |
| 🌐 Frontend                | Hébergé sur S3 (`mycontent-reco-frontend`)                                   |
| ⚙️ Backend API             | AWS Lambda + accès S3, CORS configuré                                        |
| 🚀 Déploiement automatique | GitLab CI/CD intelligent (déploiement sélectif par dossier modifié)          |
| 🔐 Sécurité                | Accès public maîtrisé via `--acl public-read` + clé IAM via GitLab Variables |

---

## 🔁 Déploiement automatisé (GitLab CI/CD)

Pipeline exécuté à chaque `push` sur `main` :
- 🔁 Sync des fichiers vers S3 (`reco-assets/`)
- 📤 Mise à jour du site statique (`s3-frontend/`)
- 📦 Packaging et déploiement de la Lambda (`lambda_function/`)

Clés AWS injectées via les variables GitLab :
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

Le projet est en accès public sur github :
https://github.com/cecile-aie/oc_aie_p10.git
---

## 🚀 Accès en production

- **Site web** : [https://mycontent-reco-frontend.s3.eu-west-3.amazonaws.com/index.html](https://mycontent-reco-frontend.s3.eu-west-3.amazonaws.com/index.html)
- **Lambda Function URL** : sécurisée, accessible publiquement avec CORS

---

## 🧠 À terme : perspectives

- Ajouter un environnement `staging`
- Affichage enrichi des résultats (tuiles, scores, contextes)
- Exploration de modèles plus avancés (context-aware, multi-facteurs)

---

## 👤 Auteur

Projet réalisé par Cécile dans le cadre du parcours OpenClassrooms — AI Engineer.
