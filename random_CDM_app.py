import streamlit as st
import random
import sqlite3

st.title("🎈 Binôme de CDM pour le mois")


# Connexion à la base de données SQLite (le fichier sera créé s'il n'existe pas)
def create_connection():
    conn = sqlite3.connect('/workspaces/randomCDM-app/cdm.db')
    return conn

# Créer la table si elle n'existe pas déjà
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cdm (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            grade TEXT NOT NULL,
            poids INTEGER NOT NULL,
            selection_count INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Fonction pour vérifier si la table 'cdm' est vide
def is_table_empty():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cdm")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

#Fonction pour initialiser la base de données - A UTILISER QU'UNE FOIS
def insert_initial_data():
    cdm = [
        {"nom": "GUILLERMIN Marie", "grade": "SM", "poids": 1, "selection_count": 0},
        {"nom": "ACHOUR Badr", "grade": "M", "poids": 2, "selection_count": 0},
        {"nom": "DE OLIVEIRA Benoît", "grade": "M", "poids": 2, "selection_count": 0},
        {"nom": "FONSALE Eloïse", "grade": "SM", "poids": 1, "selection_count": 0},
        {"nom": "LUCAS Justine", "grade": "CS", "poids": 4, "selection_count": 0},
        {"nom": "BRISVILLE Thomas", "grade": "M", "poids": 4, "selection_count": 0},
        {"nom": "BOUAZIZ Jeanne", "grade": "M", "poids": 4, "selection_count": 0},
        {"nom": "MALE Martin", "grade": "CS", "poids": 4, "selection_count": 0},
        {"nom": "KARCZEWSKI Matta", "grade": "CS", "poids": 4, "selection_count": 0},
        {"nom": "CRIBIER Thibaut", "grade": "CS", "poids": 4, "selection_count": 0},
        {"nom": "BELORGEY Marie", "grade": "M", "poids": 4, "selection_count": 0},
        {"nom": "LEQUEUX Nicolas", "grade": "M", "poids": 4, "selection_count": 0},
        {"nom": "MOUMEN Assâad", "grade": "M", "poids": 4, "selection_count": 0},
        {"nom": "ROISIN Oscar", "grade": "CS", "poids": 4, "selection_count": 0},
        {"nom": "BLAIS Estelle", "grade": "M", "poids": 2, "selection_count": 0},
    ]

    conn = create_connection()
    cursor = conn.cursor()

    for emp in cdm:
        cursor.execute("""
            INSERT INTO cdm (nom, grade, poids, selection_count)
            VALUES (?, ?, ?, ?)
        """, (emp['nom'], emp['grade'], emp['poids'], emp['selection_count']))

    conn.commit()
    conn.close()

# Créer la base de données
create_table()

# Insérer les données initiales uniquement si la table est vide
if is_table_empty():
    insert_initial_data()

# Charger les données depuis la base de données
def load_data():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cdm")
    rows = cursor.fetchall()
    conn.close()
    # Retourne une liste de dictionnaires
    return [{"id": row[0], "nom": row[1], "grade": row[2], "poids": row[3], "selection_count": row[4]} for row in rows]

# Sauvegarder les données mises à jour dans la base de données
def save_data(data):
    conn = create_connection()
    cursor = conn.cursor()
    for emp in data:
        cursor.execute("""
            UPDATE cdm
            SET selection_count = ?
            WHERE id = ?
        """, (emp["selection_count"], emp["id"]))
    conn.commit()
    conn.close()

# Fonction pour sélectionner 2 cdm avec priorité aux poids plus élevés
def select_cdm(cdm):

    # Étape 1: Trouver le nombre de sélections minimum
    min_selections = min(emp["selection_count"] for emp in cdm)

    # Étape 2: Filtrer les cdm ayant le minimum de sélections
    candidates = [emp for emp in cdm if emp["selection_count"] == min_selections]

    # Étape 3: Si plus d'un candidat avec le minimum de sélections
    if len(candidates) > 1:
        # Trier les candidats par poids décroissant
        candidates.sort(key=lambda x: x["poids"], reverse=True)

        # Sélection pondérée (favorise les poids élevés)
        weights = [emp["poids"] for emp in candidates]
        selected = random.choices(candidates, weights=weights, k=2)

        # Vérifier que les deux employés sélectionnés ne sont pas les mêmes
        while selected[0] == selected[1]:
            selected = random.choices(candidates, weights=weights, k=2)

    else:
        # Si il ne reste qu'un candidat avec le moins de sélections, il est sélectionné
        selected = [candidates[0]]

        # Sélectionner un autre nom parmi ceux ayant les poids les plus élevés
        remaining_candidates = [emp for emp in cdm if emp != candidates[0]]
        remaining_candidates.sort(key=lambda x: x["poids"], reverse=True)
        second_selected = random.choice(remaining_candidates)

        selected.append(second_selected)

    # Mise à jour du compteur de sélection
    for emp in selected:
        emp["selection_count"] += 1

    # Sauvegarder les données après la sélection
    save_data(cdm)

    return selected

# Interface Streamlit
if st.button("Lancer la sélection"):
    cdm = load_data()  # Charger les données depuis la base de données
    selected_people = select_cdm(cdm)

    # Affichage des résultats
    for person in selected_people:
        st.write(f"**{person['nom']}**")


# Fonction pour réinitialiser la base de données
def reset_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cdm")
    conn.commit()
    conn.close()
    st.write("Base de données réinitialisée!")

# # Interface Streamlit
# if st.button("Réinitialiser la base de données"):
#     reset_db()

# Afficher les données de la base dans l'application Streamlit
def show_db_data():
    data = load_data()  # Charger les données depuis la base de données
    st.write("### État actuel de la base de données:")
    st.write("ID | Nom | Grade | Poids | Sélections")
    st.write("-" * 50)
    for emp in data:
        st.write(f"{emp['id']} | {emp['nom']} | {emp['grade']} | {emp['poids']} | {emp['selection_count']}")

# # Interface Streamlit
# if st.button("Afficher l'état de la base de données"):
#     show_db_data()