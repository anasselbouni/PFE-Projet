
from linkedin_api import Linkedin

api = Linkedin('anasselbouni@hotmail.com', 'Bim@9200')

profil = api.get_profile('michelleluckychan')

print(profil)