import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.sas.am/ru/catalog/molochnye_produkty/"

request = requests.get(url)
print(request.status_code)

soup = BeautifulSoup(request.text, "html.parser")

product_sliders = soup.select("section.product-slider")

data = []

#worked with product_sliders = soup.select and not with find_all, why?????
for product_slider in product_sliders:
  category_name = product_slider.select_one("h2.product-slider__title").get_text(strip=True)
  products = product_slider.select("div.product-slider__slide")
  for product in products:
    prod_name_el = product.select_one("div.product__name")
    prod_price_el = product.select_one("div.price__new")
    if prod_name_el:
      prod_name = prod_name_el.get_text(strip=True)
      if prod_price_el:
        prod_price = product.select_one(".price__text").contents[0].strip()
      else:
        prod_price = "-1"

        print(prod_name)

      prod_price = int("".join(prod_price.split()))
      data.append({
          "Category": category_name,
          "Product name": prod_name,
          "Price": prod_price
      })

df = pd.DataFrame(data)
print(df.head())

df.to_csv(
    "dairy.csv",
    index=False
)