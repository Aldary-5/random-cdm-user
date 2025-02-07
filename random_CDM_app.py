import streamlit as st
import random
import sqlite3
import os

st.title("🎈 Binôme de CDM pour le mois")

# --- Fonctions existantes pour la gestion de la base ---

def create_connection():
    db_path = os.path.join(os.getcwd(), 'cdm_selections.db')
    conn = sqlite3.connect(db_path)
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cdm (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            grade TEXT NOT NULL,
            poids INTEGER NOT NULL,
            selection_count INTEGER NOT NULL DEFAULT 0,
            ordre_passage INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def is_table_empty():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cdm")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def insert_initial_data():
    cdm_data = [
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
    for emp in cdm_data:
        cursor.execute("""
            INSERT INTO cdm (nom, grade, poids, selection_count, ordre_passage)
            VALUES (?, ?, ?, ?, ?)
        """, (emp['nom'], emp['grade'], emp['poids'], emp['selection_count'], 0))
    conn.commit()
    conn.close()

def load_data():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cdm")
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": row[0], "nom": row[1], "grade": row[2], "poids": row[3],
         "selection_count": row[4], "ordre_passage": row[5]}
        for row in rows
    ]

def save_data(data):
    conn = create_connection()
    cursor = conn.cursor()
    for emp in data:
        cursor.execute("""
            UPDATE cdm
            SET selection_count = ?, ordre_passage = ?
            WHERE id = ?
        """, (emp["selection_count"], emp["ordre_passage"], emp["id"]))
    conn.commit()
    conn.close()

# --- Fonction de sélection existante (déjà modifiée précédemment) ---
# def select_cdm(cdm):
#     # Étape 1: Vérifier si tout le monde a un ordre de passage défini (différent de 0)
#     all_have_order = all(emp["ordre_passage"] != 0 for emp in cdm)

#     if all_have_order:
#         # Si tout le monde a un ordre de passage, on suit l'ordre de passage existant
#         cdm.sort(key=lambda x: x["ordre_passage"])  # Trier par ordre de passage
#         selected = [cdm[0], cdm[1]]  # Sélectionner les 2 premiers par ordre de passage
#         selected[0]["ordre_passage"] = selected[1]["ordre_passage"] = selected[0]["ordre_passage"] or 1  # Attribuer le même ordre de passage

#         # Décaler les autres ordres de passage, mais **ne pas affecter** ceux déjà attribués
#         for i in range(2, len(cdm)):
#             if cdm[i]["ordre_passage"] == 0:  # Ne pas affecter les CDM déjà assignés
#                 cdm[i]["ordre_passage"] = i + 1

#     else:
#         # Si tout le monde n'a pas un ordre de passage, on sélectionne parmi ceux non sélectionnés
#         non_selected = [emp for emp in cdm if emp["selection_count"] == 0]
#         non_selected.sort(key=lambda x: (-x["poids"], x["nom"]))  # Prioriser par poids décroissant et nom

#         # Si la liste est impaire, on fait un traitement spécial
#         if len(non_selected) % 2 == 1:
#             # Si un seul reste parmi ceux non sélectionnés, on sélectionne aléatoirement parmi les 2 noms ayant l'ordre de passage 1
#             selected = non_selected[:2]  # Sélectionner les 2 premiers

#             # Attribuer le même ordre de passage pour ces 2 CDM
#             selected[0]["ordre_passage"] = selected[1]["ordre_passage"] = 1

#             # Décaler un des 2 noms du binôme sélectionné de manière aléatoire
#             remaining = [emp for emp in cdm if emp["ordre_passage"] == 1]
#             selected_emp = random.choice(remaining)

#             # Décaler un nom au hasard parmi ceux ayant l'ordre 1
#             for emp in cdm:
#                 if emp["ordre_passage"] == 1 and emp != selected_emp:
#                     emp["ordre_passage"] += 1

#             # Maintenant, on s'assure que tous les autres ont leur ordre de passage mis à jour
#             for i in range(2, len(cdm)):
#                 if cdm[i]["ordre_passage"] == 0:  # Ne pas affecter les CDM déjà assignés
#                     cdm[i]["ordre_passage"] = i + 1

#         else:
#             # Liste paire : sélection classique parmi les non sélectionnés
#             selected = non_selected[:2]
#             next_order = max(emp["ordre_passage"] for emp in cdm) + 1 if cdm else 1  # Dernier ordre de passage + 1 ou 1 si vide

#             selected[0]["ordre_passage"] = selected[1]["ordre_passage"] = next_order

