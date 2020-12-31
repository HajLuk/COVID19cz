import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import urllib.request
import pandas as pd
import datetime
from datetime import date


def exponential(x, a, b):  # exponential for one value (used for interpolation)
    return a*np.exp(b*x)


def expfig(x, a, b):  # exponential for set of values (used for visualizing of our interpolation function)
    return [np.float64(a * np.exp(b * ix)) for ix in x]


# You might wanna change these as you see fit:
download = True  # 'True' means that the current data from mzcr.cz will be downloaded
N0 = 226-1  # we only wanna visualize from this date (8th of September)
Nfit = N0+85
days_step = 2.0  # should we show each day?

# download the file (optional), open it and import its contents
filename = 'covid19data.csv'
if download:
    url = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv'
    # data = urllib.URLopener()  # Python 2.7
    # data.retrieve(url, filename)  # Python 2.7
    urllib.request.urlretrieve(url, filename)  # Python 3.7

c19file = open(filename)
covid19data = pd.read_csv(c19file)
cumulative_sick = covid19data['kumulativni_pocet_nakazenych'].values
cumulative_recovered = covid19data['kumulativni_pocet_vylecenych'].values
cumulative_deaths = covid19data['kumulativni_pocet_umrti'].values
cumulative_tests = covid19data['kumulativni_pocet_testu'].values

# variables for day counters
N = len(cumulative_sick)  # size of our data
base = datetime.date(2020, 1, 27)  # the beginning of the data from mzcr.cz (27th of January)
cal = [base + datetime.timedelta(days=x) for x in range(2*N)]  # calendar from the beginning of the data
day_counter = range(1, N)  # all days for which we have data
fwd_day_cnt = range(N0, N)  # only the days that interest us
fit_day_cnt = range(Nfit, N)  # only the days that interest us
exp_day_cnt = range(1, 2*N)  # days visualised with the exponential curve
cal_day_cnt = [i.strftime("%d-%m-%y") for i in cal]  # dates of all days in a human-readable form
sN = N - N0

# allocate and calculate all the data that are not part of our file from mzcr.cz
daily_sick = np.zeros(N)
daily_recovered = np.zeros(N)
daily_deaths = np.zeros(N)
daily_tests = np.zeros(N)
currently_sick = np.zeros(N)
for j in range(1, N):
    daily_sick[j] = cumulative_sick[j] - cumulative_sick[j - 1]
    daily_recovered[j] = cumulative_recovered[j] - cumulative_recovered[j - 1]
    daily_deaths[j] = cumulative_deaths[j] - cumulative_deaths[j - 1]
    daily_tests[j] = cumulative_tests[j] - cumulative_tests[j - 1]
    currently_sick[j] = currently_sick[j - 1] + daily_sick[j] - daily_recovered[j] - daily_deaths[j]

# exponential fit for all our data: interpol_fun(x)=a*exp(b*x)
ab, trash = curve_fit(f=exponential, xdata=fit_day_cnt, ydata=currently_sick[Nfit:N + 1], p0=[0, 0], bounds=(-np.inf, np.inf))
abkuna, trash = curve_fit(f=exponential, xdata=fit_day_cnt, ydata=cumulative_sick  [Nfit:N + 1], p0=[0, 0], bounds=(-np.inf, np.inf))
abkuvy, trash = curve_fit(f=exponential, xdata=fit_day_cnt, ydata=cumulative_recovered  [Nfit:N + 1], p0=[0, 0], bounds=(-np.inf, np.inf))
abkumr, trash = curve_fit(f=exponential, xdata=fit_day_cnt, ydata=cumulative_deaths     [Nfit:N + 1], p0=[0, 0], bounds=(-np.inf, np.inf))
abkute, trash = curve_fit(f=exponential, xdata=fit_day_cnt, ydata=cumulative_tests     [Nfit:N + 1], p0=[0, 0], bounds=(-np.inf, np.inf))

