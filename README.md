# COVID19cz
Data about SARS-CoV-2 pandemic in Czech Republic.

# Requirements:
Python 3, alternatively Python 2 is required to run. Required libraries are matplotlib, scipy, numpy, pandas, datetime and urllib.
Tested on Python 3.9, should work on older. For Python 2 please replace lines for URL retrieve (as shown in the comments).

# You might wanna change these variables as you see fit:
download = True  # 'True' means that the current data from mzcr.cz will be downloaded
N0 = 226-1       # We only wanna visualize from this date (8th of September)
Nfit = N0+85     # We only fit curves from this day.
days_step = 1.0  # Should we show each day? Every single one?
