# epidemy-simulation
made for a school project. not meant to be good.

conventions:
-liste de règles R = {
  "nb_voisins": nombre de voisins contaminé minimum requis pour contamination garantie,
  "tps_min": nombre de temps minimum requis avant de ne plus etre contaminé,
  "tps_max": nombre de temps maximum requis avant de ne plus etre contaminé,
  "proba_mort": probabilité de mourir chaque jour pour une personne contaminée
  }

-état de chaque case:
  "S": susceptible à la contamination, safe,
  "R": récupéré, soigné, plus contaminé,
  "M": mort,
  x = infecté, avec x le nombre de jours restants avant la récupération
  
