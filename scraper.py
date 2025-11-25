import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
import re

# --- INSTÄLLNINGAR ---
dagar_svenska = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag"]

weekly_keywords = ["veckans pasta", "veckans soppa", "veckans vegetariska", "veckans gröna", "veckans tips", "stående rätter", "klassiker", "veckans husman"]

# Skräpfilter
junk_keywords = [
    "copyright", "©", "rights reserved", "boka", "ring", "mail", 
    "följ oss", "facebook", "instagram", "hitta hit", "öppettider", "stängt",
    "om oss", "kontakt", "karriär", "jobba", "policy", "cookies", 
    "allergier", "fråga personalen", "student", "senior", "barnmeny",
    "konsert", "kongress", "konferens", "lunchhäfte", 
    "nyhetsbrev", "registrera", "erbjudande", "dagens lunch", 
    "välkomna", "välkommen", "smaklig måltid", "logga in",
    "läs mer", "visa mer", "stäng", "meny", "start", "hem", "skip to content",
    "inkl", "serveras", "gäller", "från", "pris", "dryck", "tillbehör", "sides",
    "med reservation", "buffé", "salladsbuffé", "kaffe", "kaka", "take away", "avhämtning"
]

# Mat-filter
food_keywords = [
    "färs", "biff", "stek", "kotlett", "filé", "kyckling", "fisk", "torsk", "lax", "sej", "kolja", "räkor", "skaldjur",
    "skinka", "fläsk", "karré", "korv", "schnitzel", "burgare", "högrev", "kött", "entrecote", "ryggbiff", "oxkind",
    "vegetarisk", "veg", "halloumi", "oumph", "tofu", "bönor", "lins", "kikärt", "falafel", "ost", "paneer", "anama",
    "potatis", "ris", "pasta", "mos", "pommes", "bulgur", "couscous", "quinoa", "nudlar", "gnochi",
    "sås", "sky", "gratäng", "gryta", "soppa", "sallad", "lasagne", "pytt", "wok", "curry", "chili", "bechamel",
    "wallenbergare", "isterband", "raggmunk", "kroppkakor", "pannkaka", "ärtsoppa", "kåldolmar", "kålpudding",
    "bakad", "stekt", "kokt", "grillad", "friterad", "pocherad", "rimmad", "bräserad", "ugnsbakad",
    "chili", "bearnaise", "aioli", "tzatziki", "hummus", "pesto", "pizza", "sushi", "poké", "bowl"
]

