import scilightcon
import pytest
import datetime
from  zipfile import  ZipFile
from scilightcon.datasets._logs_reader import LogsReader
from scilightcon.utils._fixes import _get_path
import tempfile
import os 

temp_dir = tempfile.mkdtemp()

with _get_path(scilightcon.datasets.DATA_MODULE, 'logsreader_test.zip') as zip_file_path:
    with ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

filepath = os.path.join(temp_dir, 'logsreader_test')
reader = LogsReader(filepath)

def test_list_loggers():

    # 1 - checks that only one folder meets the requirements
    assert (len(reader.list_loggers()) == 1)
    # 2 - Gives back logger name that meets the conditions
    assert (reader.list_loggers() == ['Device 1'])


def test_list_measurables():

    # 1 - raises ValueError when logger name not found
    with pytest.raises(ValueError):
        reader.list_measurables(logger_name= 'idk')
    # 2 - checks that all .txt files are printed
    assert (len(reader.list_measurables(logger_name= 'Device 1')) == 2)


def test_get_data():

    from_date = datetime.datetime(2023,7,15)
    to_date = datetime.datetime(2023,7,15)

    # 1 - raises ValueError when method not found
    with pytest.raises(ValueError):
        reader.get_data(logger_name= 'idk', measurable = "A1-H", from_date = from_date, to_date = to_date)
    # 2 - raises ValueError when measurable not found
    with pytest.raises(ValueError):
        reader.get_data(logger_name= "Device 1", measurable = "idk", from_date = from_date, to_date = to_date)
    

