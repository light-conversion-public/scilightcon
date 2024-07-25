import datetime
from scilightcon.datasets import LogsReader
import matplotlib.pyplot as plt

directory = r'\\konversija\kleja\ThermologgerLogs\v5'
logger_name = "Location 2B 314"
measurable="A1-H Stalas 1"

reader = LogsReader(directory)

loggers_names_list = reader.list_loggers()
print(loggers_names_list)                                       

measurables = reader.list_measurables(logger_name)
print (measurables)

from_date = datetime.datetime(2023,7,20, 16, 0, 0)
to_date = datetime.datetime(2023,7,21, 21, 0,0)

times, values = reader.get_data(
    logger_name=logger_name,
    measurable=measurable,
    from_date=from_date,
    to_date=to_date)

plt.plot_date(times, values, '-')
plt.grid()
cleaned_measurable = measurable.strip()
words_list = cleaned_measurable.split()
first_word = words_list[0]
if first_word[-1].upper() in ('T'):
    plt.ylabel("Temperature (°C)")
if first_word[-1].upper() in ('H'):
    plt.ylabel("Humidity (%)")
else:
    pass
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('./doc/docs/img/example_logs_reader.png')
plt.show()
