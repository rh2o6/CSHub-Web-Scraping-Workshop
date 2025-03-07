import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
from typing import *
from bs4 import BeautifulSoup
import csv


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )



def example1bs4():

    soup = BeautifulSoup(requests.get("https://www.scrapethissite.com/pages/simple/").content, "html.parser")

    countries = soup.findAll("div", class_="country")
    
    if(countries):
        print("Succesfully found countries")


  


    sorted_countries_by_area = sorted(countries, key=lambda country: float(country.find(class_="country-area").get_text(strip = True)))


    for country in sorted_countries_by_area:
        name = country.find(class_="country-name")
        area = country.find(class_="country-area")
        print(f"{name.get_text(strip = True)}: {area.get_text(strip = True)}")




def example1selenium():
    driver.get("https://www.scrapethissite.com/pages/simple/")
    countries = driver.find_elements(By.CLASS_NAME,"country")
    if(countries):
        print("Succesfully found countries!")

    else:
        print("Elements not found.")


    sorted_countries_by_area = sorted(countries, key=lambda country: float(country.find_element(By.CLASS_NAME, "country-area").text.replace(',', '')))

    for country in sorted_countries_by_area:
        name = country.find_element(By.CLASS_NAME,"country-name").text
        area = country.find_element(By.CLASS_NAME,"country-area").text
        print(f"{name}: {area}")


def example2selenium():

    driver.get("https://www.scrapethissite.com/pages/forms/")
    myTable = driver.find_element(By.CLASS_NAME, "table")

    # Extract rows
    rows = myTable.find_elements(By.TAG_NAME,"tr")
    headers = myTable.find_elements(By.TAG_NAME,"th")

    # Extract header row
    header_row = []


    if headers:
        for header in headers:
            header_row.append(header.text.strip())

    # Extract table data
    table_data = []


    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")  # Use "th" for headers
        row_data = []
        for cell in cells:
            row_data.append(cell.text)
        
        if row_data:  # Remove empty rows
            table_data.append(row_data)

    # Print headers
    print(header_row)

    # Print table data
    for row in table_data:
        for cell in row:
            print(row)

    # Save data to CSV
    with open("scraped_table.csv", "w", newline="", encoding="utf-8") as file:
        
        writer = csv.writer(file)

        # Write headers if present
        if header_row:
            writer.writerow(header_row)

        # Write data
        for row in table_data:
            writer.writerow(row)

    print("CSV file saved!")


def example2bs4():
    url = "https://www.scrapethissite.com/pages/forms/"
    response = requests.get(url)
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the table
    my_table = soup.find("table")

    # Extract headers (if any)
    headers = my_table.find_all("th")

    header_row = []

    if(headers):
        for header in headers:
            header_row.append(header.text.strip())

    # Extract table rows
    rows = my_table.find_all("tr")
    
    # Process the table data
    table_data = []
    for row in rows:
        cells = row.find_all("td")
        cells_text = []

        for cell in cells:
            cells_text.append(cell.text.strip())


        table_data.append(cells_text)

    row_data = []
    

    if row_data:  # Ensure the row is not empty
        table_data.append(row_data)

    for row in table_data:
        if row == []:
            table_data.remove(row)

    # Print header and data
    print(header_row)
    for i in table_data:
        print(i)
    
    # Save to CSV
    with open("scraped_table.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write headers if present
        if header_row:
            writer.writerow(header_row)

        # Write data
        writer.writerows(table_data)

    print("CSV file saved!")


    

def playerLookup():

    playertofind = input("Enter the name of a NBA player currently playing:")
    driver.get("https://www.nba.com/players")



    #To avoid some unnecesary element from popping up
    driver.refresh()
    driver.refresh()
    driver.refresh()
    driver.refresh()    

    #Find the searchbar

    searchbar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "Block_blockAd__1Q_77")))
    searchbar.click()
    time.sleep(1)
    input_field = searchbar.find_element(By.TAG_NAME,"div")
    input_field = input_field.find_element(By.TAG_NAME,"input")
    time.sleep(3)
    input_field.click()

    
    for letter in playertofind:
        driver.execute_script("arguments[0].value += arguments[1];", input_field, letter)
        time.sleep(0.2) 
    
    

    

    input_field.send_keys(" ")

    playerTable = driver.find_element(By.CLASS_NAME,"players-list")
    time.sleep(1)
    playerbio = playerTable.find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,"td")
    playername = playerbio[0].text
    playername = playername.lstrip()
    playername = playername.rstrip()
    print(playername)
    playerlink = playerbio[0].find_element(By.TAG_NAME,"a").get_attribute("href")
    print(playerlink)
    print(f"Player Info: \n Name-{playername}, Team-{playerbio[1].text}, Number-{playerbio[2].text}, Position-{playerbio[3].text}, Player Link:{playerlink}")

playerLookup()

input("Press Enter to exit...")