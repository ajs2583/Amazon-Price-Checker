from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import smtplib

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PW = os.getenv("EMAIL_PW")
SMTP_ADDRESS = os.getenv("EMAIL_SMTP")
URL = os.getenv("WEBSITE_URL")

HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
}

"""
IMPORTANT: REPLACE WITH PRICE THRESHOLD OF YOUR CHOICE
"""
BUY_PRICE = 1


def connect_website(url, header):
    """Connect to the website and return the response."""
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print("Error connecting to the website:", e)
        return None


def parse_price(soup):
    """Extract and return the price from the HTML soup."""
    try:
        price_whole = soup.find("span", class_="a-price-whole").getText(strip=True)
        price_fraction = soup.find("span", class_="a-price-fraction").getText(
            strip=True
        )
        return float(f"{price_whole}{price_fraction}")
    except (AttributeError, ValueError) as e:
        print("Error parsing price:", e)
        return None


def parse_title(soup):
    """Extract and return the product title from the HTML soup."""
    try:
        return soup.find(id="productTitle").getText(strip=True)
    except AttributeError as e:
        print("Error parsing title:", e)
        return "Unknown Product"


def scrape_data(url, header):
    """Scrape the website and return the product title and price."""
    response = connect_website(url, header)
    if response:
        soup = BeautifulSoup(response.text, "html.parser")
        price = parse_price(soup)
        title = parse_title(soup)
        return title, price
    return None, None


def send_email(subject, message, email_address, email_pw, smtp_address):
    """Send an email with the given subject and message."""
    try:
        with smtplib.SMTP(smtp_address, 587) as connection:
            connection.starttls()
            connection.login(email_address, email_pw)
            connection.sendmail(
                from_addr=email_address,
                to_addrs=email_address,
                msg=f"Subject:{subject}\n\n{message}".encode("utf-8"),
            )
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)


def main():
    """Main function to check the price and send an email if necessary."""
    title, price = scrape_data(URL, HEADER)
    if price is not None and price < BUY_PRICE:
        subject = "Amazon Price Alert!"
        message = f"{title} is on sale for {price}!\nCheck it out here: {URL}"
        send_email(subject, message, EMAIL_ADDRESS, EMAIL_PW, SMTP_ADDRESS)
    else:
        print("No price drop detected or unable to fetch data.")


if __name__ == "__main__":
    main()
