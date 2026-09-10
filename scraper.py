import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
import re

# --- INSTÄLLNINGAR FÖR SKRAPNING ---
dagar_svenska = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag"]
weekly_keywords = ["veckans pasta", "veckans soppa", "veckans vegetariska", "veckans gröna", "veckans tips", "stående rätter", "klassiker"]
junk_keywords = ["copyright", "boka", "ring", "mail", "följ oss", "öppettider", "stängt", "allergier", "inkl", "gäller", "kontantfri", "se meny på hemsidan"]
food_keywords = ["färs", "biff", "kyckling", "fisk", "torsk", "lax", "vegetarisk", "veg", "halloumi", "pasta", "soppa", "sallad", "lasagne", "gryta", "schnitzel", "burgare", "pizza"]

# --- DATABASEN (Kategorier & Prisintervall + Skrap-länkar) ---
restaurants_config = [
    # ================= NORRKÖPING (8 st) =================
    {
        "name": "Enoteket", "city": "Norrköping", "lat": 58.5885, "lon": 16.1885,
        "type": "daily", "url": "https://www.enoteket.se/meny/lunch/", "menu_selector": "div.entry-content",
        "static_data": { 
            "price": "125:- - 145:-", "category": ["Husmanskost", "Salladsbuffé"],
            "address": "Laxholmen", "rating": 4.6, 
            "instagram_url": "https://instagram.com/enoteket", "instagram_handle": "@enoteket", 
            "image": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=600&q=80" 
        }
    },
    {
        "name": "Östgöta Kök", "city": "Norrköping", "lat": 58.5925, "lon": 16.1890,
        "type": "daily", "url": "https://norrkoping.ostgotakok.se/lunchmeny/", "menu_selector": "div.entry-content",
        "static_data": { 
            "price": "135:- - 155:-", "category": ["Premium Husman", "Salladsbuffé"],
            "address": "Nya Torget", "rating": 4.5, 
            "instagram_url": "https://instagram.com/ostgotakok", "instagram_handle": "@ostgotakok", 
            "image": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=600&q=80" 
        }
    },
    {
        "name": "Louis De Geer", "city": "Norrköping", "lat": 58.5890, "lon": 16.1840,
        "type": "daily", "url": "https://louisdegeer.se/restaurang/dagens-lunch/", "menu_selector": "div.elementor-widget-container", 
        "static_data": { 
            "price": "135:-", "category": ["Husmanskost", "Salladsbuffé", "Lunchhäfte"],
            "address": "Dalsgatan 15", "rating": 4.4, 
            "instagram_url": "https://instagram.com/louisdegeerkonsertkongress", "instagram_handle": "@louisdegeer", 
            "image": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&q=80" 
        }
    },
    {
        "name": "Harrys", "city": "Norrköping", "lat": 58.5878, "lon": 16.1920,
        "type": "static", "url": "https://harrys.se/sv-se/norrkoeping/menu/aw-shoppinglunch/", "menu_selector": "div.menu-items", 
        "static_data": { 
            "price": "129:-", "category": ["Kött", "Fisk", "Veg", "Salladsbuffé", "AW"],
            "address": "Drottninggatan 1", "rating": 4.1, 
            "instagram_url": "https://instagram.com/harrysnorrkoping", "instagram_handle": "@harrys_nkpg", 
            "image": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=600&q=80" 
        }
    },
    {
        "name": "Pappa Grappa", "city": "Norrköping", "lat": 58.5880, "lon": 16.1888,
        "type": "daily", "url": "https://www.pappagrappa.se/norrkoping/meny/", "menu_selector": "div.entry-content",
        "static_data": { 
            "price": "129:- - 149:-", "category": ["Pizza", "Pasta", "AW"],
            "address": "Gamla Torget", "rating": 4.2, 
            "instagram_url": "https://instagram.com/pappagrappa", "instagram_handle": "@pappagrappa", 
            "image": "https://images.unsplash.com/photo-1579631542720-3a87824fff86?w=600&q=80" 
        }
    },
    {
        "name": "Brödernas", "city": "Norrköping", "lat": 58.5895, "lon": 16.1895,
        "type": "static", "url": "https://www.brodernas.nu/meny", "menu_selector": "h3", 
        "static_data": { 
            "price": "115:- - 135:-", "category": ["Hamburgare", "Sallad"],
            "address": "Gamla Rådstugugatan 28", "rating": 4.3, 
            "instagram_url": "https://instagram.com/brodernas", "instagram_handle": "@brodernas", 
            "image": "https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?w=600&q=80" 
        }
    },
    {
        "name": "Spicy Hot", "city": "Norrköping", "lat": 58.5882, "lon": 16.1890,
        "type": "static", "url": "https://www.spicyhot.se/menyer/", "menu_selector": "div.menu-section", 
        "static_data": { 
            "price": "105:- - 125:-", "category": ["Asiatiskt", "Wok", "Curry"],
            "address": "Drottninggatan 55", "rating": 4.0, 
            "instagram_url": "https://instagram.com/spicyhotsverige", "instagram_handle": "@spicyhotsverige", 
            "image": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=600&q=80" 
        }
    },
    {
        "name": "Landerholms", "city": "Norrköping", "lat": 58.5875, "lon": 16.1910,
        "type": "static", "url": "https://landerholmskonditori.se/", "menu_selector": "div.entry-content p",
        "static_data": { 
            "price": "119:-", "category": ["Husmanskost", "Klassiker"],
            "address": "Hospitalsgatan 5", "rating": 4.7, 
            "instagram_url": "https://instagram.com/landerholms", "instagram_handle": "@landerholms", 
            "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80" 
        }
    },

    # ================= LINKÖPING (8 st) =================
    {
        "name": "Stångs Magasin", "city": "Linköping", "lat": 58.4109, "lon": 15.6265,
        "type": "daily", "url": "https://stangsmagasin.se/lunch/", "menu_selector": "div.entry-content",
        "static_data": { 
            "price": "145:- - 165:-", "category": ["Premium Husman", "Salladsbuffé", "Kravmärkt"],
            "address": "Södra Stånggatan 1", "rating": 4.7, 
            "instagram_url": "https://instagram.com/stangsmagasin", "instagram_handle": "@stangsmagasin", 
            "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&q=80" 
        }
    },
    {
        "name": "Pappa Grappa", "city": "Linköping", "lat": 58.4105, "lon": 15.6215,
        "type": "daily", "url": "https://www.pappagrappa.se/linkoping/meny/", "menu_selector": "div.entry-content",
        "static_data": { 
            "price": "129:- - 149:-", "category": ["Italienskt", "Pizza", "Pasta", "Buffé"],
            "address": "Ågatan 43", "rating": 4.3, 
            "instagram_url": "https://instagram.com/pappagrappa", "instagram_handle": "@pappagrappa", 
            "image": "https://images.unsplash.com/photo-1579631542720-3a87824fff86?w=600&q=80" 
        }
    },
    {
        "name": "Yogi", "city": "Linköping", "lat": 58.4098, "lon": 15.6240,
        "type": "manual", "url": "https://restaurangyogi.com/lunch", 
        "manual_menu": ["Chicken Tikka Masala", "Palak Paneer (Veg)", "Lamm Curry", "Dagens Naanbröd"],
        "static_data": { 
            "price": "139:-", "category": ["Indiskt", "Husmanskost", "Sallad"],
            "address": "Platensgatan 5", "rating": 4.5, 
            "instagram_url": "https://instagram.com/yogilinkoping", "instagram_handle": "@yogilinkoping", 
            "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600&q=80" 
        }
    },
    {
        "name": "Von Dufva", "city": "Linköping", "lat": 58.4120, "lon": 15.6200,
        "type": "manual", "url": "https://stadsmissionenost.se/restaurang-von-dufva/lunch", 
        "manual_menu": ["Kött: Pannbiff med stekt lök", "Fisk: Panerad spätta", "Veg: Morotsbiffar"],
        "static_data": { 
            "price": "138:-", "category": ["Husmanskost", "Kött", "Fisk", "Vegetariskt"],
            "address": "Gråbrödragatan 1", "rating": 4.4, 
            "instagram_url": "https://instagram.com/stadsmissionenscafeer", "instagram_handle": "@stadsmissionen", 
            "image": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=600&q=80" 
        }
    },
    {
        "name": "Ingeborgs", "city": "Linköping", "lat": 58.4100, "lon": 15.6225,
        "type": "manual", "url": "https://www.ingeborgsiorebro.se/lunch", 
        "manual_menu": ["Grillad Levain med kyckling", "Ingeborgs högrevsburgare", "Dagens Värmande Soppa"],
        "static_data": { 
            "price": "135:-", "category": ["Bageri", "Bistro", "Soppa", "Sallad"],
            "address": "Ågatan 35", "rating": 4.3, 
            "instagram_url": "https://instagram.com/ingeborgs_linkoping", "instagram_handle": "@ingeborgs_lkpg", 
            "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80" 
        }
    },
    {
        "name": "Cioccolata", "city": "Linköping", "lat": 58.4110, "lon": 15.6220,
        "type": "manual", "url": "https://cioccolata.se", 
        "manual_menu": ["Husets Lasagne", "Krämig Oxfilépasta", "Caesarsallad"],
        "static_data": { 
            "price": "129:- - 145:-", "category": ["Italienskt", "Bistro", "Pasta", "Lasagne"],
            "address": "Ågatan 39", "rating": 4.2, 
            "instagram_url": "https://instagram.com/cioccolatabistro", "instagram_handle": "@cioccolatabistro", 
            "image": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=600&q=80" 
        }
    },
    {
        "name": "Olympia", "city": "Linköping", "lat": 58.4090, "lon": 15.6180,
        "type": "manual", "url": "https://restaurangolympia.se", 
        "manual_menu": ["Klassisk Schnitzel med bearnaise", "Husets Panerade Fisk", "Dagens Vegetariska"],
        "static_data": { 
            "price": "125:-", "category": ["Klassisk Husmanskost", "Schnitzel"],
            "address": "Platensgatan 3", "rating": 4.4, 
            "instagram_url": "https://instagram.com/restaurangolympia", "instagram_handle": "@restaurangolympia", 
            "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=600&q=80" 
        }
    },
    {
        "name": "M.O.O", "city": "Linköping", "lat": 58.4115, "lon": 15.6230,
        "type": "static", "url": "https://moo.se/lunch", "menu_selector": "body",
        "static_data": { 
            "price": "149:- - 169:-", "category": ["Premium", "Hamburgare", "Steakhouse"],
            "address": "Ågatan 31", "rating": 4.5, 
            "instagram_url": "https://instagram.com/moolinkoping", "instagram_handle": "@moolinkoping", 
            "image": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=600&q=80" 
        }
    }
]

