import numpy as np
import streamlit as st
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import GridSearchCV


def en_param_selector():
    params = {}
    if st.session_state["on"]:
        alpha = st.sidebar.number_input("alpha", 0.0, 1.0, 0.5, 0.01)
        l1_ratio = st.sidebar.number_input(
            "L1 Ratio (mixing parameter)", 0.0, 1.0, 0.5, 0.01
        )
        params = {"alpha": alpha, "l1_ratio": l1_ratio}

    if st.session_state["optimal"]:
        parametersGrid = {
            "max_iter": [1, 5, 10],
            "alpha": [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
            "l1_ratio": np.arange(0.0, 1.0, 0.1),
        }
        grid = GridSearchCV(ElasticNet(), parametersGrid, scoring="accuracy", cv=10)
        return grid
    else:
        model = ElasticNet(**params)
        return model
