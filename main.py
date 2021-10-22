import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import urllib.request
import pandas as pd
import datetime
from datetime import date


def exponential(x, a, b):  # exponential for one value (used for interpolation)
    return a*np.exp(b*x)


def expfig(x, xshift, a, b):  # exponential for set of values (used for visualizing of our interpolation function)
    return [np.float64(a * np.exp(b * (ix-xshift))) for ix in x]


# You might wanna change these as you see fit:
download = True  # 'True' means that the current data from mzcr.cz will be downloaded
N0 = 226-1  # we only wanna visualize from this date (8th of September)
Nfit = N0 + 356  # previously N0+85, the "next wave" is N0+291 (June 26th 2021), next one is N0+335 (Aug 9th 2021), after adjustment N0+356 (Aug 30th 2021)
days_step = 3  # should we show each day?

# download the file (optional), open it and import its contents
c19DataFName = 'covid19data.csv'
hosDataFName = 'hospitadata.csv'
if download:
    url = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv'
    # data = urllib.URLopener()  # Python 2.7
    # data.retrieve(url, filename)  # Python 2.7
    urllib.request.urlretrieve(url, c19DataFName)  # Python 3.7
    url = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv'
    urllib.request.urlretrieve(url, hosDataFName)

c19File = open(c19DataFName)
covid19Data = pd.read_csv(c19File)
cumulative_sick = covid19Data['kumulativni_pocet_nakazenych'].values
cumulative_recovered = covid19Data['kumulativni_pocet_vylecenych'].values
cumulative_deaths = covid19Data['kumulativni_pocet_umrti'].values
cumulative_tests = covid19Data['kumulativni_pocet_testu'].values

hosFile = open(hosDataFName)
hospitaData = pd.read_csv(hosFile)
hosShift = 34  # data for hospitalizations start 34 days later than everything else
currently_hospitalized = np.hstack([np.zeros(hosShift), hospitaData['pocet_hosp'].values])
currently_seriously_ill = np.hstack([np.zeros(hosShift), hospitaData['stav_tezky'].values])
currently_medium = np.hstack([np.zeros(hosShift), hospitaData['stav_stredni'].values])
currently_mild = np.hstack([np.zeros(hosShift), hospitaData['stav_lehky'].values])
currently_asymptomatic = np.hstack([np.zeros(hosShift), hospitaData['stav_bez_priznaku'].values])

# variables for day counters
N = len(cumulative_sick)  # size of our data
base = datetime.date(2020, 1, 27)  # the beginning of the data from mzcr.cz (27th of January)
cal = [base + datetime.timedelta(days=x) for x in range(2*N)]  # calendar from the beginning of the data
day_counter = range(1, N)  # all days for which we have data
fwd_day_cnt = range(N0, N)  # only the days that interest us
#fit_day_cnt = range(Nfit, N)  # only the days that interest us
fit_day_cnt = range(0, N-Nfit)  # only the days that interest us
exp_day_cnt = range(1, 2*N)  # days visualised with the exponential curve
cal_day_cnt = [i.strftime("%d-%m-%y") for i in cal]  # dates of all days in a human-readable form
sN = N - N0

# allocate and calculate all the data that are not part of our file from mzcr.cz
daily_sick = np.zeros(N)
daily_recovered = np.zeros(N)
daily_deaths = np.zeros(N)
daily_tests = np.zeros(N)
currently_sick = np.zeros(N)
hospitalized2Sick = np.zeros(N)
seriously2Sick = np.zeros(N)
medium2Sick = np.zeros(N)
mild2Sick = np.zeros(N)
asymptomatic2Sick = np.zeros(N)

for j in range(1, N):
    daily_sick[j] = cumulative_sick[j] - cumulative_sick[j - 1]
    daily_recovered[j] = cumulative_recovered[j] - cumulative_recovered[j - 1]
    daily_deaths[j] = cumulative_deaths[j] - cumulative_deaths[j - 1]
    daily_tests[j] = cumulative_tests[j] - cumulative_tests[j - 1]
    currently_sick[j] = currently_sick[j - 1] + daily_sick[j] - daily_recovered[j] - daily_deaths[j]
    if currently_sick[j] > 0:
        hospitalized2Sick[j] = currently_hospitalized[j]/currently_sick[j]
        seriously2Sick[j] = currently_seriously_ill[j]/currently_sick[j]
        medium2Sick[j] = currently_seriously_ill[j]/currently_sick[j]
        mild2Sick[j] = currently_seriously_ill[j]/currently_sick[j]
        asymptomatic2Sick[j] = currently_asymptomatic[j]/currently_sick[j]


