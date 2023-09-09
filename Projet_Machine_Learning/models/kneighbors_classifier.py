import streamlit as st
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV


def knn_param_selector():
    params = {}
    if st.session_state['on'] :
        n_neighbors = st.sidebar.number_input("n_neighbors", 5, 20, 5, 1)
        metric = st.sidebar.selectbox(
        "metric", ("minkowski", "euclidean", "manhattan", "chebyshev", "mahalanobis")
        )

        params = {"n_neighbors": n_neighbors, "metric": metric}
    metric = ["minkowski", "euclidean", "manhattan", "chebyshev", "mahalanobis"]
    k_range = list(range(1, 31))
    param_grid = dict(n_neighbors=k_range, metric=metric)
    if st.session_state['optimal'] :
        grid = GridSearchCV(KNeighborsClassifier(), param_grid, cv=10)
        return grid
    else:
        model = KNeighborsClassifier(**params)
        return model
