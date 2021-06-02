from datetime import datetime, timedelta
from mpl_finance import candlestick_ohlc, volume_overlay
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import os
import shutil
import warnings
warnings.filterwarnings(action='ignore')


class CandlestickMaker():
    def __init__(self, sample, start_date, end_date):
        """ Initialize CandlestickManager """
        """ This class will generate candlestick images """
        """ from start_date to end_date """
        """ Note that the index of the sample is assumed to be datetime.date """
        first_date = sample.index[0]
        final_date = sample.index[-1]
        print(f"==== Initializing CandlestickManager...")
        print(f"==== Sample Info")
        print(f"==== first date: {first_date}")
        print(f"==== final date: {final_date}")
        print(f"==== CandlestickManager will make candlestick images")
        print(f"==== from {start_date} to {end_date}\n")

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.start_date = start_date.date()
        end_date = end_date.date()

        cushion_date = start_date - timedelta(days=50)
        cushion_date = cushion_date.date()
        if cushion_date < first_date:
            print(f"==== Warning! {cushion_date} before {first_date}")
            print(f"==== may lost first few candlesticks")
        self.cushion = sample[cushion_date:end_date]

    def ohlc_to_candlestick(self, coin_name="coin_Bitcoin", days=5, train=True, use_volume=False):
        # make directories to data folder
        base_dir = os.getcwd() + "/data/Candlesticks/" + \
            coin_name + "/" + str(days) + "days"
        if use_volume:
            base_dir += "/ohlcv"
        else:
            base_dir += "/ohlc"
        if train:
            base_dir += "/train"
        else:
            base_dir += "/test"
        print(f"==== Creating candlestick images...")
        print(f"==== Images will be storced in {base_dir}")

        try:
            os.makedirs(base_dir)
            os.makedirs(base_dir+"/up")
            os.makedirs(base_dir+"/down")
        except:
            print(
                f"==== Warning! directory '{base_dir}' exists! Force to overwrite")
            shutil.rmtree(base_dir)
            os.makedirs(base_dir)
            os.makedirs(base_dir+"/up")
            os.makedirs(base_dir+"/down")

        sample = self.cushion.copy()
        sample['number'] = sample.index.map(mdates.date2num)

        plt.style.use('dark_background')
        # plt.style.use('classic')

        # make labels
        # Labels are based on the last n days candlesticks, which makes more easy to deal with index
        # However, it could be confused in learning step
        # if raise tomorrow -> up, else -> down
        idx = 0
        for date in sample.index:
            if date < self.start_date:
                idx += 1
                continue

            if date != sample.index[idx]:
                print(
                    f"==== Warning: {date} and {sample.index[idx]} is not equal!")

            label = ""
            if (sample.loc[date, 'Close'] - sample.loc[date, 'Open']) / sample.loc[date, 'Close'] > 0.002:
                label = "up"
            else:
                label = "down"

            ohlc = sample.iloc[idx-days:idx, :]
            candles = ohlc[['number', 'Open', 'High', 'Low', 'Close']].copy()
            idx += 1
            dimension = 512
            my_dpi = 96
            fig = plt.figure(figsize=(dimension/my_dpi,
                       dimension/my_dpi), dpi=my_dpi)
            ax1 = fig.add_subplot(1, 1, 1)
            #ax1 = plt.subplot2grid((4, 1), (0, 0), rowspan=3)
            candlestick_ohlc(ax1, candles.values, width=1.,
                             colorup='red', colordown='blue')
            ax1.plot(ohlc.index, ohlc['EMA20'],
                     'c--', marker='o', markersize=3)
            ax1.grid(False)
            ax1.set_xticklabels([])
            ax1.set_yticklabels([])
            ax1.xaxis.set_visible(False)
            ax1.yaxis.set_visible(False)
            ax1.axis('off')

            if use_volume:
                print("volume overlay need fix")
                #ax2 = ax1.twinx()
                # bc = volume_overlay(ax2, ohlc['Open'], ohlc['Close'], ohlc['Volume'],
                #                    width=1, colorup='#77d879', colordown='#db3f3f', alpha=0.5)
                # ax2.add_collection(bc)
                # ax2.grid(False)
                # ax2.set_xticklabels([])
                # ax2.set_yticklabels([])
                # ax2.xaxis.set_visible(False)
                # ax2.yaxis.set_visible(False)
                # ax2.axis('off')

            #ax2 = fig.add_subplot(2, 1, 2)
            #ax2 = plt.subplot2grid((4, 1), (3, 0), rowspan=1)
            #ax2.bar(ohlc.index, ohlc['MACD-hist'], color='c')
            #ax2.plot(ohlc.index, ohlc['signal'], color='b')
            #ax2.plot(ohlc.index, ohlc['MACD'], color='r')
            # ax2.grid(False)
            # ax2.set_xticklabels([])
            # ax2.set_yticklabels([])
            # ax2.xaxis.set_visible(False)
            # ax2.yaxis.set_visible(False)
            # ax2.axis('off')

            # save figure
            pngfile = os.path.join(
                base_dir, label, date.strftime("%Y-%m-%d")+".png")
            plt.savefig(pngfile, pad_inches=0, transparent=False)
            plt.close()
        print(f"==== Conversion for {coin_name} is finished\n")
