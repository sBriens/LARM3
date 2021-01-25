# LARM3
# LARM3

#Challenge 1
Pour mettre en place l'environnement, il faut :
* Charger la simulation : roslaunch larm challenge-1.launch
* Lancer l'architecture de contrôle : roslaunch student_pkg navigation.launch
* Lancer rviz
* Donner une estimation de la pose avec rviz
Il est maintenant possible de donner des destinations dans le topic /goal

#Challenge 2
Les étapes pour lancer la simulation sont les suivantes:
* Ouvrir un terminal, executer la commande suivante : roslaunch larm challenge-2.launch
* Ouvrir un autre terminal, executer la commande suivante : roslaunch challenge_2 mapping.launch
Ce fichier de lancement contient le nœud slam_gmapping qui aidera à construire la carte lorsque le turtlebot se déplace. Aussi, rviz doit être lancé pour voir la construction de la carte lors des déplacements du robot.
Le fichier de lancement contient également l'algorithme de détection, cet algorithme affichera qu'une canette est détectée ou non, ou éventuellement. Il affichera également la vue de la caméra du turtlebot et les algorithmes feature_matching appliqués à la caméra rgb du turtlebot (ces vues peuvent être accédées via les outils graphiques).
* Ce nœud publiera dans la rubrique /bottle la distance entre le centre du robot et la canette détectée. La commande est la suivante: écho rostopique /bottle

#Challenge 3
Les étapes pour lancer la simulation sont les suivantes:
* Compiler le package rrt_exploration dans un premier terminal : catkin_make ; source /devel/setup.bash
* Ouvrir un autre terminal
* Charger la simulation du challenge 3 dans le 2nd terminal : roslaunch larm challenge-3.launch
* Lancer le launch file du challenge, dans le premier terminal : roslaunch challenge_3 exploration.launch
* Lancer Rviz
* Créer un polygone à l'aide de l'outils "Publish Point"
* Selection un point de départ à l'aide du même outils, une fois le polygone définie.

Le robot va parcourir la map en autonomie. On peut suivre la progression dans Rviz.
* Ouvrir un nouveau terminal
* Lancer la commande suivante pour suivre la détection des cannettes : rostopic echo /bottle (le taux de faux positif est élevé)