import streamlit as st
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV


def dt_param_selector():
    params = {}
    if st.session_state["on"]:
        st.session_state["criterion"] = 0
        criterion = st.sidebar.selectbox(
            "criterion", ["gini", "entropy"], index=st.session_state["criterion"]
        )
        max_depth = st.sidebar.number_input("max_depth", 1, 50, 5, 1, key="max_depth")
        min_samples_split = st.sidebar.number_input(
            "min_samples_split", 1, 20, 2, 1, key="min_samples_split"
        )
        max_features = st.sidebar.selectbox(
            "max_features", [None, "auto", "sqrt", "log2"], key="max_features"
        )

        params = {
            "criterion": criterion,
            "max_depth": max_depth,
            "min_samples_split": min_samples_split,
            "max_features": max_features,
        }

    if st.session_state["optimal"]:
        m = GridSearchCV(
            DecisionTreeClassifier(random_state=42),
            {
                "criterion": ["gini", "entropy"],
                "max_depth": list(range(1, 51, 10)),
                "min_samples_split": list(range(1, 21, 5)),
                "max_features": [None, "auto", "sqrt", "log2"],
            },
            cv=5,
            verbose=True,
        )
        return m
    else:
        model = DecisionTreeClassifier(**params)
        return model
