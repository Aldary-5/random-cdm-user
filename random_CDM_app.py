import streamlit as st
import random
import sqlite3
import os

st.title("🎈 Binôme de CDM pour le mois")

# --- Fonctions existantes pour la gestion de la base ---

def create_connection():
    conn = sqlite3.connect('cdm.db')
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
            ordre_passage INTEGER NOT NULL DEFAULT 0,  -- Ajout de 'ordre_passage'
            squad_number INTEGER NOT NULL DEFAULT 5    -- Ajout de 'squad_number'
        )
    """)
    conn.commit()
    conn.close()

# Vérifier si la table est vide
def is_table_empty():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cdm")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

# Insérer les données initiales avec 'ordre_passage' et 'squad_number'
def insert_initial_data():
    cdm = [
        {"nom": "GUILLERMIN Marie", "grade": "SM", "poids": 1, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
        {"nom": "ACHOUR Badr", "grade": "M", "poids": 1, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
        {"nom": "DE OLIVEIRA Benoît", "grade": "M", "poids": 1, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
        {"nom": "FONSALE Eloïse", "grade": "SM", "poids": 1, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
        {"nom": "LUCAS Justine", "grade": "CS", "poids": 4, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
        {"nom": "BRISVILLE Thomas", "grade": "M", "poids": 4, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
        {"nom": "BOUAZIZ Jeanne", "grade": "M", "poids": 4, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
        {"nom": "MALE Martin", "grade": "CS", "poids": 4, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
        {"nom": "KARCZEWSKI Matta", "grade": "CS", "poids": 4, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
        {"nom": "CRIBIER Thibaut", "grade": "CS", "poids": 4, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
        {"nom": "LEQUEUX Nicolas", "grade": "M", "poids": 4, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
        {"nom": "MOUMEN Assâad", "grade": "M", "poids": 4, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
        {"nom": "ROISIN Oscar", "grade": "CS", "poids": 4, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
        {"nom": "BLAIS Estelle", "grade": "M", "poids": 1, "selection_count": 0, "ordre_passage": 0, "squad_number": 5},
    ]

    conn = create_connection()
    cursor = conn.cursor()

    for emp in cdm:
        cursor.execute("""
            INSERT INTO cdm (nom, grade, poids, selection_count, ordre_passage, squad_number)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (emp['nom'], emp['grade'], emp['poids'], emp['selection_count'], emp['ordre_passage'], emp['squad_number']))

    conn.commit()
    conn.close()

# Charger les données depuis la base de données
def load_data():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cdm")
    rows = cursor.fetchall()
    conn.close()
    
    # Retourne une liste de dictionnaires avec 'ordre_passage' et 'squad_number'
    return [
        {"id": row[0], "nom": row[1], "grade": row[2], "poids": row[3], 
         "selection_count": row[4], "ordre_passage": row[5], "squad_number": row[6]}
        for row in rows
    ]

# Créer la table et insérer les données si la table est vide
create_table()
if is_table_empty():
    insert_initial_data()

