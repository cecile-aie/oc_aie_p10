# Dockerfile de référehce
FROM jupyter/scipy-notebook:python-3.11

# Installation des bibliothèques utiles pour le content-based
RUN pip install scikit-learn pandas numpy matplotlib seaborn
