import pandas as pd
import requests
import lxml

r = requests.get('http://irsc.ut.ac.ir/index.php?lang=fa')
df = pd.read_html(r.text)[8]
df.to_csv('irsc.csv', index=False)

print(df)