import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium
import webbrowser

prefix_to_country = {
    "+212": "Maroc",
    "+33": "France",
    "+1": "États-Unis"
}

#number = "+971525430693"
#number = "+33635375954"
number = "+212704845996" 
#number = "+212704845990"
print("Numéro importé :", number)  


pepnumber = phonenumbers.parse(number)
location_en = geocoder.description_for_number(pepnumber, 'en')



if location_en.strip():
    location = location_en
else:
    
    for prefix, country in prefix_to_country.items():
        if number.startswith(prefix):
            location = country
            break
    else:
        location = None

if location:
    print("Le nom du pays est :", location)
else:
    print("Le nom du pays est introuvable.")


carrier_name = carrier.name_for_number(pepnumber, "en")
if carrier_name:
    print("Opérateur téléphonique :", carrier_name)


key = '11136cecc87b41529d958c1f0aa4ec45'  
geocoder_api = OpenCageGeocode(key)

if location:
    results = geocoder_api.geocode(location)

    if results and len(results) > 0:
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        print("Latitude:", lat, "Longitude:", lng)
        myMap = folium.Map(location=[lat, lng], zoom_start=9)
        folium.Marker([lat, lng], popup=location).add_to(myMap)
        myMap.save("mylocation.html")
        print("Carte enregistrée sous 'mylocation.html'")

    else:
        print("Impossible de récupérer les coordonnées géographiques.")
else:
    print("Impossible de géolocaliser le numéro, car l'emplacement est vide.")

webbrowser.open("mylocation.html")