def clean_text(text):
    return text.replace("●", "").replace("•", "").replace("*", "").replace("–", "-").strip()

def is_valid_dish(line):
    line_lower = line.lower()
    if len(line_lower.split()) < 2: return False 
    if re.sub(r'[0-9:kr\-\s]', '', line_lower) == "": return False
    for junk in junk_keywords:
        if junk in line_lower: return False
    if len(line) > 25: return True
    return any(word in line_lower for word in food_keywords)

def parse_menu_smart(full_text, is_daily=False):
    weekday_index = datetime.datetime.now().weekday()
    today_name = dagar_svenska[weekday_index]
    if is_daily and weekday_index > 4: return []
    
    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
    daily_dishes = []
    seen = set()

    if is_daily:
        capturing = False
        for line in lines:
            cleaned = clean_text(line)
            lower = cleaned.lower()
            found_day = next((dag for dag in dagar_svenska if dag.lower() in lower), None)
            
            if found_day == today_name:
                capturing = True
                content = lower.replace(today_name.lower(), "").strip(" :.-")
                if len(content) > 5 and is_valid_dish(content) and cleaned not in seen:
                    daily_dishes.append(cleaned.replace(found_day, "").strip(" :.-").capitalize())
                    seen.add(cleaned)
                continue
            if found_day and found_day != today_name: capturing = False
            
            if capturing and is_valid_dish(cleaned) and cleaned not in seen:
                daily_dishes.append(cleaned.capitalize())
                seen.add(cleaned)
    else:
        for line in lines:
            cleaned = clean_text(line)
            if is_valid_dish(cleaned) and cleaned not in seen:
                daily_dishes.append(cleaned)
                seen.add(cleaned)
    
    return daily_dishes[:4]

