import requests
from bs4 import BeautifulSoup
import json 
import os 

data={}
for year in range(2008, 2019):
    yy = f"{year % 100:02}"  # Last two digits of the year

    for month in range(1, 13):
        mm = f"{month:02}"  

        for i in range(1, 3):

            url = f"https://arxiv.org/abs/{yy}{mm}.{i:05}"
            pdfurl=f"https://arxiv.org/pdf/{yy}{mm}.{i:05}"

            
            response = requests.get(url)
            if response.status_code==404:
                print("Paper not found, Skipping")
            else:
                print("analyzing....")
                soup = BeautifulSoup(response.text, 'html.parser')
                classes = ["title mathjax", "authors", "abstract mathjax","tablecell subjects","dateline"]
                elements = soup.find_all(class_=lambda c: c in classes)
                data[f"{yy}{mm}-{i:05}"] = [element.get_text(strip=True) for element in elements]
                print(url)
                os.system(f"curl {pdfurl} --output Papers/{yy}{mm}-{i:05}.pdf ")
                    

with open("pdfinfo.json", "w") as file:
    json.dump(data, file, indent=4)

print(len(data))