
import requests
import re
import time
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pdb
import json
import pdb

with open("key_airsoft_occasion.json", 'rb') as file:
    KEY = json.load(file)
email = KEY["email_con"]
mdp = KEY["password"]
liens_a = []
id_dejavu = []
liens_id = []
dic_liens = {}
annonce = {'nom','date','prix','ville','titre','num_tel','liste_image_annonce'}
replique_dejavu = []
#creer une fonction pour demander la recherche
def get_liens(recherche):

    response = requests.get("https://www.airsoft-occasion.fr/ads_search.php?sort=1&status=0&keywords="+recherche+"&postcode=&reg=0&cat=95&search_start_date=&search_end_date=&offer=1")
    print(response)
    #pdb.set_trace()
    pattern_lien = '<a href="Ads(.+?)" class="bloc_link_listing_1"'
    pattern_id = 'data-id="(.+?)"'

    with open ('code_ao', 'w') as file:
        file.write(response.text)

    with open ('code_ao', 'r') as file :
        main = file.read()
        id_ad = re.findall(pattern_id, main)
        liens = re.findall(pattern_lien, main)
        for h in id_ad:
            if h not in id_dejavu :
                #print("id_deja_vu : ",id_dejavu)
                liens_id.append(h)
                for u in liens:
                    liens_replique = ('https://www.airsoft-occasion.fr/Ads%s' % u)
                    liens_a.append(liens_replique)
                for x in range(len(liens_id)):
                    dic_liens[liens_id[x]] = liens_a[x]
                    scrap()
                id_dejavu.append(h)

            else:
                pass

            #for x in range(len(liens_id)):
                #dic_liens[liens_id[x]] = liens_a[x]
                #scrap()
        #print(dic_liens)
    return()

    # en haut ça se connecter et cela recupere les liens des annonce sur la 1er pages
    # en bas ça scrap



def scrap():
    p = 1
    for d,l in dic_liens.items() :
        if d in id_dejavu:
            pass
        else :
            url_r = (l)
            uClient = uReq(url_r)
            page_html = uClient.read()
            uClient.close()
            page_soup = soup(page_html, features="html.parser")
            with requests.Session() as s:
                url = "https://www.airsoft-occasion.fr/acc_connexion.php?type=1"
                s.get(url)
                login_data = {'email_con': email, 'password': mdp}
                aa = s.post(url, data=login_data)
                main1 = s.get(l)
                num_tel = s.post('https://www.airsoft-occasion.fr/includes/display/display_phone_ad.php',data={'id_ad': d}).text.replace('<a href=', '').replace('</a>',"")


            nom = page_soup.find('a', 'second_color').text
            date = page_soup.find('time').text
            try :
                prix = page_soup.find('p', "p_price_info_ad").text
            except AttributeError:
                prix = 'pas de prix'
            ville = page_soup.find('p', "p_middle_info_ad").text
            titre = page_soup.find('h1').text
            image = page_soup.findAll('img', 'thumbnail')
            i = 0
            liste_image = []
            liste_image_annonce = []
            for j in image:
                if i == 5:
                    break
                else:
                    liste_image.append(image[i])
                i += 1
            for h in liste_image:
                image_annonce = "https://www.airsoft-occasion.fr/" + str(h).replace('<img alt="" class="thumbnail" onclick="',"").replace('"/>', "").replace('currentSlide(1)" src="', "").replace('currentSlide(2)" src="', "").replace('currentSlide(3)" src="',"").replace('currentSlide(0)" src="', "")
                liste_image_annonce.append(image_annonce)
            print( 'annonce n°%i :' %p,nom, date, prix, ville, titre,num_tel, liste_image_annonce)
            #annonce[nom, date, prix, ville, titre,num_tel]
            id_dejavu.append(d)
        p += 1

    return()





search = 'ak' #str(input("entrer la recherche : "))
while True :
    get_liens(search)
    time.sleep(1)