def save_data(data):
    conn = create_connection()
    cursor = conn.cursor()

    for emp in data:
        # Vérifier si le nom existe déjà dans la base de données
        cursor.execute("SELECT id FROM cdm WHERE nom = ?", (emp["nom"],))
        result = cursor.fetchone()

        if result:  # Si l'entrée existe, mise à jour
            cursor.execute("""
                UPDATE cdm
                SET selection_count = ?, ordre_passage = ?
                WHERE id = ?
            """, (emp["selection_count"], emp["ordre_passage"], result[0]))
        
        else:  # Si l'entrée n'existe pas, on insère un nouvel enregistrement
            cursor.execute("""
                INSERT INTO cdm (nom, grade, poids, selection_count, ordre_passage, squad_number)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (emp["nom"], emp["grade"], emp["poids"], emp["selection_count"], emp["ordre_passage"], emp["squad_number"]))

    conn.commit()
    conn.close()

def decaler_passage(cdm, last_cdm) :
        max_order_selected = max(emp["ordre_passage"] for emp in cdm)
    # 🔄 Réinitialiser toutes les sélections à 0
        selected_cdm = []
        last_cdm = last_cdm[0]
        selected_cdm.append(last_cdm) # On l'ajoute directement
        for emp in cdm:
            emp["selection_count"] = 0

        last_cdm["selection_count"] += 1  # On incrémente sa sélection

        # 3️⃣ Sélectionner un binôme parmi ceux ayant l'ordre de passage 1
        binome_order_1 = [emp for emp in cdm if emp["ordre_passage"] == 1]
        
        if len(binome_order_1) != 2:
            raise ValueError("Erreur : il doit y avoir exactement 2 noms avec ordre de passage = 1.")

        selected_binome_1 = random.choice(binome_order_1)
        selected_binome_1["selection_count"] += 1  # Il est sélectionné avec last_cdm
        selected_cdm.append(selected_binome_1)


        # remet le dernier nom sélectionné en 1er de la liste de sélection
        last_cdm["ordre_passage"] = 1

        # 5️⃣ Décaler progressivement les ordres de passage des binômes suivants
        binome_decale = None
        current_order = 2
        while True :
            binome_next = [emp for emp in cdm if emp["ordre_passage"] == current_order]

            if binome_decale is not None :
                non_selected_binome["ordre_passage"] += 1

            if len(binome_next) != 2:
                break  # Fin du déplacement des binômes

            selected_binome = random.choice(binome_next)
            non_selected_binome = [emp for emp in binome_next if emp != selected_binome][0]
            binome_decale = non_selected_binome

            current_order += 1
        
        # 4️⃣ L'autre membre du binôme sélectionné en premier voit son ordre de passage incrémenté
        non_selected_binome_premier = [emp for emp in binome_order_1 if emp != selected_binome_1][0]
        non_selected_binome_premier["ordre_passage"] += 1


        save_data(cdm)
        return selected_cdm

def verify_and_adjust_binomes(cdm):
    """
    Cette fonction vérifie que chaque ordre de passage (sauf le maximum) est associé à exactement 2 CDM.
    Si ce n'est pas le cas, elle décale aléatoirement des CDM vers l'ordre de passage suivant,
    de sorte que tous les ordres, sauf le dernier, aient exactement 2 entrées.
    L'ordre maximal peut rester incomplet (1 seule entrée).
    La fonction modifie directement la liste 'cdm' (les dictionnaires sont modifiés in place)
    et la retourne une fois les ajustements terminés.
    """
    max_order = max(emp["ordre_passage"] for emp in cdm)
    modification = True
    while modification:
        modification = False
        # Regrouper les CDM par ordre de passage
        groups = {}
        for emp in cdm:
            order = emp["ordre_passage"]
            groups.setdefault(order, []).append(emp)
        
        # Obtenir les ordres existants triés (les ordres non utilisés apparaîtront comme 0)
        sorted_orders = sorted(groups.keys())
        
        for order in sorted_orders :
            next_order = order + 1
            while len(groups[order]) < 2 and order < max_order : 
                next_order_bis = next_order
                # Sélectionner aléatoirement l'un des deux du groupe précédent
                chosen = random.choice(groups[next_order])
                # Retirer le CDM choisi du groupe précédent
                groups[next_order].remove(chosen)
                # Ajouter le CDM choisi au groupe courant
                groups[order].append(chosen)
                # Mettre à jour son ordre_passage
                chosen["ordre_passage"] = order
                if len(groups[next_order_bis]) == 0 :
                    next_order_bis += 1
                modification = True
            
        # Si une modification a eu lieu, la boucle se répète pour vérifier de nouveau l'ensemble
    return cdm


def select_cdm(cdm):
    
    # 🔎 Vérifier si tous les CDM ont un ordre de passage défini (> 0) et si tous les CDM sont bien par binôme (dans le cas d'une suppression)
    if all(emp["ordre_passage"] > 0 for emp in cdm) and all(emp["selection_count"] == 1 for emp in cdm):
        # 🔄 Réinitialiser toutes les sélections à 0
        max_order_selected = 0
        for emp in cdm:
            emp["selection_count"] = 0
        cdm = verify_and_adjust_binomes(cdm)
    
    if all(emp["ordre_passage"] > 0 for emp in cdm):   
        
        selected_once = [emp for emp in cdm if emp["selection_count"] == 1]

        if len(selected_once) != 0:
            # 🔝 Prendre l'ordre de passage le plus élevé parmi ceux déjà sélectionnés
            max_order_selected = max(emp["ordre_passage"] for emp in selected_once)
            next_order = max_order_selected + 1

            # 🔄 Sélectionner le binôme qui a cet ordre de passage
            selected_cdm = [emp for emp in cdm if emp["ordre_passage"] == next_order]

            # Si il n'y a qu'un seul nom pour le prochain ordre de passage
            if len(selected_cdm) == 1 : 
                if len(selected_cdm) == 1 :
                # Appel de la fonction pour décaler les binômes 
                    cdm = verify_and_adjust_binomes(cdm)
                    selected_cdm_decaler = decaler_passage(cdm, selected_cdm)
                    return selected_cdm_decaler
            
            else : 
                if len(selected_cdm) != 2:
                    raise ValueError("Erreur : il doit y avoir exactement 2 noms avec le même ordre de passage.")

                # 🔼 Incrémenter le compteur de sélection pour les deux
                for emp in selected_cdm:
                    emp["selection_count"] += 1

                # Sauvegarde des modifications
                save_data(cdm)
                return selected_cdm
        
        # si on revient au début de la liste 
        else : 
            next_order = max_order_selected + 1
            # 🔄 Sélectionner le binôme qui a cet ordre de passage
            selected_cdm = [emp for emp in cdm if emp["ordre_passage"] == next_order]
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
        # Appel de la fonction pour décaler les binômes 
        selected_cdm = decaler_passage(cdm, non_selected)
        return selected_cdm

    else:
        # 6️⃣ Sélection classique si plusieurs CDM n'ont pas encore été sélectionnés
        candidates = [emp for emp in cdm if emp["ordre_passage"] == 0]
        candidates.sort(key=lambda x: x["poids"], reverse=True)

        if len(candidates) >= 2:
            # Identifier le poids maximum parmi les candidats
            max_weight = candidates[0]["poids"]
            # Sélectionner tous les candidats ayant ce poids maximal
            top_candidates = [emp for emp in candidates if emp["poids"] == max_weight]
            
            if len(top_candidates) >= 2:
                # S'il y a au moins deux CDM avec le poids maximal, on en choisit aléatoirement deux
                selected_cdm = random.sample(top_candidates, 2)
            elif len(top_candidates) == 1:
                # Sinon, on conserve le CDM avec le poids maximal et on choisit un autre parmi le reste
                first = top_candidates[0]
                remaining = [emp for emp in candidates if emp != first]
                second = random.choice(remaining)
                selected_cdm = [first, second]
            else : 
                remaining = [emp for emp in candidates if emp != first]
                selected_cdm = random.sample(remaining, 2)

            # Déterminer le prochain numéro d'ordre de passage
            max_order = max(emp["ordre_passage"] for emp in cdm) if cdm else 0
            new_order = max_order + 1

            # Appliquer le même ordre de passage aux 2 CDM sélectionnés et incrémenter leur compteur
            for emp in selected_cdm:
                emp["ordre_passage"] = new_order
                emp["selection_count"] += 1
        else:
            selected_cdm = []

    # 7️⃣ Sauvegarder les données mises à jour
    save_data(cdm)

    return selected_cdm

# Fonction pour ajouter un nouveau CDM
def add_new_cdm(new_name, new_grade):
    cdm = load_data()
    new_cdm = {}
    new_cdm["nom"] = new_name
    new_cdm["grade"] = new_grade
    new_cdm["poids"] = 4
    new_cdm["squad_number"] = 5
    # Vérifier si tout le monde a un ordre de passage > 0
    all_have_order = all(emp["ordre_passage"] > 0 for emp in cdm)

    if all_have_order:
        # Trouver l'ordre de passage le plus élevé parmi ceux qui ont une sélection = 1
        max_order_selected = max(emp["ordre_passage"] for emp in cdm if emp["selection_count"] == 1)
        next_order = max_order_selected + 1  # Prochain ordre de passage

        # Sélectionner un binôme ayant déjà cet ordre de passage pour sauvegarder les noms
        binome = [emp for emp in cdm if emp["ordre_passage"] == next_order ]


        # 🔄 Décaler tous les binômes suivants de la même façon
        binome_decale = None
        current_order = next_order + 1
        while True:
            binome_next = [emp for emp in cdm if emp["ordre_passage"] == current_order]

            if binome_decale is not None :
                binome_decale["ordre_passage"] += 1

            if len(binome_next) != 2:
                break  # Fin du décalage

            selected_binome = random.choice(binome_next)
            non_selected_binome = [emp for emp in binome_next if emp != selected_binome][0]
            binome_decale = non_selected_binome

            current_order += 1

        # Sélectionne aléatoirement 1 nom dans le binôme qui porte le même ordre de passage que le nouveau cdm et décale son ordre de passage
        if len(binome) != 2:
            raise ValueError("Erreur : il doit y avoir exactement 2 CDM avec le même ordre de passage.")

        # Sélectionner un des deux membres du binôme de façon aléatoire
        selected_binome = random.choice(binome)
        non_selected_binome = [emp for emp in binome if emp != selected_binome][0]

        # L'un garde le même ordre, l'autre est décalé de +1
        non_selected_binome["ordre_passage"] += 1

        # Attribue le prochain numéro pour passer au nouveau CDM
        new_cdm["ordre_passage"] = next_order
        new_cdm["selection_count"] = 0

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

# --- Interface pour la sélection habituelle ---

# Optionnel : Bouton pour afficher l'état de la base
def show_db_data():
    data = load_data()
    st.write("### État actuel de la base de données:")
    st.write("ID | Nom | Grade | Poids | Squad | Sélections | Ordre de passage")
    st.write("-" * 50)
    for emp in data:
        st.write(f"{emp['id']} | {emp['nom']} | {emp['grade']} | {emp['poids']} | {emp['squad_number']} | {emp['selection_count']} | {emp['ordre_passage']}")

# Réinitialiser la base de données
def reset_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE cdm SET selection_count = 0, ordre_passage = 0")
    conn.commit()
    conn.close()
    st.success("Base de données réinitialisée avec succès !")


with col1:
    if st.button("Lancer la sélection"):
        cdm_data = load_data()
        selected_people = select_cdm(cdm_data)
        for person in selected_people:
            st.write(f"**{person['nom']}")
    # if st.button("Afficher l'état de la base de données"):
    #     show_db_data()
    # # Bouton pour réinitialiser la base de données
    # if st.button("🔄 Réinitialiser la base de données"):
    #     reset_db()

# Fonction pour supprimer un CDM
def delete_cdm_by_name(cdm, nom):
    conn = create_connection()  # Assure-toi que create_connection() est défini et fonctionne
    cursor = conn.cursor()

    # Récupérer l'ordre de passage du CDM correspondant au nom
    cursor.execute("SELECT ordre_passage, selection_count FROM cdm WHERE nom = ?", (nom,))
    odp = cursor.fetchone()
    
    if odp is None:
        print(f"Aucun CDM avec le nom {nom} n'a été trouvé.")
        conn.close()
        return None
    
    ordre_passage = odp[0]
    selection = odp[1]
    binome_decale = None

    if selection == 0 and ordre_passage != 0 : 

        while ordre_passage <= max(emp["ordre_passage"] for emp in cdm):
                binome_next = [emp for emp in cdm if emp["ordre_passage"] == ordre_passage + 1]

                if binome_decale is not None :
                    binome_decale["ordre_passage"] -= 1

                if len(binome_next) != 2:
                    break  # Fin du décalage

                selected_binome = random.choice(binome_next)
                non_selected_binome = [emp for emp in binome_next if emp != selected_binome][0]
                binome_decale = non_selected_binome

                ordre_passage += 1
    
    save_data(cdm)

    cursor.execute("DELETE FROM cdm WHERE nom = ?", (nom,))
    conn.commit()
    conn.close()
    print(f"{nom} a été supprimée de la liste des CDM.")

# --- Bouton pour afficher/masquer le formulaire d'ajout d'un cdm ---
with col2:
    if "show_add_form" not in st.session_state:
        st.session_state.show_add_form = False

    if st.button("Ajouter un CDM"):
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
                ordre_passage = next((emp["ordre_passage"] for emp in new_emp if emp["nom"] == name_input), "inconnu")
                st.success(f"CDM {name_input} ajouté")
                # Une fois l'ajout effectué, on peut masquer le formulaire
                st.session_state.show_add_form = False
            else:
                st.error("Veuillez remplir tous les champs.")
    
    # Bouton pour supprimer un CDM
    if "show_add_form_suppr" not in st.session_state:
        st.session_state.show_add_form_suppr = False

    if st.button("Supprimer un CDM"):
        # Inverse l'état du formulaire (affiche s'il est masqué, le masque s'il est affiché)
        st.session_state.show_add_form_suppr = not st.session_state.show_add_form_suppr

    # Afficher le formulaire uniquement si show_add_form_suppr est True
    if st.session_state.show_add_form_suppr:
        # Message d'avertissement en rouge avec une icône warning
        st.markdown(
            "<span style='color: red; font-weight: bold;'>⚠️ Attention : la suppression bousculera tout l'ordre, soyez sûr avant de cliquer !</span>",
            unsafe_allow_html=True,
        )
        # Charger les données pour extraire les noms
        cdm_data = load_data()
        names = [emp["nom"] for emp in cdm_data]
        
        with st.form(key="add_employee_form_suppr"):
            # Utiliser une liste déroulante pour sélectionner le nom
            name_input = st.selectbox("Nom du CDM", options=names)
            submit_button = st.form_submit_button(label="Supprimer le CDM")
        
        if submit_button:
            if name_input:
                delete_cdm_by_name(cdm_data, name_input)
                st.success(f"{name_input} a été supprimé(e) de la liste des CDM")
                # Une fois la suppression effectuée, on peut masquer le formulaire
                st.session_state.show_add_form_suppr = False
            else:
                st.error("Veuillez sélectionner un CDM.")


