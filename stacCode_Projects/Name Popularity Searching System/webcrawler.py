"""
File: webcrawler.py
Name: 
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
You should see:
---------------------------
2010s
Male Number: 10905209
Female Number: 7949058
---------------------------
2000s
Male Number: 12979118
Female Number: 9210073
---------------------------
1990s
Male Number: 14146775
Female Number: 10644698
"""

import requests
from bs4 import BeautifulSoup


def main():
    for year in ['2010s', '2000s', '1990s']:
        print('---------------------------')
        print(year)
        url = 'https://www.ssa.gov/oact/babynames/decades/names'+year+'.html'
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html)

        # ----- Write your code below this line ----- #

        # soup 裡面的 <tbody> 物件
        tbody = soup.find('tbody')

        # soup 裡面的 rows
        rows = tbody.find_all('tr')

        # count male and female, start at 0
        male_total = 0
        female_total = 0

        # 搜尋出 top 200 names
        for row in rows[:200]:
            columns = row.find_all('td')
            if len(columns) >= 3:
                male_count = int(columns[2].get_text().replace(',', ''))
                female_count = int(columns[4].get_text().replace(',', ''))
                male_total += male_count
                female_total += female_count

        print(f'Male Number: ', male_total)
        print(f'Female Number: ', female_total)


if __name__ == '__main__':
    main()
