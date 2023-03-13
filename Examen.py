"""
Opdracht:

Bepalingen:
 - Je moet gebruik maken van de aangeleverde variable(n)
 - Je mag deze variable(n) niet aanpassen
 - Het is de bedoeling dat je op het einde 1 programma hebt
 - Inlever datum is zondag avond 13 maart 2023 18:00CET
 - Als inlever formaat wordt een git url verwacht die gecloned kan worden

/ 5 ptn 1 - Maak een public repository aan op jouw gitlab/github account voor dit project
/10 ptn 2 - Gebruik python om de gegeven api url aan te spreken
/20 ptn 3 - Gebruik regex om de volgende data te extracten:
    - Jaar, maand en dag van de created date
    - De provider van de nameservers (bijv voor 'ns3.combell.net' is de provider 'combell')
/15 ptn 4 - Verzamel onderstaande data en output alles als yaml. Een voorbeeld vind je hieronder.
    - Het land van het domein
    - Het ip van het domain
    - De DNS provider van het domein
    - Aparte jaar, maand en dag van de created date


Totaal  /50ptn
"""

""" voorbeeld yaml output

created:
  dag: '18'
  jaar: '2022'
  maand: '02'
ip: 185.162.31.124
land: BE
provider: combell

"""

url = "https://api.domainsdb.info/v1/domains/search?domain=syntra.be"


import requests
import re
import yaml



def get_domain_data(domain):
    """
    Haal de gegevens van de opgegeven domeinnaam op via de url
    """
    url = f"https://api.domainsdb.info/v1/domains/search?domain={domain}"
    response = requests.get(url)
    data = response.json()
    return data



def extract_domain_info(data):
    """
    Extracteer de benodigde gegevens uit de gegevens die zijn opgehaald via de API
    """
    created_date = re.search(r"(\d{4})-(\d{2})-(\d{2})T", data["domains"][0]["create_date"])
    jaar, maand, dag = created_date.groups()
    provider = re.search(r"\.(.+)\.", data["domains"][0]["NS"][0]).group(1)
    land = data["domains"][0]["country"]
    ip = data["domains"][0]["A"][0]
    provider = data["domains"][0]["NS"][0]
    return (dag, maand, jaar, ip, land, provider)


def format_output(dag, maand, jaar, ip, land, provider):
    """
    Formatteer de output als YAML
    """
    output = {
        "created": {
            "dag": dag,
            "jaar": jaar,
            "maand": maand
        },
        "ip": ip,
        "land": land,
        "provider": provider,
        
    }
    return yaml.dump(output)


if __name__ == "__main__":
    domain = "syntra.be"
    data = get_domain_data(domain)
    dag, maand, jaar, ip, land, provider = extract_domain_info(data)
    output = format_output(dag, maand, jaar, ip, land, provider)
    print(output)