abdena, trash = curve_fit(f=exponential, xdata=fit_day_cnt, ydata=daily_sick        [Nfit:N + 1], p0=[0, 0], bounds=(-np.inf, np.inf))
abdevy, trash = curve_fit(f=exponential, xdata=fit_day_cnt, ydata=daily_recovered        [Nfit:N + 1], p0=[0, 0], bounds=(-np.inf, np.inf))
abdemr, trash = curve_fit(f=exponential, xdata=fit_day_cnt, ydata=daily_deaths           [Nfit:N + 1], p0=[0, 0], bounds=(-np.inf, np.inf))
abdete, trash = curve_fit(f=exponential, xdata=fit_day_cnt, ydata=daily_tests           [Nfit:N + 1], p0=[0, 0], bounds=(-np.inf, np.inf))

# VISUALIZATION
# FIRST FIGURE
fig1 = plt.figure(1)
# currently sick
plt.plot(day_counter, currently_sick[1:N], marker='x', color='r', label="Aktualne nakazeni")  # aktualne
plt.plot(exp_day_cnt, expfig(exp_day_cnt, *ab), '--', color=(0.65, 0, 0), label="Exp. prolozeni aktualne nakazenych")  # fit current
# daily tests
plt.plot(day_counter, daily_tests[1:N], marker='D', color=(1.0, 0.6, 0.0), label="Denni testy")  # testy
plt.plot(exp_day_cnt, expfig(exp_day_cnt, *abdete), '-.', color=(0.65, 0.3, 0.0), label="Exp. prolozeni dennich testu")  # fit tests
# increments
plt.plot(day_counter, daily_sick[1:N], marker='o', color='b', label="Denni prirustky nakazenych")  # prirustky
plt.plot(exp_day_cnt, expfig(exp_day_cnt, *abdena), '-.', color=(0, 0, 0.65), label="Exp. prolozeni prirustku nakazenych")  # fit increments
# plot
ylab = [str(i)+"k" if i > 0 else "0" for i in range(0, 1000, 20)]
plt.xticks(np.arange(0.0, 2.0 * N, days_step), cal_day_cnt[0::days_step], rotation=90)
plt.yticks(np.arange(0.0, 1.0e6, 2.0e4), ylab)
plt.xlim(N0*1.0, N*1.05)
plt.ylim(0.0, exponential(N*1.05, *ab))
plt.legend()
plt.grid()
fig_manager = plt.get_current_fig_manager()
fig_manager.resize(1820, 930)
fig1.show()  # we have special name for it since we want it to be displayed alongside the other figure

# SECOND FIGURE
plt.figure(2)
# cumulative deaths
plt.plot(fwd_day_cnt, cumulative_deaths[N0:N], marker='+', color='k', label="Mrtvi celkem")  # deaths
plt.plot(exp_day_cnt, expfig(exp_day_cnt, *abkumr), '--', color=(0.3, 0.3, 0.3), label="Exp. prolozeni celkove mrtvych")  # fit deaths
# increments of daily deaths
plt.plot(fwd_day_cnt, daily_deaths[N0:N], marker='s', color=(0.65, 0.0, 0.65), label="Denne mrtvi")  # increments of deaths
plt.plot(exp_day_cnt, expfig(exp_day_cnt, *abdemr), '-.', color=(0.35, 0.05, 0.35), label="Exp. prolozeni denne mrtvych")  # fit increments of deaths
# plot
plt.xticks(np.arange(0.0, 2.0 * N, days_step), cal_day_cnt[0::days_step], rotation=90)
plt.yticks(np.arange(0.0, 1.0e6, 5.0e2))
plt.xlim(N0*1.0, N*1.05)
plt.ylim(0.0, exponential(N*1.05, *abkumr))
plt.legend()
plt.grid()
fig_manager = plt.get_current_fig_manager()
fig_manager.resize(1820, 930)
plt.show()
