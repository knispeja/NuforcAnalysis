import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

destination = r"out.csv"

root_url = r"http://www.nuforc.org/webreports/"
nuforc_root = urlopen(r"http://www.nuforc.org/webreports/ndxevent.html")
nuforc_root_html = nuforc_root.read()

nuforc_root_soup = BeautifulSoup(nuforc_root_html, 'html.parser')

with open(destination, "w", newline='', encoding='utf-8') as output_file:
    field_names = ['event_date', 'text']
    output_writer = csv.DictWriter(output_file, fieldnames=field_names, delimiter='|')
    output_writer.writerow({'event_date':'event_date', 'text':'text'})

    # Read through the table of dates which contain reports
    for page_link_soup in nuforc_root_soup.find('table').find_all('a'):
        link_to_date_page = page_link_soup.attrs['href']
        reports_by_date_html = urlopen(root_url + link_to_date_page).read()
        reports_by_date_soup = BeautifulSoup(reports_by_date_html, 'html.parser')

        # Read through the table of reports by date and get a report
        for report_link_soup in reports_by_date_soup.find('table').find_all('a'):
            link_to_report_page = report_link_soup.attrs['href']
            report_html = urlopen(root_url + link_to_report_page).read()
            report_soup = BeautifulSoup(report_html, 'html.parser').find('tbody')

            # Parse report metadata
            report_metadata_soup = report_soup.find('td')

            # Parse report text
            report_text_soup = report_metadata_soup.find_next('td')
            report_text = report_text_soup.text
            report_text = report_text.replace('|', '/')

            output_writer.writerow({
                'event_date': report_metadata_soup.text,
                'text': report_text
            })
            
            break # Remove when done


        break # Remove when done