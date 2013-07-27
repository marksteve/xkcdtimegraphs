from cStringIO import StringIO
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

colors = 'bgrcmyk'
markers = 'o^Ds*'

def plot_time_series(data):
  buf = StringIO()
  plt.xkcd()
  plt.xlabel("Date")
  plt.ylabel("Number of events")
  axes = plt.axes()
  # loc = mdates.AutoDateLocator()
  # axes.xaxis.set_major_locator(loc)
  # axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
  max_y = 0
  for i, (name, series) in enumerate(data):
    series.sort()
    series = _group_by_date(series)
    # print name, series
    times, values = zip(*series)
    max_y = max(max_y, max(values))
    # times = map(datetime.fromtimestamp, times)
    plt.plot(times, values,
             label=name,
             color=colors[i%len(colors)],
             markersize=10.0,
             marker=markers[i%len(markers)],
             )
    # plt.plot_date(x=times, y=values, label=name,
    #               color=colors[i%len(colors)],
    #               markersize=10.0,
    #               marker=markers[i%len(markers)],
    #               )
  plt.ylim(ymin=0, ymax=max_y+10)
  xlim = plt.xlim()
  plt.xlim(xlim[0]-3, xlim[1]+3)
  plt.legend()
  plt.savefig(buf, format='png')
  plt.close()
  return buf.getvalue()

def _group_by_date(series):
  nseries = []
  prev_date = None
  for ts, value in series:
    d = datetime.fromtimestamp(ts).date()
    if prev_date == d:
      nseries[-1][1] += value
    else:
      prev_date = d
      nseries.append([d, value])
  return nseries