restaurants_config = [
    # ================= NORRKÖPING (5 st) =================
    {
        "name": "Enoteket", "city": "Norrköping", "lat": 58.5885, "lon": 16.1885,
        "type": "daily", "url": "https://www.enoteket.se/meny/lunch/", "menu_selector": "div.entry-content",
        "static_data": { "address": "Laxholmen", "rating": 4.6, "price": "135:-", "instagram_url": "https://instagram.com/enoteket", "instagram_handle": "@enoteket", "image": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=600&q=80" }
    },
    {
        "name": "Östgöta Kök", "city": "Norrköping", "lat": 58.5925, "lon": 16.1890,
        "type": "daily", "url": "https://norrkoping.ostgotakok.se/lunchmeny/", "menu_selector": "div.entry-content",
        "static_data": { "address": "Nya Torget", "rating": 4.5, "price": "145:-", "instagram_url": "https://instagram.com/ostgotakok", "instagram_handle": "@ostgotakok", "image": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=600&q=80" }
    },
    {
        "name": "Pappa Grappa", "city": "Norrköping", "lat": 58.5880, "lon": 16.1888,
        "type": "daily", "url": "https://www.pappagrappa.se/norrkoping/meny/", "menu_selector": "div.entry-content",
        "static_data": { "address": "Gamla Torget", "rating": 4.2, "price": "139:-", "instagram_url": "https://instagram.com/pappagrappa", "instagram_handle": "@pappagrappa", "image": "https://images.unsplash.com/photo-1579631542720-3a87824fff86?w=600&q=80" }
    },
    {
        "name": "Brödernas", "city": "Norrköping", "lat": 58.5895, "lon": 16.1895,
        "type": "static", "url": "https://www.brodernas.nu/meny", "menu_selector": "h3", 
        "static_data": { "address": "Gamla Rådstugugatan 28", "rating": 4.3, "price": "129:-", "instagram_url": "https://instagram.com/brodernas", "instagram_handle": "@brodernas", "image": "https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?w=600&q=80" }
    },
    {
        "name": "Spicy Hot", "city": "Norrköping", "lat": 58.5882, "lon": 16.1890,
        "type": "static", "url": "https://www.spicyhot.se/menyer/", "menu_selector": "div.menu-section", 
        "static_data": { "address": "Drottninggatan 55", "rating": 4.0, "price": "115:-", "instagram_url": "https://instagram.com/spicyhotsverige", "instagram_handle": "@spicyhotsverige", "image": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=600&q=80" }
    },

    # ================= LINKÖPING (5 st) =================
    {
        "name": "Stångs Magasin", "city": "Linköping", "lat": 58.4109, "lon": 15.6265,
        "type": "daily", "url": "https://stangsmagasin.se/lunch/", "menu_selector": "div.entry-content",
        "static_data": { "address": "Södra Stånggatan 1", "rating": 4.7, "price": "155:-", "instagram_url": "https://instagram.com/stangsmagasin", "instagram_handle": "@stangsmagasin", "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&q=80" }
    },
    {
        "name": "Pappa Grappa Lkpg", "city": "Linköping", "lat": 58.4105, "lon": 15.6215,
        "type": "daily", "url": "https://www.pappagrappa.se/linkoping/meny/", "menu_selector": "div.entry-content",
        "static_data": { "address": "Ågatan 43", "rating": 4.3, "price": "139:-", "instagram_url": "https://instagram.com/pappagrappa", "instagram_handle": "@pappagrappa", "image": "https://images.unsplash.com/photo-1579631542720-3a87824fff86?w=600&q=80" }
    },
    {
        "name": "Yogi", "city": "Linköping", "lat": 58.4098, "lon": 15.6240,
        "type": "manual", "url": "https://www.yogilinkoping.se", 
        "manual_menu": ["Chicken Tikka Masala", "Palak Paneer (Veg)", "Lamm Curry", "Dagens Naanbröd"], # Hårdkodad meny för säkerhet
        "static_data": { "address": "Platensgatan 5", "rating": 4.5, "price": "125:-", "instagram_url": "https://instagram.com/yogilinkoping", "instagram_handle": "@yogilinkoping", "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600&q=80" } # NY BILD
    },
    {
        "name": "Von Dufva", "city": "Linköping", "lat": 58.4120, "lon": 15.6200,
        "type": "manual", "url": "https://vondufva.se", 
        "manual_menu": ["Wallenbergare med potatismos", "Pocherad torsk med äggsås", "Dagens Vegetariska"], # Hårdkodad
        "static_data": { "address": "Gråbrödragatan 1", "rating": 4.4, "price": "135:-", "instagram_url": "https://instagram.com/stadsmissionenscafeer", "instagram_handle": "@stadsmissionen", "image": "https://images.unsplash.com/photo-1560611021-6b7920fa4996?w=600&q=80" } # NY BILD
    },
    {
        "name": "Ingeborgs", "city": "Linköping", "lat": 58.4100, "lon": 15.6225,
        "type": "manual", "url": "https://ingeborgs.se", 
        "manual_menu": ["Ingeborgs högrevsburgare", "Grillad Levain med kyckling", "Caesarsallad", "Dagens soppa"], # Hårdkodad
        "static_data": { "address": "Ågatan 35", "rating": 4.3, "price": "135:-", "instagram_url": "https://instagram.com/ingeborgs_linkoping", "instagram_handle": "@ingeborgs_lkpg", "image": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=600&q=80" } # NY BILD
    }
]

def clean_text(text):
    text = text.replace("●", "").replace("•", "").replace("*", "").replace("–", "-")
    return text.strip()

def is_valid_dish(line):
    line_lower = line.lower()
    words = line_lower.split()
    if len(words) < 2: return False 
    if re.sub(r'[0-9:kr\-\s]', '', line_lower) == "": return False
    for junk in junk_keywords:
        if junk in line_lower: return False
    if len(line) > 25: return True
    has_food_word = any(word in line_lower for word in food_keywords)
    if has_food_word: return True
    return False

def get_takeaway_price(full_text):
    match = re.search(r'(avhämtning|take\s?away|hämtlunch).*?(\d+)(?:\:|kr|\s?kr|\s?\:-)', full_text, re.IGNORECASE)
    if match: return f"{match.group(2)}:-"
    return None

def parse_menu_smart(full_text, is_daily=False):
    weekday_index = datetime.datetime.now().weekday()
    today_name = dagar_svenska[weekday_index]
    if is_daily and weekday_index > 4: return ["Helg! Se a la carte."]
    
    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
    daily_dishes = []
    weekly_dishes = []
    seen = set()

    for line in lines:
        cleaned = clean_text(line)
        lower = cleaned.lower()
        for wk in weekly_keywords:
            if wk in lower:
                if is_valid_dish(cleaned) and cleaned not in seen:
                    weekly_dishes.append(cleaned.capitalize())
                    seen.add(cleaned)
                break
    
    if is_daily:
        capturing = False
        for line in lines:
            cleaned = clean_text(line)
            lower = cleaned.lower()
            found_day = None
            for dag in dagar_svenska:
                if dag.lower() in lower:
                    found_day = dag; break
            
            if found_day == today_name:
                capturing = True
                content = lower.replace(today_name.lower(), "").strip(" :.-")
                if len(content) > 5 and is_valid_dish(content):
                    dish = cleaned.replace(found_day, "").strip(" :.-").capitalize()
                    if dish not in seen:
                        daily_dishes.append(dish); seen.add(dish)
                continue
            if found_day and found_day != today_name: capturing = False
            
            if capturing:
                is_dup = any(wk in lower for wk in weekly_keywords)
                if is_valid_dish(cleaned) and cleaned not in seen and not is_dup:
                    daily_dishes.append(cleaned.capitalize()); seen.add(cleaned)
    else:
        for line in lines:
            cleaned = clean_text(line)
            if is_valid_dish(cleaned) and cleaned not in seen:
                daily_dishes.append(cleaned); seen.add(cleaned)
    
    final = daily_dishes + weekly_dishes
    return final[:4]

def scrape_lunch():
    output_data = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    print(f"--- Skrapar DagensLunch.se (Topp 10 - Felfri) ---")

    for rest in restaurants_config:
        print(f"Hämtar: {rest['name']} ({rest['city']})...")
        
        if rest.get('type') == 'manual':
            output_data.append({
                "name": rest['name'], "city": rest['city'], "lat": rest['lat'], "lon": rest['lon'],
                "url": rest['url'], "menu": rest.get('manual_menu', []), "takeaway_price": None,
                **rest['static_data']
            })
            continue

        try:
            response = requests.get(rest['url'], headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                for tag in soup(['header', 'nav', 'footer', 'script', 'style', 'form']): tag.decompose()
                
                if rest['menu_selector'] in ['h3', 'h4', 'div.entry-content', 'div.menu-items']:
                    elements = soup.select(rest['menu_selector'])
                    full_text = "\n".join([el.get_text() for el in elements])
                else:
                    content_div = soup.select_one(rest['menu_selector'])
                    if not content_div: content_div = soup.find('body')
                    full_text = content_div.get_text(separator='\n') if content_div else ""

                is_daily = (rest['type'] == 'daily')
                menu_items = parse_menu_smart(full_text, is_daily)
                takeaway = get_takeaway_price(full_text)
            else:
                # Fallback om sidan är nere: Visa inte "Kunde inte nå", utan visa tom lista (hanteras i HTML)
                menu_items = []; takeaway=None

            output_data.append({
                "name": rest['name'], "city": rest['city'], "lat": rest['lat'], "lon": rest['lon'],
                "url": rest['url'], "menu": menu_items, "takeaway_price": takeaway,
                **rest['static_data']
            })
        except Exception as e:
            print(f"Fel {rest['name']}: {e}")
            output_data.append({
                "name": rest['name'], "city": rest['city'], "lat": rest['lat'], "lon": rest['lon'],
                "url": rest['url'], "menu": [], "takeaway_price": None,
                **rest['static_data']
            })
        time.sleep(1)

    with open('lunch_data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    print("--- Klart! ---")

if __name__ == "__main__":
    scrape_lunch()