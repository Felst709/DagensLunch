import json

# --- DIN DATABAS ÖVER RESTAURANGER ---
restaurants = [
    # ================= NORRKÖPING =================
    {
        "name": "Enoteket", 
        "city": "Norrköping", 
        "lat": 58.5885, "lon": 16.1885,
        "price": "137:-",
        "category": ["Husmanskost", "Salladsbuffé"],
        "description": "Stor lunchbuffé med sallad, soppa och hembakat bröd. Välj mellan Dagens pasta, soppa och varmrätter.",
        "url": "https://www.enoteket.se/meny/lunch/", 
        "instagram_url": "https://instagram.com/enoteket", 
        "instagram_handle": "@enoteket", 
        "image": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=600&q=80",
        "address": "Laxholmen", 
        "rating": 4.6
    },
    {
        "name": "Östgöta Kök", 
        "city": "Norrköping", 
        "lat": 58.5925, "lon": 16.1890,
        "price": "149:-",
        "category": ["Premium Husman", "Salladsbuffé"],
        "description": "Vällagad lunch med fokus på närproducerat. Stor salladsbuffé och kaffe ingår.",
        "url": "https://norrkoping.ostgotakok.se/lunchmeny/", 
        "instagram_url": "https://instagram.com/ostgotakok", 
        "instagram_handle": "@ostgotakok", 
        "image": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=600&q=80",
        "address": "Nya Torget", 
        "rating": 4.5
    },
    {
        "name": "Louis De Geer", 
        "city": "Norrköping", 
        "lat": 58.5890, "lon": 16.1840,
        "price": "135:-",
        "category": ["Husmanskost", "Salladsbuffé", "Lunchhäfte"],
        "description": "Klassisk husmanskost i fin miljö. Salladsbuffé, måltidsdryck och kaffe ingår.",
        "url": "https://louisdegeer.se/restaurang/dagens-lunch/", 
        "instagram_url": "https://instagram.com/louisdegeerkonsertkongress", 
        "instagram_handle": "@louisdegeer", 
        "image": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&q=80",
        "address": "Dalsgatan 15", 
        "rating": 4.4
    },
    {
        "name": "Harrys", 
        "city": "Norrköping", 
        "lat": 58.5878, "lon": 16.1920,
        "price": "159:-",
        "category": ["Kött", "Fisk", "Veg", "Salladsbuffé", "AW"],
        "description": "Alltid en kött, en fisk och en vegetarisk rätt. Salladsbuffé och kaffe på maten.",
        "url": "https://harrys.se/sv-se/norrkoeping/menu/aw-shoppinglunch/", 
        "instagram_url": "https://instagram.com/harrysnorrkoping", 
        "instagram_handle": "@harrys_nkpg", 
        "image": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=600&q=80",
        "address": "Drottninggatan 1", 
        "rating": 4.1
    },
    {
        "name": "Pappa Grappa", 
        "city": "Norrköping", 
        "lat": 58.5880, "lon": 16.1888,
        "price": "129:- - 149:-",
        "category": ["Pizza", "Pasta", "AW"],
        "description": "Pizza, pasta och italienska varmrätter. En härlig atmosfär vid Gamla Torget.",
        "url": "https://www.pappagrappa.se/norrkoping/meny/", 
        "instagram_url": "https://instagram.com/pappagrappa", 
        "instagram_handle": "@pappagrappa", 
        "image": "https://images.unsplash.com/photo-1579631542720-3a87824fff86?w=600&q=80",
        "address": "Gamla Torget", 
        "rating": 4.2
    },
    {
        "name": "Brödernas", 
        "city": "Norrköping", 
        "lat": 58.5895, "lon": 16.1895,
        "price": "115:- - 135:-",
        "category": ["Hamburgare", "Sallad"],
        "description": "Grymma hamburgare och sallader. Dagens lunch inkluderar ofta sides och dryck.",
        "url": "https://www.brodernas.nu/meny", 
        "instagram_url": "https://instagram.com/brodernas", 
        "instagram_handle": "@brodernas", 
        "image": "https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?w=600&q=80",
        "address": "Gamla Rådstugugatan 28", 
        "rating": 4.3
    },
    {
        "name": "Spicy Hot", 
        "city": "Norrköping", 
        "lat": 58.5882, "lon": 16.1890,
        "price": "105:- - 125:-",
        "category": ["Asiatiskt", "Wok", "Curry"],
        "description": "Klassiska asiatiska rätter. Välj mellan wok, curry, och friterat. Snabb servering.",
        "url": "https://www.spicyhot.se/menyer/", 
        "instagram_url": "https://instagram.com/spicyhotsverige", 
        "instagram_handle": "@spicyhotsverige", 
        "image": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=600&q=80",
        "address": "Drottninggatan 55", 
        "rating": 4.0
    },
    {
        "name": "Landerholms", 
        "city": "Norrköping", 
        "lat": 58.5875, "lon": 16.1910,
        "price": "119:-",
        "category": ["Husmanskost", "Klassiker"],
        "description": "Vällagad husmanskost i klassisk miljö. Alltid dagens rätt och veckans alternativ.",
        "url": "https://landerholmskonditori.se/", 
        "instagram_url": "https://instagram.com/landerholms", 
        "instagram_handle": "@landerholms", 
        "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80",
        "address": "Hospitalsgatan 5", 
        "rating": 4.7
    },

    # ================= LINKÖPING =================
    {
        "name": "Stångs Magasin", 
        "city": "Linköping", 
        "lat": 58.4109, "lon": 15.6265,
        "price": "145:- - 165:-",
        "category": ["Premium Husman", "Salladsbuffé", "Kravmärkt"],
        "description": "Kravmärkt och närodlat i fantastisk miljö vid ån. Inklusive sallad och kaffe.",
        "url": "https://stangsmagasin.se/lunch/", 
        "instagram_url": "https://instagram.com/stangsmagasin", 
        "instagram_handle": "@stangsmagasin", 
        "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&q=80",
        "address": "Södra Stånggatan 1", 
        "rating": 4.7
    },
    {
        "name": "Pappa Grappa", 
        "city": "Linköping", 
        "lat": 58.4105, "lon": 15.6215,
        "price": "129:- - 149:-",
        "category": ["Italienskt", "Pizza", "Pasta", "Sallad", "Buffé"],
        "description": "Italiensk lunchbuffé och à la carte. Pizza, pasta och sallader i toppklass.",
        "url": "https://www.pappagrappa.se/linkoping/meny/", 
        "instagram_url": "https://instagram.com/pappagrappa", 
        "instagram_handle": "@pappagrappa", 
        "image": "https://images.unsplash.com/photo-1579631542720-3a87824fff86?w=600&q=80",
        "address": "Ågatan 43", 
        "rating": 4.3
    },
    {
        "name": "Yogi", 
        "city": "Linköping", 
        "lat": 58.4098, "lon": 15.6240,
        "price": "139:-",
        "category": ["Indiskt", "Husmanskost", "Sallad"],
        "description": "Autentisk indisk mat. Spännande husmanskost. Ris och sallad ingår alltid.",
        "url": "https://restaurangyogi.com/lunch", 
        "instagram_url": "https://instagram.com/yogilinkoping", 
        "instagram_handle": "@yogilinkoping", 
        "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600&q=80",
        "address": "Platensgatan 5", 
        "rating": 4.5
    },
    {
        "name": "Von Dufva", 
        "city": "Linköping", 
        "lat": 58.4120, "lon": 15.6200,
        "price": "138:-",
        "category": ["Husmanskost", "Kött", "Fisk", "Vegetariskt"],
        "description": "God mat som gör gott. Drivs av Stadsmissionen. Alltid kött, fisk och vegetariskt.",
        "url": "https://stadsmissionenost.se/restaurang-von-dufva/lunch", 
        "instagram_url": "https://instagram.com/stadsmissionenscafeer", 
        "instagram_handle": "@stadsmissionen", 
        "image": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=600&q=80",
        "address": "Gråbrödragatan 1", 
        "rating": 4.4
    },
    {
        "name": "Ingeborgs", 
        "city": "Linköping", 
        "lat": 58.4100, "lon": 15.6225,
        "price": "135:-",
        "category": ["Bageri", "Bistro", "Soppa", "Sallad", "Smörgås"],
        "description": "Hantverksbageri som serverar soppor, grillade smörgåsar och sallader.",
        "url": "https://www.ingeborgsiorebro.se/lunch", 
        "instagram_url": "https://instagram.com/ingeborgs_linkoping", 
        "instagram_handle": "@ingeborgs_lkpg", 
        "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80",
        "address": "Ågatan 35", 
        "rating": 4.3
    },
    {
        "name": "Cioccolata", 
        "city": "Linköping", 
        "lat": 58.4110, "lon": 15.6220,
        "price": "129:- - 145:-",
        "category": ["Italienskt", "Bistro", "Pasta", "Lasagne", "Sallad"],
        "description": "Mysig bistro med pasta, lasagne och fräscha sallader.",
        "url": "https://cioccolata.se", 
        "instagram_url": "https://instagram.com/cioccolatabistro", 
        "instagram_handle": "@cioccolatabistro", 
        "image": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=600&q=80",
        "address": "Ågatan 39", 
        "rating": 4.2
    },
    {
        "name": "Olympia", 
        "city": "Linköping", 
        "lat": 58.4090, "lon": 15.6180,
        "price": "125:-",
        "category": ["Klassisk Husmanskost", "Schnitzel"],
        "description": "Klassisk schnitzel, plankstek och husmanskost i generösa portioner.",
        "url": "https://restaurangolympia.se", 
        "instagram_url": "https://instagram.com/restaurangolympia", 
        "instagram_handle": "@restaurangolympia", 
        "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=600&q=80",
        "address": "Platensgatan 3", 
        "rating": 4.4
    },
    {
        "name": "M.O.O", 
        "city": "Linköping", 
        "lat": 58.4115, "lon": 15.6230,
        "price": "149:- - 169:-",
        "category": ["Premium", "Hamburgare", "Steakhouse"],
        "description": "Kvalitetskött och burgare. En lite lyxigare lunchupplevelse mitt i stan.",
        "url": "https://moo.se/lunch", 
        "instagram_url": "https://instagram.com/moolinkoping", 
        "instagram_handle": "@moolinkoping", 
        "image": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=600&q=80",
        "address": "Ågatan 31", 
        "rating": 4.5
    }
]

def generate_json():
    print("--- Genererar static lunch_data.json ---")
    
    # Spara direkt till filen
    with open('lunch_data.json', 'w', encoding='utf-8') as f:
        json.dump(restaurants, f, ensure_ascii=False, indent=4)
        
    print(f"--- Klart! {len(restaurants)} restauranger sparade. ---")

if __name__ == "__main__":
    generate_json()