#             # Décaler les autres ordres de passage
#             for i in range(2, len(cdm)):
#                 if cdm[i]["ordre_passage"] == 0:  # Ne pas affecter les CDM déjà assignés
#                     cdm[i]["ordre_passage"] = i + 1

#     # Incrémenter le compteur de sélection pour les CDM sélectionnés
#     for emp in selected:
#         emp["selection_count"] += 1

#     # Sauvegarder les données dans la base après sélection
#     save_data(cdm)

#     return selected

def select_cdm(cdm):
    # 🔎 Vérifier si tous les CDM ont un ordre de passage défini (> 0)
    if all(emp["ordre_passage"] > 0 for emp in cdm):
        # 🔍 Chercher les binômes ayant un nombre de sélection = 1
        selected_once = [emp for emp in cdm if emp["selection_count"] == 1]

        if selected_once:
            # 🔝 Prendre l'ordre de passage le plus élevé parmi ceux déjà sélectionnés
            max_order_selected = max(emp["ordre_passage"] for emp in selected_once)
            next_order = max_order_selected + 1

            # 🔄 Sélectionner le binôme qui a cet ordre de passage
            selected_cdm = [emp for emp in cdm if emp["ordre_passage"] == next_order]

            if len(selected_cdm) != 2:
                raise ValueError("Erreur : il doit y avoir exactement 2 noms avec le même ordre de passage.")

            # 🔼 Incrémenter le compteur de sélection pour les deux
            for emp in selected_cdm:
                emp["selection_count"] += 1

            # Sauvegarde des modifications
            save_data(cdm)
            return selected_cdm

    # 1️⃣ Trouver les CDM qui n'ont pas encore été sélectionnés
    non_selected = [emp for emp in cdm if emp["selection_count"] == 0]

    # 2️⃣ Cas particulier : il ne reste qu'un seul CDM non sélectionné
    if len(non_selected) == 1:
        # 🔄 Réinitialiser toutes les sélections à 0
        for emp in cdm:
            emp["selection_count"] = 0

        last_cdm = non_selected[0]
        last_cdm["selection_count"] += 1  # On l'ajoute directement
        selected_cdm = [last_cdm]

        # 3️⃣ Sélectionner un binôme parmi ceux ayant l'ordre de passage 1
        binome_order_1 = [emp for emp in cdm if emp["ordre_passage"] == 1]
        
        if len(binome_order_1) != 2:
            raise ValueError("Erreur : il doit y avoir exactement 2 noms avec ordre de passage = 1.")

        selected_binome = random.choice(binome_order_1)
        selected_binome["selection_count"] += 1  # Il est sélectionné avec last_cdm
        selected_binome["ordre_passage"] = 1  # Son ordre reste 1
        selected_cdm.append(selected_binome)

        # 4️⃣ L'autre membre du binôme voit son ordre de passage incrémenté
        non_selected_binome = [emp for emp in binome_order_1 if emp != selected_binome][0]
        non_selected_binome["ordre_passage"] += 1

        # remet le dernier nom sélectionné en 1er de la liste de sélection
        last_cdm["ordre_passage"] = 1

        # 5️⃣ Décaler progressivement les ordres de passage des binômes suivants
        current_order = 2
        while True:
            binome_next = [emp for emp in cdm if emp["ordre_passage"] == current_order]

            if len(binome_next) != 2:
                break  # Fin du déplacement des binômes

            selected_binome = random.choice(binome_next)
            non_selected_binome = [emp for emp in binome_next if emp != selected_binome][0]

            non_selected_binome["ordre_passage"] += 1
            current_order += 1

    else:
        # 6️⃣ Sélection classique si plusieurs CDM n'ont pas encore été sélectionnés
        candidates = [emp for emp in cdm if emp["ordre_passage"] == 0]
        candidates.sort(key=lambda x: x["poids"], reverse=True)

        if len(candidates) >= 2:
            selected_cdm = random.sample(candidates, 2)
            max_order = max(emp["ordre_passage"] for emp in cdm) if cdm else 0
            new_order = max_order + 1

            for emp in selected_cdm:
                emp["ordre_passage"] = new_order
                emp["selection_count"] += 1

        else:
            selected_cdm = []

    # 7️⃣ Sauvegarder les données mises à jour
    save_data(cdm)

    return selected_cdm

