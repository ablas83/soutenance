import streamlit as st
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV


def rd_param_selector():
    params = {}
    if st.session_state["on"]:
        alpha = st.sidebar.number_input("alpha", 0.0, 100.0, 10.0, 1.0)
        params = {"alpha": alpha}
    if st.session_state["optimal"]:
        parameters = {"alpha": [1, 10]}
        Ridge_reg = GridSearchCV(Ridge(), parameters, cv=5)
        return Ridge_reg
    else:
        model = Ridge(**params)
        return model
