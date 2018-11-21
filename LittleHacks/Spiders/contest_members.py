import requests
from lxml import etree
import os
import csv

def main():
    os.chdir(r'C:\tmp')
    base_url = 'http://www.cnccac.com/rank-5-'
    count = 23  # How many pages

    with open('test.csv', mode='w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        for i in range(1, (count+1)):
            url = base_url + str(i) + '.html'
            r = requests.get(url)
            e = etree.HTML(r.text)
            
            # Select via css class. 
            par_list = e.xpath("//*[contains(@class, 'phlist1')]")
            sch_list = e.xpath("//*[contains(@class, 'phlist2')]")
            
            for i in range(1, len(par_list)):  # Leave out the 1st element
                writer.writerow([par_list[i].text, sch_list[i].text])
                
        f.close()

if __name__ == '__main__':
    main()