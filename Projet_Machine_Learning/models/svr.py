import streamlit as st
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV


def svr_param_selector():
    params = {}
    if st.session_state['on']:
        kernel = st.sidebar.selectbox("Kernel", ["linear", "poly", "rbf", "sigmoid"])
        C = st.sidebar.number_input("C (Regularization parameter)", 0.01, 10.0, 1.0, 0.01)
        epsilon = st.sidebar.number_input("Epsilon", 0.01, 1.0, 0.1, 0.01)
        params = {"kernel": kernel, "C": C, "epsilon": epsilon}
    if st.session_state['optimal'] :
        parametres = {'kernel' : ('linear', 'poly', 'rbf', 'sigmoid'),'C' : [1,5,10],'degree' : [3,8],'coef0' : [0.01,10,0.5],'gamma' : ('auto','scale')}
        grids = GridSearchCV(SVR(),parametres,cv=5)
        return grids
    else:
        model = SVR(**params)
        return model