# Fonction pour ajouter un nouveau CDM
def add_new_cdm(cdm, new_cdm):
    # Vérifier si tout le monde a un ordre de passage > 0
    all_have_order = all(emp["ordre_passage"] > 0 for emp in cdm)

    if all_have_order:
        # Trouver l'ordre de passage le plus élevé parmi ceux qui ont une sélection = 1
        max_order_selected = max(emp["ordre_passage"] for emp in cdm if emp["selection_count"] == 1)
        next_order = max_order_selected + 1  # Prochain ordre de passage
        new_cdm["ordre_passage"] = next_order
        new_cdm["selection_count"] = 0

        # Sélectionner un binôme ayant déjà cet ordre de passage
        binome = [emp for emp in cdm if emp["ordre_passage"] == next_order - 1]

        if len(binome) != 2:
            raise ValueError("Erreur : il doit y avoir exactement 2 CDM avec le même ordre de passage.")

        # Sélectionner un des deux membres du binôme de façon aléatoire
        selected_binome = random.choice(binome)
        non_selected_binome = [emp for emp in binome if emp != selected_binome][0]

        # L'un garde le même ordre, l'autre est décalé de +1
        non_selected_binome["ordre_passage"] += 1

        # 🔄 Décaler tous les binômes suivants de la même façon
        current_order = next_order
        while True:
            binome_next = [emp for emp in cdm if emp["ordre_passage"] == current_order]

            if len(binome_next) != 2:
                break  # Fin du décalage

            selected_binome = random.choice(binome_next)
            non_selected_binome = [emp for emp in binome_next if emp != selected_binome][0]

            non_selected_binome["ordre_passage"] += 1
            current_order += 1

    else:
        # Si d'autres CDM n'ont pas encore d'ordre de passage, le nouveau est ajouté normalement
        new_cdm["selection_count"] = 0
        new_cdm["ordre_passage"] = 0

    # Ajouter le nouveau CDM à la liste
    cdm.append(new_cdm)
    
    # Sauvegarder la base de données
    save_data(cdm)
    
    return cdm


# --- Interface Streamlit pour ajouter un cdm ---

col1, col2 = st.columns(2)

# --- Bouton pour afficher/masquer le formulaire d'ajout d'un cdm ---
with col2:
    if "show_add_form" not in st.session_state:
        st.session_state.show_add_form = False

    if st.button("Ajouter un cdm"):
        # Inverse l'état du formulaire (affiche s'il est masqué, le masque s'il est affiché)
        st.session_state.show_add_form = not st.session_state.show_add_form

    # Afficher le formulaire uniquement si show_add_form est True
    if st.session_state.show_add_form:
        # Message d'avertissement en rouge avec une icône warning
        st.markdown(
            "<span style='color: red; font-weight: bold;'>⚠️ Attention : l'ajout bousculera tout l'ordre, soyez sûr avant de cliquer !</span>",
            unsafe_allow_html=True,
        )
        with st.form(key="add_employee_form"):
            name_input = st.text_input("Nom du CDM")
            grade_input = st.text_input("Grade du CDM")
            submit_button = st.form_submit_button(label="Ajouter le CDM")
        if submit_button:
            if name_input and grade_input:
                new_emp = add_new_cdm(name_input, grade_input)
                st.success(f"Employé {new_emp['nom']} ajouté avec ordre de passage {new_emp['ordre_passage']}")
                # Une fois l'ajout effectué, on peut masquer le formulaire
                st.session_state.show_add_form = False
            else:
                st.error("Veuillez remplir tous les champs.")



# Optionnel : Bouton pour afficher l'état de la base
def show_db_data():
    data = load_data()
    st.write("### État actuel de la base de données:")
    st.write("ID | Nom | Grade | Poids | Sélections | Ordre de passage")
    st.write("-" * 50)
    for emp in data:
        st.write(f"{emp['id']} | {emp['nom']} | {emp['grade']} | {emp['poids']} | {emp['selection_count']} | {emp['ordre_passage']}")

# Réinitialiser la base de données
def reset_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE cdm SET selection_count = 0, ordre_passage = 0")
    conn.commit()
    conn.close()
    st.success("Base de données réinitialisée avec succès !")


# --- Interface pour la sélection habituelle ---
with col1:
    if st.button("Lancer la sélection"):
        cdm_data = load_data()
        selected_people = select_cdm(cdm_data)
        for person in selected_people:
            st.write(f"**{person['nom']}** (Ordre de passage: {person['ordre_passage']})")
    if st.button("Afficher l'état de la base de données"):
        show_db_data()
    # Bouton pour réinitialiser la base de données
    if st.button("🔄 Réinitialiser la base de données"):
        reset_db()
