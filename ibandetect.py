import re


BANK_REGISTRY = {

    # Germany
    "DE": {
        "37040044": "Commerzbank",
        "50010517": "ING Germany",
        "10000000": "Bundesbank",
        "70020270": "HypoVereinsbank",
        "20050550": "Hamburger Sparkasse"
    },

    # France
    "FR": {
        "20041": "BNP Paribas",
        "30004": "Societe Generale",
        "10278": "Credit Mutuel",
        "30066": "CIC Bank"
    },

    # United Kingdom
    "GB": {
        "NWBK": "NatWest",
        "BARC": "Barclays",
        "LOYD": "Lloyds Bank",
        "HBUK": "HSBC UK",
        "MONZ": "Monzo Bank"
    },

    # Estonia
    "EE": {
        "22": "Swedbank Estonia",
        "10": "SEB Pank",
        "77": "LHV Pank",
        "42": "Luminor Bank"
    },

    # Lithuania
    "LT": {
        "32500": "Revolut Bank",
        "70440": "SEB Lithuania",
        "73000": "Swedbank Lithuania",
        "40100": "Luminor Lithuania"
    },

    # Netherlands
    "NL": {
        "INGB": "ING Netherlands",
        "RABO": "Rabobank",
        "ABNA": "ABN AMRO",
        "BUNQ": "bunq"
    },

    # Spain
    "ES": {
        "2100": "CaixaBank",
        "0049": "Banco Santander",
        "0075": "Banco Popular",
        "1465": "ING Spain"
    },

    # Italy
    "IT": {
        "03069": "Intesa Sanpaolo",
        "05034": "Banco BPM",
        "02008": "UniCredit",
        "05428": "Banca Popolare"
    },

    # Belgium
    "BE": {
        "539": "Belfius",
        "068": "BNP Paribas Fortis",
        "340": "KBC Bank"
    }
}



def validate_iban(iban: str) -> bool:
    iban = iban.replace(" ", "").upper()

    if not re.match(r'^[A-Z0-9]{15,34}$', iban):
        return False

    if iban.startswith("EE") and len(iban) != 20:
        return False

    rearranged = iban[4:] + iban[:4]

    numeric_iban = ""
    for char in rearranged:
        if char.isdigit():
            numeric_iban += char
        else:
            numeric_iban += str(ord(char) - 55)

    return int(numeric_iban) % 97 == 1


def extract_bank_from_iban(iban: str):
    iban = iban.replace(" ", "").upper()
    country = iban[:2]

    if country not in BANK_REGISTRY:
        return country, "Unknown Bank"

    if country == "DE":
        bank_code = iban[4:12]
    elif country == "FR":
        bank_code = iban[4:9]
    elif country == "GB":
        bank_code = iban[4:8]
    elif country == "EE":
        bank_code = iban[4:6]
    else:
        return country, "Unknown Bank"

    bank_name = BANK_REGISTRY[country].get(bank_code, "Unknown Bank")
    return country, bank_name

def MOTD():
    cyan = "\033[96m"
    blue = "\033[94m"
    bold = "\033[1m"
    reset = "\033[0m"

    print(f"""{bold}{cyan}
    ________  ___    _   ______  ______________________________
   /  _/ __ )/   |  / | / / __ \/ ____/_  __/ ____/ ____/_  __/
   / // __  / /| | /  |/ / / / / __/   / / / __/ / /     / /   
 _/ // /_/ / ___ |/ /|  / /_/ / /___  / / / /___/ /___  / /    
/___/_____/_/  |_/_/ |_/_____/_____/ /_/ /_____/\____/ /_/     
{blue}                                                              
Welcome to the system.
{reset}""")


if __name__ == "__main__":

    while True:
        MOTD()
        user_input = input("Enter IBAN: ").strip()
        if user_input.lower() in ['exit', 'q']:
            print("Exit")
            break
        if validate_iban(user_input):
            country, bank = extract_bank_from_iban(user_input)
            print("\nValid IBAN ✅")
            print("Country:", country)
            print("Bank:", bank)
        else:
            print("\nInvalid IBAN ❌")
