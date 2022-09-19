### Comment configurer l'application Web

1. Téléchargez Mongodb et lancez le serveur

2. Installez les pré-requis
Dans le terminal :  
  - pip install -r requirements.txt
  - pip install linkedin-api
  
3. Migrer les modèles
Dans le terminal :
  - python manage.py makemigrations
  - python manage.py migrate
  
4. Créer un utilisateur administrateur
Dans le terminal :
  - python manage.py createsuperuser
  
5. Exécutez l'application Web 
Dans le terminal :
  -  python manage.py runserver
  
6. Ajouter au moins un compte LinkedIn à la base de données
  - Aller à http://127.0.0.1:8000/admin/
  - ajouter nouveau in Linkedin_accounts
