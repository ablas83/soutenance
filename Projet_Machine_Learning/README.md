# Projet_Machine_Learning

# Stream-ml-diginamic 🧪

Stream-ml-diginamic est une application **Streamlit** qui vous permet de manipuler des modèles d'apprentissage automatique directement depuis votre navigateur.

## Comment ça marche ?

1. 🗂️ Vous choisissez et configurez un **jeu de données** à partir d'une liste prédéfinie, il y'a aussi la
possibilité d'importer un fichier csv de votre bureau.
   
2. ⚙️ Vous sélectionnez un **modèle** et réglez ses hyperparamètres, il y'a aussi la possiblité de choisir les 
paramétres par défaut du modéle ou de choisir l'option **hyperparamètres optimales** qui va choisir les meilleurs
paramétres pour le modèle choisit.

3. 📉 L'application permet d'afficher les résultats suivants :
   - **Dataframe** : affiche la base de donnée selectionné.
   - **Analyse descriptive** : visualise un résumé statique du dataframe tel que : la distribution, la tendance centrale et la dispersion des données.
   - **Etude de corrélation** : Affiche la matrice de corrélation entre les colonnes de la base de donnée.
   - **Evaluation du modèle** : Affiche la matrice de confusion, la courbe d'apprentissage, la courbe du ROC pour les modèles de classifications et la courbe d'apprentissage, le diagramme quantile-quantile, le histogramme des résidus,le diagramme de dispersion, le diagramme de dispersion entre les valeurs réelles et prédites pour les modèles de regressions .
   - **Metrics** : Affiche le MSE(mean squared error) et le score r2 pour les modèles de regressions.
                   Affichhe l'accuracy et le score f1 pour les modèles de classifications. 

## Pour exécuter l'application localement
```shell
streamlit run main.py
```

## Structure du code
- `main.py` : le main script pour démarrer l'application
- `utils/`
  - `bdd.py`: Gère la connexion et extraction des données avec une bdd PostgreSQL.
  - `plots.py`: Contient les différents graphes utilisés dans l'app. 
- `models/`: Contient les différents modèles utilisés dans l'app avec les hyperparamètres.
- `preprocessing.py`: Contient les différents opérations de preprocessing appliqués sur la dataset (Gestion des valeurs manaquantes, Conversion des valeurs catégorialles, standarisation). 
- `helpers/`
  - `selection.py` : Selectionne le type d'algorithme (classification, regression) à partir de la base de donnée choisit.

