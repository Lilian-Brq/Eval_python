Exercice 1
Q1 : Il faut utiliser le verbe POST et le code 201 (created)
Q2 : 404 Not Found
Q3 : le code 401 c'est pour l'authentifaction et le code 403 c'est pour l'autorisation 
        401 --> Si on essaye d'acceder a une page protegé par un compte, le serveur refuse l'accés si on ets pas authentifier

        403 --> le serveur sait qui on est mais il refuse car on a pas les droits administrateur



Exercice 3 
Q4 :   Lors du lancement de uvicorn windows bloque l'installation : apres recherche, il aurait fallut passer avec sqlite3 mais ca faisait changer tout nos fichiers et ne correspondrait plus au demande du tp. 

note: This error originates from a subprocess, and is likely not a problem with pip.
ERROR: Failed to build 'sqlalchemy' when installing build dependencies for sqlalchemy
