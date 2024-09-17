import pandas as pd
import requests
import base64
from io import BytesIO
from bs4 import BeautifulSoup

def get_logo_url(company_name):
    possible_domains = [".co.za"]
    for domain in possible_domains:
        api_url = f"https://logo.clearbit.com/{company_name.replace(' ', '')}{domain}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return api_url
    return None

def google_search_for_logo(company_name):
    search_url = f"https://www.google.co.za/search?q={company_name}+logo&tbm=isch"
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            if img.get('src').startswith('http'):
                return img.get('src')
    return None

def image_url_to_base64(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image = BytesIO(response.content)
        base64_image = base64.b64encode(image.getvalue()).decode('utf-8')
        return base64_image
    return None

def fetch_and_convert_logos(company_names):
    logos_base64 = {}
    for company in company_names:
        print(f"Processing {company}...")
        logo_url = get_logo_url(company)
        if not logo_url:
            logo_url = google_search_for_logo(company)
        if logo_url:
            base64_logo = image_url_to_base64(logo_url)
            if base64_logo:
                logos_base64[company] = base64_logo
                print(f"Successfully fetched and converted logo for {company}")
            else:
                print(f"Failed to convert logo for {company}")
        else:
            print(f"Logo not found for {company}")
    return logos_base64

def update_csv_with_logos(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    
    company_names = df['company_name'].unique()
    
    logos_base64 = fetch_and_convert_logos(company_names)
    
    df['logo_base64'] = df['company_name'].apply(lambda x: logos_base64.get(x, ''))
    
    df.to_csv(output_csv, index=False)
    print(f"Updated CSV file saved as {output_csv}")

input_csv = r"C:\Users\janna\Downloads\cardholder_details (1).csv"
output_csv = r"C:\Users\janna\Downloads\output.csv"

update_csv_with_logos(input_csv, output_csv)
