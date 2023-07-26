import time
import csv
import random
from bs4 import BeautifulSoup
import requests

def simulate_human_behavior():
    # Simulate human-like behavior by adding random delays between requests
    delay = round(random.uniform(1.5, 3.5), 2)
    time.sleep(delay)

def scrape_website(url):
    # Simulate human-like behavior before making the request
    simulate_human_behavior()

    # Set the provided User-Agent header to mimic a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    # Send the GET request to the website with the headers
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Error: Unable to fetch the content from {url}. Status Code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error: Unable to fetch the content from {url}. Error message: {e}")
        return None
def main():
    # Ask the user to input the URL they want to scrape
    url = input("Enter the URL to scrape: ")

    # Check if the URL is valid
    if not url.startswith("http"):
        print("Error: Invalid URL. Please enter a valid URL starting with 'http' or 'https'.")
        return

    html_content = scrape_website(url)

    if not html_content:
        return

    soup = BeautifulSoup(html_content, "lxml")

    # Extract the title
    title = soup.find("h1").text.strip()

    # Extract the overview
    overview_locality = soup.find("p", class_="localityText__textContent localityText__hide").text.strip()

    # Extracting the heading and paragraph details
    heading_elems = soup.find_all('p', class_='localityText__subHeading')
    paragraph_elems = soup.find_all('p', class_='localityText__textContent')

    # Extracting the text content of the heading and paragraph elements
    headings = [heading.text.strip() for heading in heading_elems]
    paragraphs = [paragraph.text.strip() for paragraph in paragraph_elems]

    # Extracting the "Great Here" section (if present)
    great_here_div = soup.find("div", class_="cd___99XidDetailsList cd__wd50 body_med pageComponent", attrs={"data-label": "GREAT"})
    great_here_content = great_here_div.text.strip() if great_here_div else ""

    # Extracting the "Attention Needed" section (if present)
    attention_needed_div = soup.find("div", class_="cd___99XidDetailsList cd__wd50 body_med pageComponent", attrs={"data-label": "NOT_GREAT"})
    attention_needed_content = attention_needed_div.text.strip() if attention_needed_div else ""

    # Find the <h2> tag with class="ellipsis2Lines" inside the upcoming_div
    upcoming_div = soup.find("div", {"data-label": "UPCOMING_DEVELOPMENTS"})
    header = upcoming_div.find("h2")
    upcoming_developments_heading = header.text.strip() if header else ""
    p_tags = upcoming_div.find_all("p", class_="body_med Ng800 ud__pTag")
    upcoming_developments_content = "\n".join(p.text.strip() for p in p_tags)

    # Find the <h2> tag with class="ellipsis2Lines" for Recommended Properties
    h2_tag = soup.find("h2", class_="ellipsis2Lines")
    recommended_properties_heading = h2_tag.text.strip() if h2_tag else ""
    p_tags_read_more_less = soup.find_all("p", class_="ReadMoreLess__f14")
    recommended_properties_content = "\n".join(p.text.strip() for p in p_tags_read_more_less)

    # Find the <h2> tag with class="pageHeadingDesktop__headingSubheadingWrap" for Nearby Areas
    h2_nearby_areas = soup.find("h2", class_="pageHeadingDesktop__headingSubheadingWrap")
    nearby_areas_heading = h2_nearby_areas.text.strip() if h2_nearby_areas else ""
    # Find all <a> tags with class="lsc__wd lsc__locLabel" for Nearby Areas
    a_tags_nearby_areas = soup.find_all("a", class_="lsc__wd lsc__locLabel")
    # Extract and join the text content from each <a> tag without the word "Overview" for Nearby Areas
    nearby_areas_content = ", ".join(a_tag.text.strip().replace("Overview", "") for a_tag in a_tags_nearby_areas)

    # Find the <h2> tag for Similar Localities
    similar_localities_div = soup.find("div", {"data-label": "SIMILAR_LOCALITIES"})
    h2_similar_localities = similar_localities_div.find("h2")
    similar_localities_heading = h2_similar_localities.text.strip() if h2_similar_localities else ""
    # Find all <a> tags with class="lsc__wd lsc__locLabel" for Similar Localities
    a_tags_similar_localities = similar_localities_div.find_all("a", class_="lsc__wd lsc__locLabel")
    # Extract and join the text content from each <a> tag without the word "Overview" for Similar Localities
    similar_localities_content = ", ".join(a_tag.text.strip().replace("Overview", "") for a_tag in a_tags_similar_localities)

    # Find the <h2> tag for FAQ
    faq_items = soup.find_all("div", class_="fq__divLi")
    faq_heading = "FAQ"
    faq_content = "\n".join(item.text.strip() for item in faq_items)

    # Create a list of dictionaries to store the data
    data_list = [
        {"Column Name": "Title", "Content": title},
        {"Column Name": "Overview", "Content": overview_locality},
        {"Column Name": headings[0], "Content": paragraphs[0]},  # Infrastructure
        {"Column Name": headings[1], "Content": paragraphs[1]},  # Rental Insights
        {"Column Name": "Great Here", "Content": great_here_content},
        {"Column Name": "Attention Needed", "Content": attention_needed_content},
        {"Column Name": upcoming_developments_heading, "Content": upcoming_developments_content},
        {"Column Name": recommended_properties_heading, "Content": recommended_properties_content},
        {"Column Name": nearby_areas_heading, "Content": nearby_areas_content},
        {"Column Name": similar_localities_heading, "Content": similar_localities_content},
        {"Column Name": faq_heading, "Content": faq_content},
    ]

    # Append heading and paragraph details to the data list
    for heading, paragraph in zip(headings[2:], paragraphs[2:]):
        data_list.append({"Column Name": heading, "Content": paragraph})

        # Write the data to a CSV file
    csv_filename = r"C:\Users\amirt\Downloads\99acres_data.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Column Name", "Content"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)

    print(f"Data has been successfully saved to {csv_filename}.")

if __name__ == "__main__":
    main()
