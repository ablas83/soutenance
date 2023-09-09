import streamlit as st
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.model_selection import GridSearchCV


def nn_param_selector():
    params = {}
    if st.session_state['on'] :
        number_hidden_layers = st.sidebar.number_input("number of hidden layers", 1, 5, 1)

        hidden_layer_sizes = []

        for i in range(number_hidden_layers):
            n_neurons = st.sidebar.number_input(
                f"Number of neurons at layer {i+1}", 2, 200, 100, 25
            )
            hidden_layer_sizes.append(n_neurons)

        hidden_layer_sizes = tuple(hidden_layer_sizes)

        activation = st.sidebar.selectbox(
            "activation", options=["relu", "logistic", "tanh", "identity"]
        )

        solver = st.sidebar.selectbox(
            "solver", options=["adam", "sgd", "lbfgs"]
        )

        max_iter = st.sidebar.number_input("max_iter", 100, 2000, step=50, value=100)


        params = {
            "hidden_layer_sizes" : hidden_layer_sizes,
            "activation" : activation,
            "solver" : solver,
            "max_iter" : max_iter
        }

    if st.session_state['optimal'] :
        parameters = {'solver': ['lbfgs'], 'max_iter': [1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000 ], 'alpha': 10.0 ** -np.arange(1, 10), 'hidden_layer_sizes':np.arange(10, 15), 'random_state':[0,1,2,3,4,5,6,7,8,9]}
        clf = GridSearchCV(MLPClassifier(), parameters, n_jobs=-1)
        return clf
    else:
        model = MLPClassifier(**params)
        return model