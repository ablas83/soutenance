import numpy as np
from sklearn.linear_model import Lasso
import streamlit as st
from sklearn.model_selection import GridSearchCV


def rl_param_selector():
    params = {}
    if st.session_state["on"]:
        alpha = st.sidebar.number_input("alpha", 0.00, 100.00, 0.10, 0.05)
        params = {"alpha": alpha}
    if st.session_state["optimal"]:
        alphas = np.logspace(-4, -0.5, 30)
        tuned_parameters = {"alpha": alphas}
        clf = GridSearchCV(Lasso(), tuned_parameters, cv=5)
        return clf
    else:
        model = Lasso(**params)
        return model
