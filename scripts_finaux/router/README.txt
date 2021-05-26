Ce dossier comprend tout les scripts et ressources nécessaires pour les CE.

Configuration initiale du router:
	./init.sh <id_router>

	Le fichier iptables.init comprend la configuration initiale d'iptables

Réservation/Libération de flux:
	./conf.sh 
		-> attends les informations sur l'entrée standard
		-> <@IP_src;@IP_dst;Port_dst;bandwidth;mark;del>

Deamon:
	./reservation_daemon.sh
		-> effectue une écoute permanente sur un port et execute conf.sh avec le paquet reçu