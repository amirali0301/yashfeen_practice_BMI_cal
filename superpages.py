import csv
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time

url = "https://www.superpages.com/search?search_terms=computer&geo_location_terms=ca"

async def fetch(session, url, retries=3):
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"Error fetching {url}. Retrying... ({attempt+1}/{retries})")
            time.sleep(2)  # Wait for 2 seconds before retrying
    return None

async def get_inner_page_data(session, full_url, writer, processed_urls):
    try:
        async with session.get(full_url) as response:
            if response.status != 200:
                print(f"Error accessing {full_url}: Status code {response.status}")
                return

            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            name_element = soup.find("h1", class_="business-name")
            name = name_element.text.strip() if name_element else "Not available"

            # Get the rating
            rating_element = soup.find("div", class_="rating-stars")
            rating = rating_element["class"][1] if rating_element else "Not available"

            # Get the primary category
            primary_category_element = soup.find("div", class_="primary-category")
            primary_category = primary_category_element.text.strip() if primary_category_element else "Not available"

            # Get the location
            location_element = soup.find("h2", class_="address")
            location_full = location_element.text.strip() if location_element else "Not available"

            # Get the time info
            time_info_element = soup.find("div", class_="time-info")
            time_info_onday = time_info_element.text.strip() if time_info_element else "Not available"

            # Get the phone number
            phone_element = soup.find("p", class_="phone")
            phone_number = phone_element.text.strip() if phone_element else "Not available"

            # Get the email
            email_element = soup.find("a", class_="email-business")
            email = email_element["href"].split(":")[1] if email_element else "Not available"

            # Get additional details
            details_section = soup.find("section", id="business-info")

            # Initialize variables for additional details
            general_info = extra_phones = hours = social_links = categories = services_products = brands = website = "Not available"

            if details_section:
                # General Info
                general_info_element = details_section.find("dd", class_="general-info")
                general_info = general_info_element.text.strip() if general_info_element else "Not available"
                
                # Extra Phones
                extra_phones_element = details_section.find("dd", class_="extra-phones")
                extra_phones = extra_phones_element.text.strip() if extra_phones_element else "Not available"
                
                # Hours
                hours_element = details_section.find("dd", class_="open-hours")
                hours = hours_element.text.strip() if hours_element else "Not available"
                
                # Social Links
                social_links_element = details_section.find("dd", class_="social-links")
                social_links = social_links_element.text.strip() if social_links_element else "Not available"
                
                # Categories
                categories_element = details_section.find("dd", class_="categories")
                categories = categories_element.text.strip() if categories_element else "Not available"
                
                # Services/Products
                services_products_element = details_section.find("dt", string="Services/Products")
                if services_products_element:
                    services_products = services_products_element.find_next_sibling("dd").text.strip()
                else:
                    services_products = "Not available"
                
                # Brands
                brands_element = details_section.find("dd", class_="brands")
                brands = brands_element.text.strip() if brands_element else "Not available"
                
                # Other Links
                other_links_element = details_section.find("dd", class_="weblinks")
                website = other_links_element.text.strip() if other_links_element else "Not available"

            # Check if the URL has already been processed
            if full_url not in processed_urls:
                # Append the extracted data to the CSV file
                writer.writerow([name, rating, primary_category, location_full, time_info_onday,email, phone_number, general_info, extra_phones, hours, social_links, categories, services_products, brands, website])
                processed_urls.add(full_url)
    except Exception as e:
        print(f"Error processing inner page {full_url}: {str(e)}")

async def main():
    processed_urls = set()  # Set to store processed URLs
    async with aiohttp.ClientSession() as session:
        try:
            response = await session.get(url)
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            input("Please enter desired data and location manually. Then press Enter to start scraping...")

            # Save parsed components to a CSV file
            output_csv_file = "result3.csv"
            with open(output_csv_file, "w", newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Name', 'RATING', 'PRIMARY CATEGORY', 'COMPLETE LOCATION', 'TODAY TIME', 'EMAIL','PHONE NUMBER', 'DETAILS ABOUT COMPANY', 'FAX/EXTRA PHONE NUMBER', 'HOURS', 'SOCIAL LINKS', 'CATEGORIES', 'SERVICES / PRODUCTS', 'BRANDS INVOLVE', 'WEBSITE'])

                while True:
                    # Extract the complete HTML soup of the page
                    soup = BeautifulSoup(html, 'html.parser')

                    # Find all <div> tags with class "media-thumbnail"
                    media_thumbnail_divs = soup.find_all('div', class_='search-results organic')

                    # List to store inner page tasks
                    inner_page_tasks = []

                    # Iterate over each div with class "media-thumbnail"
                    for div in media_thumbnail_divs:
                        # Find all <a> tags within the div
                        a_tags = div.find_all('a', href=True)

                        # Extract href attributes and clean URLs, removing duplicates
                        for a in a_tags:
                            href = a['href'].strip('"')
                            # Prepend "https://www.yellowpages.com" to each collected URL
                            full_url = f"https://www.superpages.com{href}"
                            # Fetch data from the inner page concurrently
                            inner_page_tasks.append(get_inner_page_data(session, full_url, writer, processed_urls))

                    # Run inner page tasks concurrently
                    await asyncio.gather(*inner_page_tasks)

                    # Find the "Next" button
                    next_button = soup.find('a', class_='next ajax-page')
                    if next_button:
                        # If the "Next" button is found, extract the href attribute and navigate to the next page
                        next_url = f"https://www.superpages.com{next_button['href']}"
                        response = await session.get(next_url)
                        html = await response.text()
                    else:
                        # If there is no "Next" button, break out of the loop
                        break

        except Exception as e:
            print(f"Exception occurred: {e}")

    print(f"All parsed URLs and inner page data saved in {output_csv_file}")

# Run the main coroutine
asyncio.run(main())
