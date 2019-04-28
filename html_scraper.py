from lxml import html
import requests
import pandas as pd


class HtmlScraper:
    """Scrape data (table) from HTML pages

    You may specify the table id to retrive specific table's data in the webpage

    """

    def parse_url(self, url, headers):

        page = requests.get(url, headers=headers)
        return html.fromstring(page.content)

    @staticmethod
    def clean_text(elt):
        return elt.text_content().replace(u'\xa0', u'')

    def parse_html_table(self, root, table_id):
        ''' parse the html table according to the id

        @return the DataFrame from the table including header and data        
        '''

        # Get the table from the root according to the id
        table = root.get_element_by_id(table_id)
        # Retrieve the header information
        table_header = table.xpath('.//th')
        header = [self.clean_text(th) for th in table_header]
        data = [[self.clean_text(td) for td in tr.xpath('.//td')]
                for tr in table.xpath('.//tr')]
        data = [row for row in data if len(row) == len(header)]
        return pd.DataFrame(data, columns=header)

        # print(header)

    def save_to_csv(self, data, columns, filename):
        data.to_csv(path_or_buf=filename, columns=columns,
                    index=False)


def retrieve_data_to_csv(url, filename, cols):
    ''' Scrape data and save to csv files
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    sc = HtmlScraper()
    root = sc.parse_url(url, headers)
    df = sc.parse_html_table(root, "curr_table")

    with open(filename, 'wb') as csvfile:
        sc.save_to_csv(df, cols, csvfile)


if __name__ == "__main__":
    cols = ['Date', 'Price']
    url = 'https://www.investing.com/commodities/gold-historical-data'
    retrieve_data_to_csv(url, "gold.csv", cols)

    url = 'https://www.investing.com/commodities/silver-historical-data'
    retrieve_data_to_csv(url, "silver.csv", cols)
