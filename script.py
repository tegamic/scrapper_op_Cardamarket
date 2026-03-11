import os
import re
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =========================
# CONFIGURACIÓN
# =========================
URL = "https://www.cardmarket.com/en/OnePiece/Products/Singles/Awakening-of-the-New-Era-Japanese?searchMode=v2&idCategory=1621&idExpansion=5481&idRarity=0&sortBy=price_desc&perSite=30"
URL = "https://www.cardmarket.com/en/OnePiece/Products/Singles/Adventure-on-Kamis-Island-Asia-Region-Legal?idRarity=0&sortBy=price_desc&perSite=30"
URL = "https://www.cardmarket.com/en/OnePiece/Products/Singles/Emperors-in-the-New-World-Non-English?idRarity=0&sortBy=price_desc&perSite=30"
URL = "https://www.cardmarket.com/en/OnePiece/Products/Singles/Royal-Blood-Non-English?idRarity=0&sortBy=price_desc&perSite=30"
URL = "https://www.cardmarket.com/en/OnePiece/Products/Singles/500-Years-into-the-Future-Japanese?searchMode=v2&idCategory=1621&idExpansion=5587&idRarity=0&sortBy=price_desc&perSite=30"
URL = "https://www.cardmarket.com/en/OnePiece/Products/Singles/Bonds-of-Master-and-Disciple-Non-English?searchMode=v2&idCategory=1621&idExpansion=6157&idRarity=0&sortBy=price_desc&perSite=30"
URL = "https://www.cardmarket.com/en/OnePiece/Products/Singles/Egghead-Crisis-Asia-Region-Legal?idRarity=0&sortBy=price_desc&perSite=30"
URL = "https://www.cardmarket.com/en/OnePiece/Products/Singles/The-Azure-Seas-Seven-Asia-Region-Legal?searchMode=v2&idCategory=1621&idExpansion=6411&idRarity=0&sortBy=price_desc&perSite=30"
URL = "https://www.cardmarket.com/en/OnePiece/Products/Singles/Royal-Blood-Non-English?searchMode=v2&idCategory=1621&idExpansion=5975&idRarity=0&sortBy=price_desc&perSite=30"
URL = "https://www.cardmarket.com/en/OnePiece/Products/Singles/Carrying-on-his-Will-Non-English?searchMode=v2&idCategory=1621&idExpansion=6277&idRarity=0&sortBy=price_desc&perSite=30"
URL = "https://www.cardmarket.com/en/OnePiece/Products/Singles/Adventure-on-Kamis-Island-Asia-Region-Legal?searchMode=v2&idCategory=1621&idExpansion=6504&idRarity=0&sortBy=price_desc&perSite=30"
URL = "https://www.cardmarket.com/en/OnePiece/Products/Singles/Emperors-in-the-New-World-Non-English?searchMode=v2&idCategory=1621&idExpansion=5887&idRarity=0&sortBy=price_desc&perSite=30"
URL = "https://www.cardmarket.com/en/OnePiece/Products/Singles/Awakening-of-the-New-Era-Japanese?searchMode=v2&idCategory=1621&idExpansion=5481&idRarity=0&sortBy=price_desc&perSite=30"

SELECCION = "A35"
COLECCION = ""
CODIGO_COLECCION = "op-05"

JSON_PATH = "data/espirales.json"
IMAGES_DIR = f"images/cartas/{CODIGO_COLECCION}"
TOP_N = 10

HEADLESS = False


# =========================
# UTILIDADES
# =========================
def limpiar_precio(precio_texto: str) -> str:
    """
    '2.500,00 €' -> '2500.00€'
    '119,99 €'   -> '119.99€'
    """
    precio = precio_texto.strip()
    precio = precio.replace(".", "")
    precio = precio.replace(",", ".")
    precio = precio.replace(" €", "€")
    return precio


def limpiar_nombre(nombre: str) -> str:
    """
    Elimina prefijos tipo 'OP05-JP ' y arregla algunos nombres.
    """
    nombre = nombre.strip()
    nombre = re.sub(r"^[A-Z0-9\-]+(?:\s+[A-Z0-9\-]+)?\s+", "", nombre)
    nombre = nombre.replace('Eustass"Captain"Kid', 'Eustass "Captain" Kid')
    nombre = re.sub(r"\s+", " ", nombre).strip()
    return nombre


def cargar_json_existente(path: str) -> dict:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def guardar_json(path: str, data: dict) -> None:
    directorio = os.path.dirname(path)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def guardar_screenshot_imagen(driver, img_element, destino: str) -> None:
    """
    Guarda la imagen renderizada directamente desde el navegador.
    Evita SSL, 403 y bloqueos al descargar desde la URL.
    """
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img_element)
    time.sleep(0.8)

    # Intenta forzar lazy load
    driver.execute_script("""
        const img = arguments[0];
        if (img.dataset && img.dataset.echo && (!img.src || img.src.includes('transparent.gif'))) {
            img.src = img.dataset.echo;
        }
    """, img_element)

    time.sleep(1.2)

    img_element.screenshot(destino)


# =========================
# SELENIUM
# =========================
options = Options()
if HEADLESS:
    options.add_argument("--headless=new")

options.add_argument("--window-size=1600,2200")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
wait = WebDriverWait(driver, 20)


try:
    os.makedirs(IMAGES_DIR, exist_ok=True)

    driver.get(URL)

    # Aceptar cookies si aparecen
    try:
        cookie_buttons = driver.find_elements(By.CSS_SELECTOR, "#CookiesConsent button[type='submit']")
        if cookie_buttons:
            cookie_buttons[0].click()
            time.sleep(1)
    except Exception:
        pass

    cards = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "main.container section > div.row > div.d-flex.mb-4")
        )
    )[:TOP_N]

    cartas = []

    for idx, card in enumerate(cards, start=1):
        # Scroll a la carta
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
        time.sleep(0.8)

        # Nombre
        name_raw = card.find_element(By.CSS_SELECTOR, "h2.card-title").text.strip()
        name = limpiar_nombre(name_raw)

        # Precio
        price_raw = card.find_element(By.CSS_SELECTOR, "p.card-text.text-muted b").text.strip()
        price = limpiar_precio(price_raw)

        # Imagen
        img_tag = card.find_element(By.CSS_SELECTOR, "img")
        filename = f"{CODIGO_COLECCION}_{idx}.png"
        local_file_path = os.path.join(IMAGES_DIR, filename)

        guardar_screenshot_imagen(driver, img_tag, local_file_path)

        cartas.append({
            "nombre": f"#{idx} {name}",
            "precio": price,
            "imagen": f"images/cartas/{CODIGO_COLECCION}/{filename}"
        })

        print(f"Guardada carta #{idx}: {name}")

    nuevo_bloque = {
        "coleccion": COLECCION,
        "cartas": cartas
    }

    data = cargar_json_existente(JSON_PATH)
    data[SELECCION] = nuevo_bloque
    guardar_json(JSON_PATH, data)

    print(f"\nSelección {SELECCION} actualizada correctamente en {JSON_PATH}")
    print(f"Imágenes guardadas en {IMAGES_DIR}")

finally:
    driver.quit()