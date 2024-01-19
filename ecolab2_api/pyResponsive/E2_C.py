'''

pip install flask
pip install json
pip instal requests
pip install Flask-SQLAlchemy

'''

############################################################################################################

from flask import Flask, render_template, request, jsonify, url_for, redirect
import json
import requests
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from Connexion import utilisateur,session, password, base_de_donne, port, Base, DB_URL
from Historique import HistoriqueCellule
from Experience import Experience
from Cellule import Cellule
from User import Utilisateur
from OctopusDB import octopus

############################################################################################################

# App setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{utilisateur}:{password}@localhost:{port}/{base_de_donne}'

############################################################################################################

# Recovery of configuration informations
with open('/home/luca/Bureau/ecolab/Ecolabs_test/ecolab2_api/pyResponsive/config.json', 'r') as config:
    config = json.load(config)
    ip = config['IP']
    port = config['Port']
    debug = config['Debug']

############################################################################################################
# Auteur Luca et Deva

# Basic role 
role = "visiteur"

# Web pages

# Connection
@app.route('/connexion')
def forms():
    return render_template('connection.html',ip=ip, port=port)

# Index
@app.route('/')
def index():
    global role
    try:
        # Retrieving data in Json Ecolab 2
        ecolab2 = "http://10.119.20.100:8080/"
        json_data2 = requests.get(ecolab2).json()

        # Retrieving data in Json Ecolab 4
        ecolab4 = "http://10.119.40.100:8080/"
        json_data4 = requests.get(ecolab4).json()
       
        return render_template('index.html', role= role, info2=json_data2, info4=json_data4)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return "Erreur lors de la récupération des données depuis l'API."
    
    
# Détails
@app.route('/detail',methods=['POST'])
def detail():
    global session
    try:
        #I collect the name of the cell that the client clicked using the POST method.
        cellule_name =request.form.get('name')
        #cellule_name = "E2C3"

        #I'm trying to get the Ecolab and Cell numbers by their names
        ecolab = cellule_name[1]
        cell =  cellule_name[3]

        #Collection of parameters of cells
        # Ip according to ecolab
        data = requests.get(f'http://10.119.{ecolab}0.100:8080/')
        parameters = data.json()

        #I utilize the collected numbers to create patterns such as 'ecolab_(number of ecolab)' 
        #and 'Cellule_(number of cellule)
        jsonEcolab = f"ecolab_{ecolab}"
        jsonCellule = f"Cellule_{cell}"

        #Obtaining the Cellule object using its name
        cellule = octopus.get_cellule_by_name(cellule_name)
        
        #Obtaining the Experience object using its ID
        experienceInProgress = cellule.experience_id

        #Obtaining a list of all historique of cellule using its ID
        historique = octopus.get_historique_by_id(cellule.id)

        #Obtaining a list of all experience with satus "a venir" are "en cours"
        future_and_current_experiences = octopus.get_futur_and_current_experience()
        session.commit()

        return render_template('detail.html',experience_avenir_encours = future_and_current_experiences ,nom_cellule=cellule_name, 
                           cellule = cellule, experience=experienceInProgress,info = parameters, historique= historique, jsonEcolab = jsonEcolab, jsonCellule=jsonCellule )
    except requests.exceptions.RequestException as e:
        return render_template('error.html', error_message=str(e))
    
# Experiences
@app.route('/experiences')
def experiences():
    global session
    #Obtaining all experiences existing in the database
    experiences = octopus.get_all_experience()
    session.commit()
    return render_template('experience.html',experiences=experiences)

# Add experience
@app.route('/add-experiences')
def addExperience():
    return render_template('addExperience.html')

# Edit experience
@app.route('/edit-experiences',methods=['POST'])
def editExperiences():
    id_experience = int(request.form.get('id_experience'))

    #Obtaining the object of experience using its ID
    experience = octopus.get_experience_by_id(id_experience)
    #print(experience)
    return render_template('editExperience.html',experience=experience)

############################################################################################################
# Action Methods 

# Disconnection
@app.route('/deconnexion')
def deconnexion():
    global role
    role='visiteur'
    return redirect(url_for('index'))

# Connection processing
@app.route('/traitement', methods=['POST'])
def traitement():
    global role

    login = request.form.get('login')
    mdp = request.form.get('password')

    role = octopus.get_role_by_user(login, mdp)

    # Admin template
    if role == 'admin':
        try:
            # Retrieving data in Json Ecolab 2
            ecolab2 = "http://10.119.20.100:8080/"
            json_data2 = requests.get(ecolab2).json()

            # Retrieving data in Json Ecolab 4
            ecolab4 = "http://10.119.40.100:8080/"
            json_data4 = requests.get(ecolab4).json()

            return render_template('adminTemplate.html', role= role, info2=json_data2, info4=json_data4)
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
        return "Erreur lors de la récupération des données depuis l'API."
    

    elif role == 'normal':
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

# Add experience passed
@app.route('/new-experience-in-cellule', methods=['POST'])
def new_experience_in_cellule():
    global session
    try: 
        #Obtaining ID of experience using method POST
        experience_id= int(request.form.get('experience')) 

         #Obtaining ID of cellule using method POST
        cellule_id = int(request.form.get('cellule'))

         #Obtaining name of cell 
        cellule_name = octopus.get_cellule_name_from_id(cellule_id)

         #Obtaining the experiens in Progress
        experienceInProgress = request.form.get('experienceEnCours')#int()

        #update column status of historique using cell ID
        update_historique = octopus.update_historique(cellule_id)

        update_cellule = octopus.new_experience_of_cellule(cellule_id,experience_id)
        add_historique = octopus.new_historique(cellule_id,experience_id)

        session.commit()
        return render_template('successAddExperienceInCellule.html',cellule = cellule_name)
    
    except requests.exceptions.RequestException as e:
        return render_template('error.html', error_message=str(e))

# Add experience 
@app.route('/process-add-experiences',methods=['POST'])
def processToAddExperience():
    global session
    #Obtaining the new datas of experience for creat an object 
    name = request.form.get('nom')
    starting_date = request.form.get('date_debut')
    finishing_date = request.form.get('date_fin')
    status = request.form.get('etat_experience')
    newExperience = Experience(nom=name,date_debut=starting_date,date_fin=finishing_date,etat_experience=status)
    session.add(newExperience)
    session.commit()
    return redirect(url_for('experiences'))

# Edit experience
@app.route('/process-edit-experiences',methods=['POST'])
def processToEditExperiences():
    global session
    #Obtaining the new datas of experience for edit the object 
    id_experience = int(request.form.get('id_experience'))
    nom = request.form.get('nom')
    date_debut = request.form.get('date_debut')
    date_fin = request.form.get('date_fin')
    etat = request.form.get('etat_experience')

    #Obtaining the relevant object in the database
    experience = octopus.get_experience_by_id(id_experience)

    #edit the datas
    experience.nom=nom
    if date_debut:
        experience.date_debut = date_debut
    if date_fin:
        experience.date_fin = date_fin
    experience.etat_experience = etat   
    session.commit()
    return redirect(url_for('experiences'))

# Start Flask server
if __name__ == '__main__':
    app.run(host=ip,port=5500,debug=debug)