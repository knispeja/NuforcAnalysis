import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

destination = r"out.csv"

root_url = r"http://www.nuforc.org/webreports/"
nuforc_root = urlopen(r"http://www.nuforc.org/webreports/ndxevent.html")
nuforc_root_html = nuforc_root.read()

nuforc_root_soup = BeautifulSoup(nuforc_root_html, 'html.parser')

with open(destination, "w", newline='', encoding='utf-8') as output_file:
    field_names = ['event_date', 'reported_date', 'posted_date', 'location', 'shape', 'duration', 'text']
    output_writer = csv.DictWriter(output_file, fieldnames=field_names, delimiter='|')
    output_writer.writerow({
        'event_date': 'event_date',
        'reported_date': 'reported_date',
        'posted_date': 'posted_date',
        'location': 'location',
        'shape': 'shape',
        'duration': 'duration',
        'text': 'text'
    })

    # Read through the table of dates which contain reports
    for page_link_soup in nuforc_root_soup.find('table').find_all('a'):
        link_to_date_page = page_link_soup.attrs['href']
        reports_by_date_html = urlopen(root_url + link_to_date_page).read()
        reports_by_date_soup = BeautifulSoup(reports_by_date_html, 'html.parser')

        print(page_link_soup.text)

        # Read through the table of reports by date and get a report
        for report_link_soup in reports_by_date_soup.find('table').find_all('a'):
            link_to_report_page = report_link_soup.attrs['href']
            report_html = urlopen(root_url + link_to_report_page).read()
            report_soup = BeautifulSoup(report_html, 'html.parser').find('tbody')

            # Parse report metadata
            report_metadata_soup = report_soup.find('td')
            report_metadata_text = report_metadata_soup.get_text(separator='|')
            
            mod_text = report_metadata_text[report_metadata_text.find(':') + 1:]
            date_occurred = mod_text[:mod_text.find('|')].strip()

            mod_text = mod_text[mod_text.find('|') + 1:]
            mod_text = mod_text[mod_text.find(':') + 1:]
            date_reported = mod_text[:mod_text.find('|')].strip()

            mod_text = mod_text[mod_text.find('|') + 1:]
            mod_text = mod_text[mod_text.find(':') + 1:]
            date_posted = mod_text[:mod_text.find('|')].strip()

            mod_text = mod_text[mod_text.find('|') + 1:]
            mod_text = mod_text[mod_text.find(':') + 1:]
            location = mod_text[:mod_text.find('|')].strip()

            mod_text = mod_text[mod_text.find('|') + 1:]
            mod_text = mod_text[mod_text.find(':') + 1:]
            shape = mod_text[:mod_text.find('|')].strip()

            mod_text = mod_text[mod_text.find('|') + 1:]
            mod_text = mod_text[mod_text.find(':') + 1:]
            duration = mod_text.strip()

            # Parse report text
            report_text_soup = report_metadata_soup.find_next('td')
            report_text = report_text_soup.get_text(separator='\n')
            report_text = report_text.replace('|', '/')
            report_text = report_text.replace('\"', '\'')
            report_text = report_text.strip()

            # Write to CSV
            output_writer.writerow({
                'event_date': date_occurred,
                'reported_date': date_reported,
                'posted_date': date_posted,
                'location': location,
                'shape': shape,
                'duration': duration,
                'text': report_text
            })

            print('.', end='', flush=True)