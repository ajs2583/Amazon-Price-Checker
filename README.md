# Amazon Price Tracker

A simple Python script to monitor the price of a product on Amazon and send an email notification when the price drops below a defined threshold.

## Features

- Scrapes product title and price from an Amazon product page  
- Sends an email alert if the price falls below your set target  
- Uses environment variables to securely store credentials and configuration  
- Easily customizable and lightweight  

## Getting Started

### 1. Clone the Repository

git clone https://github.com/ajs2583/amazon-price-tracker.git
cd amazon-price-tracker

### 2. Install Dependencies

pip install -r requirements.txt

requirements.txt:
beautifulsoup4
requests
python-dotenv

### 3. Create a .env File

In the root directory, create a `.env` file and add the following:

EMAIL_ADDRESS=your_email@example.com
EMAIL_PW=your_email_password
EMAIL_SMTP=smtp.your-email-provider.com
WEBSITE_URL=https://www.amazon.com/dp/YOUR_PRODUCT_ID

Note: If you're using Gmail, you may need to enable "less secure app access" or create an app-specific password.

## Usage

Run the script:
```
python main.py
```
If the product's price is below your defined threshold (BUY_PRICE), an email alert will be sent to the email address you specified.

## Configuration

To set your target price, change this line in the script:
```python
BUY_PRICE = 100  # Set your desired price threshold
```
## Notes

- This script relies on Amazon's current page structure. If it changes, the script may need to be updated.
- For personal and educational use only.
- Avoid sending frequent or excessive requests to Amazon.

## License

This project is licensed under the MIT License.
