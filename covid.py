from datetime import date, timedelta
import os

import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import matplotlib.ticker as ticker

def download_data(data_path):
    URL_BASE = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv'
    URL_HOSP = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv'
    dataframe_base = pd.read_csv(URL_BASE, index_col="datum")
    dataframe_hosp = pd.read_csv(URL_HOSP, index_col="datum")
    dataframe = dataframe_base.join(dataframe_hosp)
    dataframe.to_pickle(data_path)
    return dataframe

def handle_fig(func):
    def wrapper(*args, **kwargs):
        fig = func(*args, **kwargs)
        if "filename" in kwargs:
            filepath = os.path.join(FIG_PATH, kwargs["filename"])
            fig.savefig(filepath, dpi=100)
        if not kwargs["display"]:
            plt.close(fig)
            fig.clf()
    return wrapper

@handle_fig
def plot_data1(dataframe, **kwargs):
    FIGSIZE = (10, 5)
    WINDOWNAME = "Základní přehled"
    tick_spacing = 50
    fig = plt.figure(WINDOWNAME, figsize=FIGSIZE)
    ax = plt.gca()
    ax.plot(dataframe.index, dataframe["prirustkovy_pocet_nakazenych"], label="Nově nakažení")
    plt.xlim(225, dataframe["prirustkovy_pocet_nakazenych"].size*1.05)
    plt.ylim(0.0, np.max(dataframe["prirustkovy_pocet_nakazenych"])*1.1)
    ax.xaxis.set_major_locator(plt.MaxNLocator(125))
    ax.yaxis.set_major_locator(plt.MaxNLocator(25))
    for name, date in DATES.items():
        plt.axvline(dataframe.index.get_loc(date), color="r")
    plt.xticks(rotation=90)
    plt.grid()
    fig_manager = plt.get_current_fig_manager()
    fig_manager.resize(1820, 930)
    plt.subplots_adjust(left=0.03, bottom=0.1, right=0.99, top=0.99, wspace=None, hspace=None)
    plt.legend()
    return fig

@handle_fig
def plot_data2(dataframe, filename=False, display=False):
    FIGSIZE = (12, 4)
    WINDOWNAME = "Úmrtí"
    subset = dataframe.loc[dataframe.index > DATES["breakpoint1"]]
    tick_spacing = 1
    fig = plt.figure(WINDOWNAME, figsize=FIGSIZE)
    ax = plt.gca()
    ax.plot(subset.index, subset["kumulativni_pocet_umrti"], label="Kumulativní počet úmrtí")
    plt.xlim(0, subset["kumulativni_pocet_umrti"].size*1.05)
    plt.ylim(0.0, np.max(subset["kumulativni_pocet_umrti"])*1.1)
    ax.xaxis.set_major_locator(plt.MaxNLocator(125))
    ax.yaxis.set_major_locator(plt.MaxNLocator(25))
    plt.xticks(rotation=90)
    plt.grid()
    fig_manager = plt.get_current_fig_manager()
    fig_manager.resize(1820, 930)
    plt.subplots_adjust(left=0.03, bottom=0.1, right=0.99, top=0.99, wspace=None, hspace=None)
    plt.legend()
    return fig

def robot_export(path=False):
    path = path if path else FIG_PATH

    dataframe = download_data(data_path="data.pckl")

    plot_data1(dataframe, display=True, filename="plot1.png")
    plot_data2(dataframe, display=True)


FIG_PATH = os.path.join("figs")

DATES = {
    "breakpoint1": "2021-10-01",
    "the_other_day": "2020-06-25",
}

if __name__ == "__main__":

    dataframe = download_data(data_path="data.pckl")

    plot_data1(dataframe, display=True, filename="plot1.png")
    plot_data2(dataframe, display=True)

    plt.show()
