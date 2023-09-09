import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


def rf_param_selector():
    params = {}
    if st.session_state["on"]:
        criterion = st.sidebar.selectbox("criterion", ["gini", "entropy"])
        n_estimators = st.sidebar.number_input("n_estimators", 50, 300, 100, 10)
        max_depth = st.sidebar.number_input("max_depth", 1, 50, 5, 1)
        min_samples_split = st.sidebar.number_input("min_samples_split", 1, 20, 2, 1)
        max_features = st.sidebar.selectbox(
            "max_features", [None, "auto", "sqrt", "log2"]
        )

        params = {
            "criterion": criterion,
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "min_samples_split": min_samples_split,
            "max_features": max_features,
            "n_jobs": -1,
        }
    if st.session_state["optimal"]:
        param_grid = {
            "n_estimators": [200, 500],
            "max_features": ["auto", "sqrt", "log2"],
            "max_depth": [4, 5, 6, 7, 8],
            "criterion": ["gini", "entropy"],
        }
        grid = GridSearchCV(RandomForestClassifier(), param_grid, cv=5)
        return grid
    else:
        model = RandomForestClassifier(**params)
        return model
