from flask import Flask, render_template, request, jsonify, url_for
import requests





app = Flask(__name__)
ecolabs = {

        "ecolab_2": {
            'Cellule_1': {
                "name": "E2C1",
                "fins": {
                    "ip": "192.168.0.21",
                    "port": 9600,
                    "dst_net_addr": 2,
                    "dst_node_num": 2,
                    "dst_unit_addr": 0
                },
                "params": {
                    "temperature_reprise": 10,
                    "temperature_eau_pluie": 15,
                    "temperature_consigne": 0
                }
            },
            'Cellule_2':{
                    "name": "E2C2",
                    "fins": {
                        "ip": "192.168.0.2",
                        "port": 9600,
                        "dst_net_addr": 1,
                        "dst_node_num": 1,
                        "dst_unit_addr": 0
                    },
                    "params": {
                        "temperature_reprise": 11,
                        "temperature_eau_pluie": 16,
                        "temperature_consigne": 0
                    }
            },
            'Cellule_3':{
                    "name": "E2C3",
                    "fins": {
                        "ip": "192.168.0.3",
                        "port": 9600,
                        "dst_net_addr": 1,
                        "dst_node_num": 1,
                        "dst_unit_addr": 0
                    },
                    "params": {
                        "temperature_reprise": 12,
                        "temperature_eau_pluie": 17,
                        "temperature_consigne": 0
                    }
            }
        }

    }

# country = input("lr nom de la vile :")


# try:
#
#     print(json)
#     print(json['name']['official'])
# except Exception as e:
#     print(f"Une erreur s'est produite : {e}")


@app.route('/')
def index():

     
    # try:
    #     api_lien = "http://10.119.20.100:8080/"
    #     json_data = requests.get(api_lien).json()   
    #     return render_template('index.html', info=json_data)
    # except Exception as e:
    #     print(f"Une erreur s'est produite : {e}")
    #     return "Erreur lors de la récupération des données depuis l'API."
    return render_template('index.html', info=ecolabs)

# @app.route('/pays')
# def pays():
#     api_lien = "https://restcountries.com/v3.1/all"
#     json_data = requests.get(api_lien).json()
#     return render_template('lesPays.html', info=json_data)


# @app.route('/rechercher', methods=['POST'])
# def rechercher():
#     recherche = request.form['recherchePays']
#     api_lien = f"https://restcountries.com/v3.1/name/{recherche}"
#     json_data = requests.get(api_lien).json()
#     print(json_data)
#     return render_template('rechercheParPays.html', info=json_data)

# @app.route('/rechercher/<nom>')
# def rechercherpays(nom):

#     api_lien = f"https://restcountries.com/v3.1/name/{nom}"
#     json_data = requests.get(api_lien).json()
#     print(nom)
#     print(json_data)
#     return render_template('rechercheParPays.html', info=json_data)

if __name__ == '__main__':
    app.run(host="",port=3000,debug=True)