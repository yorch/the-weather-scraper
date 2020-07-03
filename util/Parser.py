import unicodedata
from datetime import datetime, date, timedelta
from util.WeatherClass import Weather


class Parser:
    @staticmethod
    def format_key(key: str) -> str:
        # Replace white space and delete dots
        return key.replace(' ','_').replace('.','')


    @staticmethod
    def parse_html_table_row(date_string: str, history_table: list) -> dict:

        table_rows = [tr for tr in history_table[0].xpath('//tr') if len(tr) == 12]
        headers_list = []
        data_rows = []

        # set Table Headers
        for header in table_rows[0]:
            headers_list.append(header.text)

        for tr in table_rows[1:]:
            row_dict = {}
            for i, td in enumerate(tr.getchildren()):
                td_content = unicodedata.normalize("NFKD", td.text_content())

                # replace time with datetime in first column
                if i == 0:
                    td_content = f'{date_string} {td_content}'
                    date_time = datetime.strptime(td_content, "%Y-%m-%d %I:%M %p")
                    row_dict['Date'] = date_time.strftime('%m/%d/%Y')
                    row_dict['Time'] = date_time.strftime('%I:%M %p')
                else:
                    row_dict[Parser.format_key(headers_list[i])] = td_content

            data_rows.append(row_dict)
        
        return data_rows