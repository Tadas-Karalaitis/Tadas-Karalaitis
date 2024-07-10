# DONE The program should be run with two command line arguments - an email address and an API to use (one out of two that you have implemented)
# DONE Your program should first check if the format of the command line arguments is valid
# DONE The email provided should be checked. It can be as complex as you choose to be – the most simple implementation would simply check whether an “@” and a “.” exist.
# DONE The program should check whether the API argument passed is one of the two that you have implemented
# DONE Your program should then call the API chosen.
# DONE The information received from an API should be formatted into a human-readable message and sent to the email which was provided in the command line argument. You should use a Gmail account for sending the email.
# DONE You should only use Python’s in-built libraries to send the email via a Gmail account
# DONE Your program should use the try/except statements at least once.
# DONE Your program should have at least 3 unit tests.
# DONE At the end of the file, as a comment, add the 5 keybinds you researched in Part 1 of this sprint


from email.message import EmailMessage # for representing an email message
import sys # for maneging command line arguments
import os # for reaching secure variables with sensitive information
from dotenv import load_dotenv # for loading email adress and email password from hidden file .env
import ssl # for secure connection
import smtplib # for sending an email message
import requests # to import APIs
import json 


load_dotenv() 


apis = ["weather", "exchange_rates"]


# Some random text, just to test git stuff

def main():
    if len(sys.argv) != 3:
        print(
            'You have to enter 2 command line arguments: valid email adress and API name ("weather" or "exchange_rate")'
        )
        sys.exit(1)
    email_adress = sys.argv[1]
    api = sys.argv[2]
    try:
        validate_arguments(email_adress, api)
    except Exception as e:  # exception from validate_arguments function
        sys.exit(e)
    # cheking what API is selected by user and declairing send_email function arguments for each case of API selection
    if api == "weather":
        sub = "Weather update proudly presented by Tadas Karalaitis"
        content = weather()
    elif api == "exchange_rates":
        sub = "Latest currency exchange rates proudly presented by Tadas Karalaitis "
        content = exchange_rates()
    send_email(sub, content)
    print('email successfully sent!!!')


# checking if command line arguments are valid
def validate_arguments(email_adress, api):
    if (email_adress.count("@") != 1 or "." not in email_adress) and (api not in apis):
        raise Exception(
            'Your both command line arguments are invalid. First one has to be valid email adress and second - API name "weather" or "exchange_rates"'
        )
    elif email_adress.count("@") != 1 or "." not in email_adress:
        raise Exception(
            "Invalid first command line argument! It has to be valid email adress."
        )
    elif api not in apis:
        raise Exception(
            'Invalid second command line argument! It has to be API name "weather" or "exchange_rates"'
        )


# weather API
def weather():
    api_key = os.getenv("weatherstack_key")
    url = f"http://api.weatherstack.com/current?access_key={api_key}"
    querystring = {"query": "Vilnius"}
    response = requests.get(url, params=querystring)
    file = response.json()
    location = file["request"]["query"]
    temp = file["current"]["temperature"]
    description = file["current"]["weather_descriptions"]
    wind = file["current"]["wind_speed"]
    wind_dir = file["current"]["wind_dir"]
    humid = file["current"]["humidity"]
    forecast = f"Subscribed location: {location}\nDescription: {description[0]}\nTemperature: {temp}\nWind: {wind} km/h, direction - {wind_dir}\nHumidity: {humid} RH"
    return forecast


# exchange_rates API
def exchange_rates():
    api_key = os.getenv("exchange_rates_key")

    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=USD,GBP,AUD,CNY,INR,JPY,KRW,MXN,RUB&base={'EUR'}"

    payload = {}
    headers = {"apikey": api_key}
    response = requests.request("GET", url, headers=headers, data=payload)
    result_str = response.text
    result = json.loads(result_str) # converting result_str to a dictionary
    rate_date = result["date"]
    rate_USD = round(result["rates"]["USD"], 2)
    rate_GBP = round(result["rates"]["GBP"], 2)
    rate_AUD = round(result["rates"]["AUD"], 2)
    rate_CNY = round(result["rates"]["CNY"], 2)
    rate_INR = round(result["rates"]["INR"], 2)
    rate_JPY = round(result["rates"]["JPY"], 2)
    rate_KRW = round(result["rates"]["KRW"], 2)
    rate_MXN = round(result["rates"]["MXN"], 2)
    rate_RUB = round(result["rates"]["RUB"], 2)
    rates = f"Here are {rate_date} your subscribed excange rates for 1 Euro:\n{rate_USD} USD;\n{rate_GBP} GBP;\n{rate_AUD} AUD;\n{rate_CNY} CNY;\n{rate_INR} INR;\n{rate_JPY} JPY;\n{rate_KRW} KRW;\n{rate_MXN} MXN;\n{rate_RUB} RUB."
    return rates

# function to send email
def send_email(sub, content):
    email_sender = os.getenv("email_adress")
    email_password = os.getenv("email_psv")
    emain_receiver = sys.argv[1]
    subject = sub
    body = content
    em = EmailMessage()
    em["from"] = email_sender
    em["to"] = emain_receiver
    em["subject"] = subject
    em.set_content(body) # creating an email message
    context = ssl.create_default_context() # creating secure connection
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp: # connection to Gmail’s email server smtp.gmail.com - server's adress, 465 - port's number.
        smtp.login(email_sender, email_password)  # logging in to Gmail account.
        smtp.sendmail(email_sender, emain_receiver, em.as_string()) # sending an email.


if __name__ == "__main__":
    main()


# 1. Ctrl+k Ctrl+s - Opens all keyboard shortcuts
# 2. Shift+Alt+UP or Shift+Alt+DOWN - copy the line or selected lines
# 3. Ctrl+`` - opens a terminal
# 4. Alt+up/down - moves a line or selected lines up and down
# 5. Ctrl+up/down - scroles up and down
