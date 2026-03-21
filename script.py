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
from urllib.parse import urlparse


# =========================
# CONFIGURACIÓN
# =========================

#BlackFlame
URL = "https://www.pricecharting.com/console/pokemon-japanese-ruler-of-the-black-flame?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#WildForce
URL = "https://www.pricecharting.com/console/pokemon-japanese-wild-force?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#SilverLance
URL = "https://www.pricecharting.com/console/pokemon-japanese-silver-lance?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#InfernoX
URL = "https://www.pricecharting.com/console/pokemon-japanese-inferno-x?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#MegaBrave
URL = "https://www.pricecharting.com/console/pokemon-japanese-mega-brave?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#Blue Sky Stream
URL = "https://www.pricecharting.com/console/pokemon-japanese-blue-sky-stream?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#Eevee Heroes
URL = "https://www.pricecharting.com/console/pokemon-japanese-eevee-heroes?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#RagingSurf
URL = "https://www.pricecharting.com/console/pokemon-japanese-raging-surf?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#CyberJudge
URL = "https://www.pricecharting.com/console/pokemon-japanese-cyber-judge?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#WhiteFlare
URL = "https://www.pricecharting.com/console/pokemon-japanese-white-flare?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#StellarMiracle
URL = "https://www.pricecharting.com/console/pokemon-japanese-stellar-miracle?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#MatchlessFighters
URL = "https://www.pricecharting.com/console/pokemon-japanese-matchless-fighter?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#Star-birth
URL = "https://www.pricecharting.com/console/pokemon-japanese-star-birth?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#LostAbyss
URL = "https://www.pricecharting.com/console/pokemon-japanese-lost-abyss?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#super-electric-breaker
URL = "https://www.pricecharting.com/console/pokemon-japanese-super-electric-breaker?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#skyscraping-perfection
URL = "https://www.pricecharting.com/console/pokemon-japanese-skyscraping-perfection?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#glory-of-team-rocket
URL = "https://www.pricecharting.com/console/pokemon-japanese-glory-of-team-rocket?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#glory-of-team-rocket
URL = "https://www.pricecharting.com/console/pokemon-japanese-glory-of-team-rocket?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#terastal-festival
URL = "https://www.pricecharting.com/console/pokemon-japanese-terastal-festival?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#NIHIL-ZERO
URL = "https://www.pricecharting.com/console/pokemon-japanese-nihil-zero?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#Battle-Partners
URL = "https://www.pricecharting.com/console/pokemon-japanese-battle-partners?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#heat-wave-arena
URL = "https://www.pricecharting.com/console/pokemon-japanese-heat-wave-arena?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#black-bolt
URL = "https://www.pricecharting.com/console/pokemon-japanese-black-bolt?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#mega-dream
URL = "https://www.pricecharting.com/console/pokemon-japanese-mega-dream-ex?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#violet-ex
URL = "https://www.pricecharting.com/console/pokemon-japanese-violet-ex?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#triplet-beat
URL = "https://www.pricecharting.com/console/pokemon-japanese-triplet-beat?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#shiny-star-v
URL = "https://www.pricecharting.com/console/pokemon-japanese-shiny-star-v?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#shiny-treasure-ex
URL = "https://www.pricecharting.com/console/pokemon-japanese-shiny-treasure-ex?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#OP-07
URL = "https://www.pricecharting.com/console/one-piece-japanese-500-years-in-the-future?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#legacy-of-the-master
URL = "https://www.pricecharting.com/console/one-piece-japanese-legacy-of-the-master?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#extra-booster-egghead-crisis
URL = "https://www.pricecharting.com/console/one-piece-japanese-extra-booster-egghead-crisis?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#azure-sea%27s-seven
URL = "https://www.pricecharting.com/console/one-piece-japanese-azure-sea%27s-seven?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#one-piece-japanese-royal-blood
URL = "https://www.pricecharting.com/console/one-piece-japanese-royal-blood?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#one-piece-japanese-carrying-on-his-will
#URL = "https://www.pricecharting.com/console/one-piece-japanese-carrying-on-his-will?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#one-piece-japanese-adventure-on-kami%27s-island
URL = "https://www.pricecharting.com/console/one-piece-japanese-adventure-on-kami%27s-island?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#one-piece-japanese-emperors-in-the-new-world
#URL = "https://www.pricecharting.com/console/one-piece-japanese-emperors-in-the-new-world?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#one-piece-japanese-awakening-of-the-new-era
#URL = "https://www.pricecharting.com/console/one-piece-japanese-awakening-of-the-new-era?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#one-piece-japanese-fist-of-divine-speed
#URL = "https://www.pricecharting.com/console/one-piece-japanese-fist-of-divine-speed?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#one-piece-japanese-extra-booster-anime-25th-collection
#URL = "https://www.pricecharting.com/console/one-piece-japanese-extra-booster-anime-25th-collection?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#pokemon-japanese-vstar-universe
#URL = "https://www.pricecharting.com/console/pokemon-japanese-vstar-universe?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#one-piece-japanese-extra-booster-heroines-edition
#URL = "https://www.pricecharting.com/console/one-piece-japanese-extra-booster-heroines-edition?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="
#pokemon-ascended-heroes
URL = "https://www.pricecharting.com/console/pokemon-ascended-heroes?sort=highest-price&model-number=&model-number=&exclude-hardware=true&exclude-variants=false&show-images=true&in-collection="