def scrape_lunch():
    output_data = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    print(f"--- Skrapar luncher ---")

    for rest in restaurants_config:
        print(f"Hämtar: {rest['name']}...")
        
        if rest.get('type') == 'manual':
            output_data.append({"name": rest['name'], "city": rest['city'], "lat": rest['lat'], "lon": rest['lon'], "url": rest['url'], "menu": rest.get('manual_menu', []), **rest['static_data']})
            continue

        try:
            response = requests.get(rest['url'], headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                for tag in soup(['header', 'nav', 'footer', 'script', 'style', 'form']): tag.decompose()
                
                content_div = soup.select_one(rest['menu_selector']) if rest['menu_selector'] not in ['h3', 'h4', 'div.entry-content', 'div.menu-items'] else None
                if not content_div and rest['menu_selector'] in ['h3', 'h4', 'div.entry-content', 'div.menu-items']:
                    full_text = "\n".join([el.get_text() for el in soup.select(rest['menu_selector'])])
                else:
                    full_text = content_div.get_text(separator='\n') if content_div else soup.find('body').get_text(separator='\n')

                menu_items = parse_menu_smart(full_text, (rest['type'] == 'daily'))
                if not menu_items and 'manual_menu' in rest: menu_items = rest['manual_menu']
            else:
                menu_items = rest.get('manual_menu', [])

            output_data.append({"name": rest['name'], "city": rest['city'], "lat": rest['lat'], "lon": rest['lon'], "url": rest['url'], "menu": menu_items, **rest['static_data']})
        except Exception as e:
            output_data.append({"name": rest['name'], "city": rest['city'], "lat": rest['lat'], "lon": rest['lon'], "url": rest['url'], "menu": rest.get('manual_menu', []), **rest['static_data']})
        time.sleep(1)

    with open('lunch_data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    print("--- Klart! ---")

if __name__ == "__main__":
    scrape_lunch()
