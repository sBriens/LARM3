# LARM3
# LARM3

#Challenge 1
Pour mettre en place l'environnement, il faut :
    - Charger la simulation
     roslaunch larm challenge-1.launch
    - Lancer l'architecture de contrôle    roslaunch student_pkg navigation.launch
    - Lancer rviz
    - Donner une estimation de la pose avec rviz
Il est maintenant possible de donner des destinations dans le topic /goal


#Challenge 3
Les étapes pour lancer la simulation sont les suivantes:
    -Compiler le package rrt_exploration dans un premier terminal : catkin_make ; source /devel/setup.bash
    -Ouvrir un autre terminal
    -Charger la simulation du challenge 3 dans le 2nd terminal : roslaunch larm challenge-3.launch
    -Lancer le launch file du challenge, dans le premier terminal : roslaunch challenge_3 exploration.launch
    -Lancer Rviz
    -Créer un polygone à l'aide de l'outils "Publish Point"
    -Selection un point de départ à l'aide du même outils, une fois le polygone définie.

Le robot va parcourir la map en autonomie. On peut suivre la progression dans Rviz.

    -Ouvrir un nouveau terminal
    -Lancer la commande suivante pour suivre la détection des cannettes : rostopic echo /bottle (le taux de faux positif est élevé)