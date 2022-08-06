from linkedin_api import Linkedin
li_us ="anass.elbouni@uit.ac.ma"
li_pa = "Bim@1997_"
api = Linkedin(li_us,li_pa)
profil = api.get_profile("yassine-jabairi-04065b159")
print(profil)