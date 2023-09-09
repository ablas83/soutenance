import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV


def lir_param_selector():

    if st.session_state["optimal"]:
        m = GridSearchCV(LinearRegression(), {}, cv=5, verbose=True)
        return m
    else:
        model = LinearRegression()
        return model
