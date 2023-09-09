import streamlit as st
from Utils.bdd import connection_database, get_data_to_df
from helpers.selection import getAlgorims
from Utils.metrics import train_test
import preprocessing
import Utils.plots as pt
import pandas as pd
import plotly.graph_objs as go


st.set_option("deprecation.showPyplotGlobalUse", False)

df = None
table = None


def intro():
    return st.set_page_config(
        page_title="ML Playground",
    )


def header():
    st.title("**Bienvenue dans Stream-ml-diginamic 🧪**")
    st.subheader(
        """
        C'est un endroit où vous pouvez vous familiariser avec les modèles d'apprentissage automatique directement depuis votre navigateur
        """
    )

    st.markdown(
        """
    - 🗂️ Choisissez un jeu de données
    - ⚙️ Sélectionnez un modèle et configurez ses hyperparamètres ou choisissez l'option hyperparamètres optimales 
    - 📉 Entraînez-le et vérifiez ses métriques de performance.
    - 🩺 Diagnostiquez un éventuel surapprentissage ou sous-apprentissage a travers différents courbes tel que la courbe                          d'apprentissage
    -----
    """
    )


def sidebar():
    st.sidebar.selectbox(
        "please select your dataset",
        options=["Diabet inde", "Vin"],
        key="data_sb",
        on_change=changeData,
    )
    st.sidebar.file_uploader(
        "Choose a file",
        type=["csv"],
        key="uploaded_file",
        on_change=load,
        help="Choisir un CSV ayant target comme dernière colonne et point-virgule comme séparation",
    )


def changeAlgo():
    pass


def changeData():
    pass


def load():
    pass


def getData(type, path):
    db = connection_database()
    return get_data_to_df(type, db, path)


