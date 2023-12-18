# Import necessary libraries
import pandas as pd
from bs4 import BeautifulSoup

# Define a function to extract data from an HTML table


def extract_table_data(html, existing_df):
    """
    Extracts data from an HTML table and updates an existing DataFrame.

    :param html: HTML content containing the table.
    :param existing_df: Existing DataFrame to which the extracted data is added.
    :return: Updated DataFrame with extracted data.
    """

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table with class 'NewSearchResults'
    table = soup.find('table', class_='NewSearchResults')

    # Check if the table is found, if not, return the existing DataFrame
    if not table or not table.find('tbody'):
        return existing_df

    # Create a new DataFrame to store the extracted data
    df = pd.DataFrame(columns=['Link', 'Case #/Received Date',
                      'eFiling Status/Case Status', 'Caption', 'Court/Case Type', 'Empty'])

    # Define a list of keywords to filter the data
    # Replace with your actual keywords
    keywords = [
        "specialty capital",
        "millstone funding",
        "silverline services",
        "instafunders",
        "the lcf group",
        "commissioners of the state insurance fund",
        "specialty capital",
        "the smarter merchant",
        "rdm capital funding",
        "prosperum capital partners",
        "accelerated inventory management",
        "american express national bank",
        "flexibility capital",
        "knightsbridge funding",
        "bizfund",
        "american express national bank",
        "liquidibee 1",
        "security credit services",
        "itria ventures",
        "flash funding services",
        "alternative funding group",
        "liberty funding solutions",
        "funding",
        "dmka",
        "blue sky advance",
        "finance",
    ]

    # Loop through each row in the table's tbody
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')

        # Check if the number of cells is as expected (at least 4)
        if len(cells) < 4:
            continue  # Skip this row as it doesn't have enough cells

        # Extract relevant data from the cells
        case_type = cells[3].get_text().strip().lower()
        caption = cells[2].get_text().strip().lower()

        # Check if the case type matches 'commercial - contract' and if any keyword is in the caption
        if "commercial - contract" in case_type and any(keyword in caption for keyword in keywords):
            # Extract the link if available
            link = cells[0].find('a')['href'] if cells[0].find('a') else None
            link = 'https://iapps.courts.state.ny.us/nyscef/' + \
                link if link else None
            row_data = [link] + [cell.text.strip() for cell in cells]
            df.loc[len(df)] = row_data

    # If an existing DataFrame is provided, concatenate it with the newly extracted data
    if existing_df is not None:
        existing_df = pd.concat([existing_df, df], ignore_index=True)

    return existing_df