# exponential fit for all our data: interpol_fun(x)=a*exp(b*x)
ab, trash = curve_fit(f=exponential, xdata=fit_day_cnt, ydata=currently_sick[Nfit:N + 1], p0=[0, 0], bounds=(-np.inf, np.inf))
abkuho, trash = curve_fit(f=exponential, xdata=fit_day_cnt, ydata=currently_hospitalized[Nfit:N + 1], p0=[0, 0], bounds=(-np.inf, np.inf))
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
plt.plot(exp_day_cnt, expfig(exp_day_cnt, Nfit, *ab), '--', color=(0.65, 0, 0), label="Exp. prolozeni aktualne nakazenych")  # fit current
# currently hospitalized
plt.plot(day_counter, currently_hospitalized[1:N], marker='s', color=(0.3, 0.3, 0.3), label="Aktualne hospitalizovani")  # aktualne
plt.plot(exp_day_cnt, expfig(exp_day_cnt, Nfit, *abkuho), '--', color='k', label="Exp. prolozeni aktualne hospitalizovanych")  # fit current
# daily tests
plt.plot(day_counter, daily_tests[1:N], marker='D', color=(1.0, 0.6, 0.0), label="Denni testy")  # testy
plt.plot(exp_day_cnt, expfig(exp_day_cnt, Nfit, *abdete), '-.', color=(0.65, 0.3, 0.0), label="Exp. prolozeni dennich testu")  # fit tests
# increments
plt.plot(day_counter, daily_sick[1:N], marker='o', color='b', label="Denni prirustky nakazenych")  # prirustky
plt.plot(exp_day_cnt, expfig(exp_day_cnt, Nfit, *abdena), '-.', color=(0, 0, 0.65), label="Exp. prolozeni prirustku nakazenych")  # fit increments
# plot
ystep = 5  # ticks on y axis after ystep (in thousands)
ylabel = [str(i) + "k" if i > 0 else "0" for i in range(0, 1000, ystep)]
plt.xticks(np.arange(0.0, 2.0 * N, days_step), cal_day_cnt[0::days_step], rotation=90)
plt.yticks(np.arange(0.0, 1.0e6, ystep*1000.0), ylabel)
plt.xlim(N0*1.0, N*1.05)
plt.ylim(0.0, max(exponential((N-Nfit)*1.05, *ab), 1.05*np.max(currently_sick[1:N])))
plt.legend()
plt.grid()
fig_manager = plt.get_current_fig_manager()
fig_manager.resize(1820, 930)
plt.subplots_adjust(left=0.03, bottom=0.1, right=0.99, top=0.99, wspace=None, hspace=None)
fig1.show()  # we have special name for it since we want it to be displayed alongside the other figure

# SECOND FIGURE (deaths)
fig2 = plt.figure(2)
# cumulative deaths
plt.plot(day_counter, cumulative_deaths[1:N], marker='+', color='k', label="Mrtvi celkem")  # deaths
plt.plot(exp_day_cnt, expfig(exp_day_cnt, Nfit, *abkumr), '--', color=(0.3, 0.3, 0.3), label="Exp. prolozeni celkove mrtvych")  # fit deaths
# increments of daily deaths
plt.plot(day_counter, daily_deaths[1:N], marker='s', color=(0.65, 0.0, 0.65), label="Denne mrtvi")  # increments of deaths
plt.plot(exp_day_cnt, expfig(exp_day_cnt, Nfit, *abdemr), '-.', color=(0.35, 0.05, 0.35), label="Exp. prolozeni denne mrtvych")  # fit increments of deaths
# plot
ystep = 1  # ticks on y axis after ystep (in thousands)
ylabel = [str(i) + "k" if i > 0 else "0" for i in range(0, 1000, ystep)]
plt.xticks(np.arange(0.0, 2.0 * N, days_step), cal_day_cnt[0::days_step], rotation=90)
plt.yticks(np.arange(0.0, 1.0e6, ystep*1000.0), ylabel)
plt.xlim(N0*1.0, N*1.05)
plt.ylim(0.0, max(exponential(N*1.05, *abkumr), 1.05*np.max(cumulative_deaths[N0:N])))
plt.legend()
plt.grid()
fig_manager = plt.get_current_fig_manager()
fig_manager.resize(1820, 930)
plt.subplots_adjust(left=0.03, bottom=0.1, right=0.99, top=0.99, wspace=None, hspace=None)
fig2.show()

# THIRD FIGURE (hospitalized-to-sick ratio)
plt.figure(3)
# all hospitalized to sick
plt.plot(day_counter, hospitalized2Sick[1:N], marker='+', color='b', label="Vsichni hospitalizovani ku nemocnym")
# seriously ill to sick
plt.plot(day_counter, seriously2Sick[1:N], marker='s', color='k', label="Vazne nemocni ku vsem nemocnym")
# medium condition to sick
plt.plot(day_counter, medium2Sick[1:N], marker='s', color='r', label="Stredne nemocni ku vsem nemocnym")
# mild condition to sick
plt.plot(day_counter, mild2Sick[1:N], marker='s', color='y', label="Lehce nemocni ku vsem nemocnym")
# asymptomatic ill to sick
plt.plot(day_counter, asymptomatic2Sick[1:N], marker='o', color='g', label="Bezpriznakovi ku vsem nemocnym")
# plot
ystep = 0.05  # ticks on y axis after ystep (in thousands)
ylabel = [str(i) + " %" for i in range(0, 101, 5)]
plt.xticks(np.arange(0.0, 2.0 * N, days_step), cal_day_cnt[0::days_step], rotation=90)
plt.yticks(np.arange(0.0, 1.01, ystep), ylabel)
plt.xlim(N0*1.0, N*1.0)
plt.ylim(0.0, 0.40)
plt.legend()
plt.grid()
fig_manager = plt.get_current_fig_manager()
fig_manager.resize(1820, 930)
plt.subplots_adjust(left=0.03, bottom=0.1, right=0.99, top=0.99, wspace=None, hspace=None)
plt.show()
