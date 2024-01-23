'''
Flask : pip install SQLAlchemy

'''

############################################################################################################

# Importation des modules nécessaires
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from Connexion import utilisateur,session, password, base_de_donne, port, Base
from Historique import HistoriqueCellule
from Experience import Experience
from Cellule import Cellule
from User import Utilisateur
from werkzeug.security import check_password_hash

############################################################################################################

# Auteur: Deva

class OctopusDB:
    def __init__(self):
        self.experiences = session.query(Experience).all()
        self.cellules = session.query(Cellule).all()
        self.historique = session.query(HistoriqueCellule).all()
        self.users = session.query(Utilisateur).all()


    # Method to retrieve all experiments from database
    def get_all_experience(self):
        global session
        experiences = session.query(Experience).all()
        session.commit()
        return experiences


    # Method to retrieve the name of a cell from its ID
    def get_cellule_name_from_id(self, id_cellule):
        for cellule in self.cellules:
            if cellule.id == id_cellule:
                return cellule.nom

    # Method to retrieve a cell from its name
    def get_cellule_by_name(self,name):
        for cellule in self.cellules:
            if cellule.nom == name:
                return cellule
        return None

    # Method to retrieve a cell from its ID
    def get_cellule_by_id(self,id_cellule):
        for cellule in self.cellules:
            if cellule.id == id_cellule:
                return cellule

    # Method for retrieving current and future experiences
    def get_futur_and_current_experience(self):
        result = []
        for experience in self.experiences:
            if experience.etat_experience == "à venir" or experience.etat_experience == "En cours":
                result.append(experience)
        return result

    # Method to retrieve an experience from its ID
    def get_experience_by_id(self,id_experience):
        try :
            for experience in self.experiences:
                if experience.id == id_experience:
                    return experience
        except Exception as e:
            print(f"Erreur lors de la récupération de l'expérience par ID : {str(e)}")
            return None


    # Method to retrieve the history of a cell from its ID
    def get_historique_by_id(self,cellule_id):
        global session
        historiques = session.query(HistoriqueCellule).all()
        result = []
        for historique in historiques:
            if historique.cellule_id == cellule_id:

                cellule = self.get_cellule_by_id(historique.cellule_id)
                experience = self.get_experience_by_id(historique.cellule_experience_id)
                result.append({"historique": historique, "cellule": cellule, "experience": experience})
        session.commit()
        return result

    # Method to retrieve the experience of a cell from its ID
    def get_experience_of_cellule(self,cellule_id):
        for cellule in self.cellules:
            if cellule.id == cellule_id:
                return self.get_experience_by_id(cellule.experience_id)
        return None

 # Method to retrieve an experience from its ID
    def get_experience_by_id(self,id):
        for experience in self.experiences:
            if experience.id == id :
                return experience
        return None

    # Method for updating a cell's experience
    def new_experience_of_cellule(self,id_cellule,id_experience):
        global session
        try :
            cellule = self.get_cellule_by_id(id_cellule)
            cellule.experience_id = id_experience
            session.commit()
            return "Mise à jour réussie"
        except Exception as e:
            return f"Une erreur s'est produite : {str(e)}"

    # Method to update the history of a cell
    def new_historique(self,id_cellule,id_experience):
        global session
        try:
            new_historique = HistoriqueCellule(cellule_id=id_cellule,cellule_experience_id=id_experience,status="En cours",action="Ajout d'une nouvelle expérience à la cellule")
            session.add(new_historique)
            session.commit()
            return "c'est bon"
        except Exception as e:
            return f"Une erreur s'est produite : {str(e)}"

    # Method to update the history of a cell
    def update_historique(self,cellule_id):
        global session
        historiques = session.query(HistoriqueCellule).all()
        try :
            for historique in historiques:
                if historique.cellule_id == cellule_id and historique.status == "En cours":
                    historique.status = "Terminés"
                    session.commit()
            return "mise a jour reussi !"
        except Exception as e:
            return f"Une erreur s'est produite : {str(e)}"
        
    # Auteur Luca
    
    # Existant
    def user_exists(cls,login,password):
        global session
        users = session.query(Utilisateur).all()
        try:
            for user in users:
                if login == user.username:
                    if user.check_password(password):
                        return True
                    else:
                        return 'mot de passe incorrecte'
                    
            return 'Utilisateur inexistant'

        except Exception as e:
            return f"une erreur s'est produite : {str(e)}"
        

    # method to find out if user exists and get their role
    def get_role_by_user(cls,username):
        global session
        users = session.query(Utilisateur).all()
        try:
            for user in users:
                if username == user.username:
                        return user.role
            
            return 'utilisateur inexistant'
        except Exception as e:
            return f"une erreur s'est produite : {str(e)}"
            


# name = 'admin'
# pwd = 'UtilisateurAdmin'



# Affichage du résultat


octopus = OctopusDB()
# resultat = octopus.user_existant(name, pwd)

# print(resultat)




