# epidemy-simulation
made for a school project. not meant to be good.

conventions:
-liste de règles R = {
  "nb_voisins": nombre de voisins contaminé minimum requis pour contamination garantie,
  "recup_min": nombre de temps minimum requis avant de ne plus etre contaminé,
  "recup_max": nombre de temps maximum requis avant de ne plus etre contaminé,
  "proba_mort": probabilité de mourir chaque jour pour une personne contaminée,
  "proba_oubli": probabilité de redevenir susceptible à l'infection chaque jour pour une personne soignée
  }

-état de chaque case:
  "S": susceptible à la contamination, safe,
  "R": récupéré, soigné, plus contaminé,
  "M": mort,
  "I": qui vient d'être infecté, ne pouvant donc pas infecter les autres, et qui deviendra contagieux le jour suivant
  x = infecté, avec x le nombre de jours restants avant la récupération
  
