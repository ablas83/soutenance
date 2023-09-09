import streamlit as st
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV


def svc_param_selector():
    params = {}
    if st.session_state["on"]:
        C = st.sidebar.number_input("C", 0.01, 100.0, 1.0, 1.0)
        kernel = st.sidebar.selectbox("kernel", ("rbf", "linear", "poly", "sigmoid"))
        params = {"C": C, "kernel": kernel}

    param_grid = {
        "C": [0.1, 1, 10, 100],
        "gamma": [1, 0.1, 0.01, 0.001],
        "kernel": ["rbf", "poly", "sigmoid"],
    }
    if st.session_state["optimal"]:
        grid = GridSearchCV(SVC(), param_grid, cv=5)
        return grid
    else:
        model = SVC(**params)
        return model
