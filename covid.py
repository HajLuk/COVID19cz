import numpy as np
import urllib.request
import pandas as pd
import requests
import matplotlib.pylab as plt
import matplotlib.ticker as ticker



URL_C19 = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv'
URL_HOS = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv'

dataframe_c19 = pd.read_csv(URL_C19, index_col="datum")
# dataframe_hos = pd.read_csv(URL_HOS)

print(dataframe_c19.keys())

tick_spacing = 50

fig, ax = plt.subplots(1,1)
ax.plot(dataframe_c19.index, dataframe_c19["prirustkovy_pocet_nakazenych"])
ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()




# for filepath, url in ((C19_FILEPATH, URL_C19), (HOS_FILEPATH, URL_HOS)):
#     open(filepath, 'wb').write(requests.get(url, allow_redirects=True).content)
#
# dataframe_c19 = read_csv(open(C19_FILEPATH))

# cumulative_sick = covid19Data['kumulativni_pocet_nakazenych'].values
# cumulative_recovered = covid19Data['kumulativni_pocet_vylecenych'].values
# cumulative_deaths = covid19Data['kumulativni_pocet_umrti'].values
# cumulative_tests = covid19Data['kumulativni_pocet_testu'].values

