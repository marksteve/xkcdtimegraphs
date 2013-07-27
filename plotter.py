from cStringIO import StringIO
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates


def plot_time_series(data):
  buf = StringIO()
  plt.xkcd()
  plt.xlabel("Date")
  plt.ylabel("Number of events")
  axes = plt.axes()
  # loc = mdates.AutoDateLocator()
  # axes.xaxis.set_major_locator(loc)
  # axes.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))
  for name, series in data:
    series.sort()
    series = _group_by_date(series)
    times, values = zip(*series)
    # print times, values
    # times = map(datetime.fromtimestamp, times)
    # plt.plot_date(x=times, y=values, label=name)
    plt.plot(times, values, label=name)
  plt.ylim(ymin=0)
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

