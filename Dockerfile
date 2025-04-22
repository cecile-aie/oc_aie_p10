# Dockerfile pour content-based + collaborative filtering
FROM jupyter/scipy-notebook:python-3.11

# Installation des bibliothèques utiles pour le content-based
RUN pip install scikit-learn pandas numpy matplotlib seaborn

# Installation de la bibliothèque Surprise pour le collaborative filtering
RUN pip install scikit-surprise termcolor implicit==0.7.2