def obtener_codigo_coleccion_desde_url(url: str) -> str:
    ruta = urlparse(url).path.rstrip("/")
    return ruta.split("/")[-1]

SELECCION = "A66"
COLECCION = ""
CODIGO_COLECCION = obtener_codigo_coleccion_desde_url(URL)

JSON_PATH = "data/espirales_valladolid.json"
IMAGES_DIR = f"images/cartas/{CODIGO_COLECCION}"
TOP_N = 10

HEADLESS = False


# =========================
# UTILIDADES
# =========================


def limpiar_precio(precio_texto: str) -> str:
    return precio_texto.strip()


def limpiar_nombre(nombre: str) -> str:
    """
    Limpia espacios extra.
    """
    nombre = nombre.strip()
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
    src = img_element.get_attribute("src") or ""
    src_grande = src.replace("/60.jpg", "/1600.jpg")

    if not src_grande:
        raise ValueError("No se pudo obtener la URL de la imagen")

    ventana_original = driver.current_window_handle

    driver.switch_to.new_window("tab")
    driver.get(src_grande)

    img_grande = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "img"))
    )

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script(
            "return arguments[0].complete && arguments[0].naturalWidth > 0;",
            img_grande
        )
    )

    time.sleep(0.5)
    img_grande.screenshot(destino)

    driver.close()
    driver.switch_to.window(ventana_original)


def obtener_texto_precio(card) -> str:
    """
    Prioriza used_price.
    Si está vacío, prueba cib_price y luego new_price.
    """
    selectores = [
        "td.used_price .js-price",
        "td.cib_price .js-price",
        "td.new_price .js-price",
    ]

    for selector in selectores:
        try:
            texto = card.find_element(By.CSS_SELECTOR, selector).text.strip()
            if texto:
                return texto
        except Exception:
            pass

    return ""

def obtener_texto_precio_psa_10(card) -> str:
    """
    Usa la columna new_price como precio PSA 10.
    Si está vacía, devuelve cadena vacía.
    """
    try:
        return card.find_element(By.CSS_SELECTOR, "td.new_price .js-price").text.strip()
    except Exception:
        return ""


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

    rows = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "tbody tr[data-product]")
        )
    )[:TOP_N]

    cartas = []

    for idx, row in enumerate(rows, start=1):
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
        time.sleep(0.5)

        # Nombre
        name_raw = row.find_element(By.CSS_SELECTOR, "td.title a").text.strip()
        name = limpiar_nombre(name_raw)

        # Precio
        price_raw = obtener_texto_precio(row)
        price = limpiar_precio(price_raw)

        # Precio PSA 10
        price_psa_10_raw = obtener_texto_precio_psa_10(row)
        price_psa_10 = limpiar_precio(price_psa_10_raw)

        # Imagen
        img_tag = row.find_element(By.CSS_SELECTOR, "td.image img.photo")
        filename = f"{CODIGO_COLECCION}_{idx}.png"
        local_file_path = os.path.join(IMAGES_DIR, filename)

        guardar_screenshot_imagen(driver, img_tag, local_file_path)

        cartas.append({
    "nombre": f"#{idx} {name}",
    "precio": price,
    "precio_psa_10": price_psa_10,
    "imagen": f"images/cartas/{CODIGO_COLECCION}/{filename}"
})

        print(f"Guardada carta #{idx}: {name} - {price}")

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