if __name__ == "__main__":
    intro()
    sidebar()
    header()
    with st.expander("DataFrame"):
        if st.session_state["uploaded_file"] is not None:
            df = getData("load file", st.session_state["uploaded_file"])
            table = st.table(df.head())
        else:
            df = getData(st.session_state["data_sb"], None)
            table = st.table(df.head())
    if df is not None:
        algorithms = getAlgorims(df)
        with st.expander("Analyse descriptive"):
            st.table(df.describe())
            st.table(df.info())
            st.pyplot(pt.distribution_target(df))
        with st.expander("Etude de corrélation"):
            st.pyplot(pt.etude_correlation(df))

        st.sidebar.selectbox(
            "please select your algorithm",
            options=algorithms.keys(),
            key="algo",
            on_change=changeAlgo,
        )
        st.sidebar.toggle("Modifier les Hyperparamètres", key="on")
        st.sidebar.toggle("Hyperparamètres optimaux", key="optimal")
        model = algorithms[st.session_state["algo"]]()
        preprocessor = preprocessing.DataPreprocessor(df)
        X_train, X_test, y_train, y_test, X, y = preprocessor.preprocess_data()
        if "SVC" in list(algorithms):
            clf = model.fit(X_train, y_train)
            if st.session_state["optimal"]:
                best_model = clf.best_estimator_
                y_pred = best_model.predict(X_test)
                best_params_df = pd.DataFrame(clf.best_params_, index=["Valeur"])
                cm, acc, f1 = train_test(y_pred, y_test, algorithms)
                with st.expander("Evaluation du modéle"):
                    st.pyplot(pt.conf_matrix(y_test, y_pred))
                    st.pyplot(pt.courbe_appr(best_model, X, y))
                    try:
                        st.text(
                            "",
                            help="Evalue la capacité d'un modèle à discriminer entre les classes positives et négatives. Modèle parfait : courbe qui s'élève rapidement vers le coin supérieur gauche, ce qui signifie un TP rate élevé et un FP rate bas à un seuil faible.",
                        )
                        st.pyplot(pt.roc_class(best_model, X_test, y_test))
                    except AttributeError as e:
                        st.error(f"La courbe ROC ne convient pas au modèle SVC")
                with st.expander("Metrics"):
                    jauge = go.Indicator(
                        mode="gauge+number+delta",
                        value=acc,
                        title={"text": f"Accuracy (test)"},
                        domain={"x": [0, 1], "y": [0, 1]},
                        gauge={"axis": {"range": [0, 1]}},
                        delta={"reference": acc},
                    )
                    # fig = go.Figure(jauge)
                    jauge2 = go.Indicator(
                        mode="gauge+number+delta",
                        value=f1,
                        title={"text": f"score f1"},
                        domain={"x": [0, 1], "y": [0, 1]},
                        gauge={"axis": {"range": [0, 1]}},
                        delta={"reference": f1},
                    )
                    fig = go.Figure(jauge)
                    fig1 = go.Figure(jauge2)
                    # img_bytes = fig.to_image(format="png",width = 150, height = 100)
                    # st.image(Image.open(io.BytesIO(img_bytes)),use_column_width=True)
                    col1, _, col2 = st.columns([1, 1, 1])
                    with col1:
                        st.plotly_chart(fig, use_container_width=True)
                    with col2:
                        st.plotly_chart(fig1, use_container_width=True)
                with st.expander("Meilleur parametres"):
                    st.dataframe(best_params_df)
            else:
                y_pred = clf.predict(X_test)

                cm, acc, f1 = train_test(y_pred, y_test, algorithms)
                with st.expander("Evaluation du modèle"):
                    st.text(
                        "",
                        help="Calcule les vrai positifs (haut-gauche), vrai négatifs (bas-droite), faux positifs (bas-gauche), faux négatifs (haut-droite)",
                    )
                    st.pyplot(pt.conf_matrix(y_test, y_pred))
                    st.text(
                        "",
                        help="Représente la performance au fur et à mesure de l'apprentissage. Underfitting : convergence vers une faible performance. Optimal : convergence vers une haute performance. Overfitting : courbe d'entraînement continue à s'améliorer tandis que la courbe de validation stagne ou commence à se dégrader",
                    )
                    st.text("test", help="test").pyplot(pt.courbe_appr(model, X, y))
                    try:
                        st.text(
                            "",
                            help="Evalue la capacité d'un modèle à discriminer entre les classes positives et négatives. Modèle parfait : courbe qui s'élève rapidement vers le coin supérieur gauche, ce qui signifie un TP rate élevé et un FP rate bas à un seuil faible.",
                        )
                        st.pyplot(pt.roc_class(clf, X_test, y_test))
                    except AttributeError as e:
                        st.error(f"La courbe ROC ne convient pas au modèle SVC")
                with st.expander("Metrics"):
                    jauge = go.Indicator(
                        mode="gauge+number+delta",
                        value=acc,
                        title={"text": f"Accuracy (test)"},
                        domain={"x": [0, 1], "y": [0, 1]},
                        gauge={"axis": {"range": [0, 1]}},
                        delta={"reference": acc},
                    )
                    # fig = go.Figure(jauge)
                    jauge2 = go.Indicator(
                        mode="gauge+number+delta",
                        value=f1,
                        title={"text": f"score f1"},
                        domain={"x": [0, 1], "y": [0, 1]},
                        gauge={"axis": {"range": [0, 1]}},
                        delta={"reference": f1},
                    )
                    fig = go.Figure(jauge)
                    fig1 = go.Figure(jauge2)
                    # img_bytes = fig.to_image(format="png",width = 150, height = 100)
                    # st.image(Image.open(io.BytesIO(img_bytes)),use_column_width=True)
                    col1, _, col2 = st.columns([1, 1, 1])
                    with col1:
                        st.plotly_chart(fig, use_container_width=True)
                    with col2:
                        st.plotly_chart(fig1, use_container_width=True)

        else:
            clf = model.fit(X_train, y_train)
            if st.session_state["optimal"]:
                best_model = clf.best_estimator_
                y_pred = best_model.predict(X_test)
                mse, r2 = train_test(y_pred, y_test, algorithms)
                best_params_df = pd.DataFrame(clf.best_params_, index=["Valeur"])
                with st.expander("Evaluation du modéle"):
                    st.text(
                        "",
                        help="Représente la performance au fur et à mesure de l'apprentissage. Underfitting : convergence vers une faible performance. Optimal : convergence vers une haute performance. Overfitting : courbe d'entraînement continue à s'améliorer tandis que la courbe de validation stagne ou commence à se dégrader",
                    )
                    st.pyplot(pt.courbe_appr(best_model, X, y))
                    st.text(
                        "",
                        help="Permet de comparer visuellement la distribution des données réelles à une distribution théorique, avec une ligne droite indiquant une bonne correspondance.",
                    )
                    st.pyplot(pt.quant_quant(y_test, y_pred))
                    st.text(
                        "",
                        help="Examine la répartition des résidus. Idéalement, les résidus devraient suivre une distribution normale centrée sur zéro. Si l'histogramme présente une forme proche d'une courbe en cloche centrée sur zéro, cela indique que le modèle de régression capture correctement la variabilité des données.",
                    )
                    st.plotly_chart(pt.histo_residu(y_test, y_pred))
                with st.expander("Metrics"):
                    jauge = go.Indicator(
                        mode="gauge+number+delta",
                        value=mse,
                        title={"text": f"MSE (test)"},
                        domain={"x": [0, 1], "y": [0, 1]},
                        gauge={"axis": {"range": [0, 1]}},
                        delta={"reference": mse},
                    )
                    # fig = go.Figure(jauge)
                    jauge2 = go.Indicator(
                        mode="gauge+number+delta",
                        value=r2,
                        title={"text": f"score r2"},
                        domain={"x": [0, 1], "y": [0, 1]},
                        gauge={"axis": {"range": [0, 1]}},
                        delta={"reference": r2},
                    )
                    fig = go.Figure(jauge)
                    fig1 = go.Figure(jauge2)
                    # img_bytes = fig.to_image(format="png",width = 150, height = 100)
                    # st.image(Image.open(io.BytesIO(img_bytes)),use_column_width=True)
                    col1, _, col2 = st.columns([1, 1, 1])
                    with col1:
                        st.plotly_chart(fig, use_container_width=True)
                    with col2:
                        st.plotly_chart(fig1, use_container_width=True)
                with st.expander("Meilleur parametres"):
                    st.dataframe(best_params_df)
            else:
                y_pred = clf.predict(X_test)
                mse, r2 = train_test(y_pred, y_test, algorithms)
                with st.expander("Evaluation du modéle"):
                    st.text(
                        "",
                        help="Représente la performance au fur et à mesure de l'apprentissage. Underfitting : convergence vers une faible performance. Optimal : convergence vers une haute performance. Overfitting : courbe d'entraînement continue à s'améliorer tandis que la courbe de validation stagne ou commence à se dégrader",
                    )
                    st.pyplot(pt.courbe_appr(model, X, y))
                    st.text(
                        "",
                        help="Permet de comparer visuellement la distribution des données réelles à une distribution théorique, avec une ligne droite indiquant une bonne correspondance.",
                    )
                    st.pyplot(pt.quant_quant(y_test, y_pred))
                    st.text(
                        "",
                        help="Examine la répartition des résidus. Idéalement, les résidus devraient suivre une distribution normale centrée sur zéro. Si l'histogramme présente une forme proche d'une courbe en cloche centrée sur zéro, cela indique que le modèle de régression capture correctement la variabilité des données.",
                    )
                    st.plotly_chart(pt.histo_residu(y_test, y_pred))
                with st.expander("Metrics"):
                    jauge = go.Indicator(
                        mode="gauge+number+delta",
                        value=mse,
                        title={"text": f"MSE (test)"},
                        domain={"x": [0, 1], "y": [0, 1]},
                        gauge={"axis": {"range": [0, 1]}},
                        delta={"reference": mse},
                    )
                    # fig = go.Figure(jauge)
                    jauge2 = go.Indicator(
                        mode="gauge+number+delta",
                        value=r2,
                        title={"text": f"score r2"},
                        domain={"x": [0, 1], "y": [0, 1]},
                        gauge={"axis": {"range": [0, 1]}},
                        delta={"reference": r2},
                    )
                    fig = go.Figure(jauge)
                    fig1 = go.Figure(jauge2)
                    # img_bytes = fig.to_image(format="png",width = 150, height = 100)
                    # st.image(Image.open(io.BytesIO(img_bytes)),use_column_width=True)
                    col1, _, col2 = st.columns([1, 1, 1])
                    with col1:
                        st.plotly_chart(fig, use_container_width=True)
                    with col2:
                        st.plotly_chart(fig1, use_container_width=True)
