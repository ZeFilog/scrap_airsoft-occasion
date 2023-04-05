
import requests
import re
import time
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import json

with open("key_airsoft_occasion.json", 'rb') as file:
    KEY = json.load(file)
email = KEY["email_con"]
mdp = KEY["password"]
liens_a = []
id_dejavu = []
liens_id = []
dic_liens = {}
annonce = {'nom','date','prix','ville','titre','num_tel','liste_image_annonce'}

def get_liens(recherche): # Making a GET request to the specified URL with the user's search query included
    response = requests.get("https://www.airsoft-occasion.fr/ads_search.php?sort=1&status=0&keywords="+recherche+"&postcode=&reg=0&cat=95&search_start_date=&search_end_date=&offer=1") # Setting the regular expressions to find the links of the products and the unique ids of the products
    pattern_lien = '<a href="Ads(.+?)" class="bloc_link_listing_1"'
    pattern_id = 'data-id="(.+?)"'

    with open ('code_ao', 'w') as file: # Writing the response to a file named "code_ao"
        file.write(response.text)

    with open ('code_ao', 'r') as file : # Reading the file again
        # Finding the regular expressions in the source code and saving the results in the lists "liens" and "id_ad"
        main = file.read() 
        id_ad = re.findall(pattern_id, main)
        liens = re.findall(pattern_lien, main)
        # Iterating over the "id_ad" list
        for h in id_ad:  # Check if the id is already in the "id_dejavu" list
            if h not in id_dejavu : # If not, append the id to the list "liens_id" and the corresponding link to the list "liens_a"
                #print("id_deja_vu : ",id_dejavu)
                liens_id.append(h)
                for u in liens:
                    liens_replique = ('https://www.airsoft-occasion.fr/Ads%s' % u)
                    liens_a.append(liens_replique) # Creating a dictionary "dic_liens" that maps the product ids to the corresponding links
                for x in range(len(liens_id)):
                    dic_liens[liens_id[x]] = liens_a[x]
                    scrap()
                    # Append the id to the list "id_dejavu" to keep track of the ids that have already been processed
                id_dejavu.append(h)
            else:
                # If the id is already in the "id_dejavu" list, move on to the next id in the "id_ad" list
                pass
    return()


def scrap():
    p = 1 # Initialize the counter for the number of ads
    for d,l in dic_liens.items() :  # Iterate through the dictionary containing the links and ids
        if d in id_dejavu: # Check if the id is already in the list of visited ids
            pass # If it is, pass and move on to the next iteration
        else :
            url_r = (l) # Assign the current link to a variable
            uClient = uReq(url_r) # Open a connection to the website
            page_html = uClient.read()  # Read the html content of the page
            uClient.close() # Close the connection
            page_soup = soup(page_html, features="html.parser") # Parse the html using BeautifulSoup
            with requests.Session() as s: # Use a session to handle cookies and login
                url = "https://www.airsoft-occasion.fr/acc_connexion.php?type=1" # Assign the login url to a variable
                s.get(url) # Retrieve the page
                login_data = {'email_con': email, 'password': mdp} # Store the login data in a dictionary
                s.post(url, data=login_data) # Send a post request with the login data
                s.get(l) # Retrieve the current ad page
                num_tel = s.post('https://www.airsoft-occasion.fr/includes/display/display_phone_ad.php',data={'id_ad': d}).text.replace('<a href=', '').replace('</a>',"") # Scrap the phone number of the ad
            nom = page_soup.find('a', 'second_color').text # Scrap the name of the seller
            date = page_soup.find('time').text # Scrap the date of the ad
            try :
                prix = page_soup.find('p', "p_price_info_ad").text # Scrap the price of the item
            except AttributeError:
                prix = 'pas de prix' # If there is no price specified, assign "pas de prix"
            ville = page_soup.find('p', "p_middle_info_ad").text # Scrap the location of the item
            titre = page_soup.find('h1').text  # Scrap the title of the ad
            image = page_soup.findAll('img', 'thumbnail') # Scrap the images of the ad
            i = 0
            # Initialize the image list and the final image list
            liste_image = []
            liste_image_annonce = []
            # Iterate through the images in the 'image' variable
            for j in image:
                # if the iteration reaches 5, break the loop
                if i == 5: # only 5 images can be posted on a same poste
                    break
                else:
                    # Else, append the current image to the liste_image
                    liste_image.append(image[i])
                # increment the iterator by 1
                i += 1   # Iterate through the liste_image
            for h in liste_image: # Create the image_annonce url by concatenating the base url and the image url and replacing unwanted parts
                image_annonce = "https://www.airsoft-occasion.fr/" + str(h).replace('<img alt="" class="thumbnail" onclick="',"").replace('"/>', "").replace('currentSlide(1)" src="', "").replace('currentSlide(2)" src="', "").replace('currentSlide(3)" src="',"").replace('currentSlide(0)" src="', "")
                liste_image_annonce.append(image_annonce)  # Append the final image url to the final image list
            print('annonce n°%i :' %p, nom, date, prix, ville, titre,num_tel, liste_image_annonce) # Print the final output with the details of the ad
            id_dejavu.append(d) # Append the current ad id to the list of already visited ads
        p += 1
    return()





search = str(input("entrer la recherche : "))
while True :
    get_liens(search)
    time.sleep(10 * 60) # Wait for 10 minutes before running the search again.






