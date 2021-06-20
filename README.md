# Test recrutement AUXILIA

## Présentation matériel de base

### But

Le code est une API très simple qui prédit la présence, ou non, d'un comportement dangereux d'une personne au volant. En plus d'identifier 
la non régularité du comportement, l'API permet de caractériser l'infraction commise. En particulier, neuf comportements interdits sont détectés par les modèles:
* utilisation de son téléphone pour envoi de texto avec main droite
* utilisation de son téléphone pour un appel avec main droite
* utilisation de son téléphone pour envoi de texto avec main gauche
* utilisation de son téléphone pour un appel avec main gauche
* manipulation de l'autoradio
* consommation de boisson ou nourriture 
* recherche d'un objet sur la banquette arrière 
* remaquillage et/ou recoiffure
* discussion avec un ou plusieurs passagers

L'API permet également de générer une carte de chaleur afin de localiser quelle partie de l'image a permis aux modèles de faire leurs prédiction.

### Installation

Requis: 
- Python v3

Etapes d'installation:
1. Créer deux dossiers heatpmap et model
2. Télécharger le modèle et le mettre dans le dossier model
3. Créer un environnement virtuel (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) et l'activer
4. Ouvrir son terminal, aller dans le dossier test_recrutement puis écrire la commande suivante `pip install -r requirements.txt`

### Fonctionnement

L'API est extrêmement, et volontairement, basique. Elle fonctionne de la manière suivante:
1. Activer son environnement virtuel `source <ENV>/bin/activate`
2. Commande: `python main.py --path=<PATH_IMAGE> --heatmap=<TRUE_OR_FALSE>` with:
  - `<PATH_IMAGE>`: le chemin d'accès à l'image à prédire
  - `<TRUE_OR_FASE>`: mettre True si vous souhaitez générer une carte de chaleur appliquée à l'image
  
En sortie l'API affiche les résultats globaux dans le terminal sous la forme d'un JSON et, potentiellement, enregistre la carte de chaleur dans le dossier 
`./heatmap`.

## Exercice

L'idée de l'exercice est de réaliser un ou plusieurs micro-services permettant d'agiliser l'envoi des images et de le rendre dynamique. Les objectifs sont les 
suivants:
* Charger une fois le modèle et pas à chaque prédiction,
* Mettre en place un système de file d'attente (en utilisant RabbitMQ par exemple) afin de traiter les images les unes après les autres dans l'ordre d'ancienneté 
de la demande
* (falcultatif) Mettre en place un service qui envoie automatiquement les fichiers présent dans un certain dossier
* Restituer la prédiction des modèles sous forme plus digeste qu'un json (par exemple sous forme d'une image)
* (facultatif) Faire une mini application qui permettrait de voir les résultats
* (facultatif) Toute optimisation de l'API est le bienvenue ! 

La durée attendue pour réaliser ce test de recrutement est de 10 jours environ et pourra aller jusqu'à 21 jours. Le code devra être accompagné d'une notice expliquant comment utiliser la solution. Par la suite, un dernier entretien sera fait au cours duquel le candidat devra expliquer son travail et justifier ses choix. 


# BON COURAGE
