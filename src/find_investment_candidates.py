#!/usr/bin/env python

# Dividend data are easy to scrape from:
# http://www.infobolsa.es/mercado-nacional/mercado-continuo
# Double checked with:
# http://www.bolsamadrid.es/esp/aspx/Empresas/OperFinancieras/Dividendos.aspx
# TODO: Scrape aspx website

# TODO: find optimal tota_dividend/stock_price and plot dividends evolution over the past years

# TODO: write test for the parsing to make sure it is parsed as expected

import pandas as pd
import numpy as np

import csv

def load_data():
    data = pd.read_csv('scrapy/output.csv')
    data['amount'] = data['amount'].apply(pd.to_numeric, errors='ignore')
    return data

def main():
    data = load_data()

    company_dividends = []
    year = 2019
    for company in data['company'].unique():
        company_data_for_year = data.loc[ (data['company'] == company) & (data['exercice'] == year)]
        total_dividend = company_data_for_year['amount'].sum()
        if total_dividend:
            price = float(company_data_for_year['price'].iloc[0].replace(",","."))
            company_dividends.append({
                'company': company,
                'dividend': total_dividend, 
                'price': price, 
                'profitability': total_dividend/price
                })

    sorted_companies = sorted(company_dividends, key = lambda x: x['profitability'], reverse=True)

    csv_column_names = ['company','dividend','price','profitability']
    with open('company_dividends_2019.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_column_names)
        writer.writeheader()
        for data in sorted_companies:
            writer.writerow(data)


if __name__ == '__main__':
    main()
