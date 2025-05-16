[![Voir sur GitLab](https://img.shields.io/badge/🔒_Code_complet_sur-GitLab-FC6D26?logo=gitlab&logoColor=white)](git@cecile-proj.duckdns.org:oc_aie/p10-realisez-une-application-de-recommandation-de-contenu.git)
[![Webapp en ligne](https://img.shields.io/badge/🖼️_Webapp_en_ligne-S3-blue?logo=amazon-aws&logoColor=white)](https://mycontent-reco-frontend.s3.eu-west-3.amazonaws.com/index.html)

> 🚀 **Code complet disponible sur GitLab**
>
> Ce dépôt GitHub est une copie publique nettoyée à des fins de consultation.
> Le dépôt complet contient :
> - les modèles entraînés (.pkl, .npz)
> - le layer Lambda zippé
> - les scripts de déploiement
>
> 👉 Accéder au dépôt complet : [gitlab.com/cecile-aie/oc_aie_p10](git@cecile-proj.duckdns.org:oc_aie/p10-realisez-une-application-de-recommandation-de-contenu.git)


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

## 🧱 Architecture technique

| Composant                  | Implémentation / Fonctionnalité                                               | Emplacement / Rôle                                        |
| -------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------- |
| 🔍 Recommandation          | `LightFM` compilé sans OpenMP, exécuté dans une **fonction AWS Lambda**       | Back-end principal (reco-lambda)                          |
| 🗺️ Visualisation          | Graphe `Plotly 3D` intégré dans une **page HTML statique**                    | Généré offline, intégré dans la webapp S3                 |
| 🌐 Frontend                | Application Flask simplifiée, déployée comme site statique **S3**             | `mycontent-reco-frontend` – accès public                  |
| ⚙️ Backend API             | **Lambda AWS** avec point d’accès URL + accès lecture aux assets S3           | Exécuté serverless, non public, appelé depuis le frontend |
| 🚀 Déploiement automatique | Pipeline **GitLab CI/CD** intelligent (push conditionnel par dossier modifié) | Orchestration des builds, déploiements S3 et Lambda       |
| 🔐 Sécurité                | Accès public maîtrisé (`--acl public-read`) + **clé IAM chiffrée GitLab**     | Sécurisé via GitLab CI/CD avec variables protégées        |
| 📁 Code complet            | Contient modèles `.pkl`, `.npz`, scripts Lambda, CI/CD, frontend              | 🔒 GitLab (privé)                                         |
| 📂 Miroir public           | Copie nettoyée sans gros fichiers, avec badges + lien vers GitLab             | GitHub (public, en lecture seule)                         |

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
