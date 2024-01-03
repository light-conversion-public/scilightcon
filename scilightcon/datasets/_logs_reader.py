import datetime
import pytest
from datetime import date
import numpy as np
import os
import glob
from pathlib import Path
from typing import List

__doctest_skip__ = ['*']
class LogsReader:
    """
    Reader object for getting time-dependent data from logs folders, created by different software (Argos, CEP, ThermoLoggers, etc.) 

    Examples:

        >>> from scilightcon.datasets import LogsReader # doctest: +SKIP
        >>> import datetime # doctest: +SKIP
        >>> directory = r'\\\\konversija\kleja\ThermologgerLogs\\v5' # doctest: +SKIP
        >>> reader = LogsReader(directory) # doctest: +SKIP
        >>> loggers_names_list = reader.list_loggers() # doctest: +SKIP
        >>> loggers_names_list # doctest: +SKIP
        ['Location 2B 314', 'Location 2D 3.14 Logger 1-4', 'Location 2D 3.14 Logger 5-8', ...] # doctest: +SKIP
        >>> logger_name = 'Location 2B 314' # doctest: +SKIP
        >>> measurables_list = reader.list_measurables(logger_name) # doctest: +SKIP
        >>> measurables_list # doctest: +SKIP
        ['A1-H Stalas 1', 'A1-H', 'A1-T Stalas 1', 'A1-T'] # doctest: +SKIP
        >>> measurable = 'A1-H Stalas 1' # doctest: +SKIP
        >>> from_date = datetime.datetime(2023,7,20) # doctest: +SKIP
        >>> to_date = datetime.datetime(2023,7,21) # doctest: +SKIP
        >>> times, values = reader.get_data(logger_name=logger_name, measurable=measurable, from_date=from_date, to_date=to_date) # doctest: +SKIP    
    """

    def __init__(self, loggs_dir: str):
        self.loggs_dir = loggs_dir
    
    def list_loggers(self) -> List[str]:
        """  
        Collects names of available loggers

        Returns:
            A list of Logger names       
        """
        loggers_names_list = []
        for logger_name in os.listdir(self.loggs_dir):
            logger_name_path = os.path.join(self.loggs_dir, logger_name)
            if not os.path.isdir(logger_name_path):
                continue
            for year_month in os.listdir(logger_name_path):
                year_month_path = os.path.join(logger_name_path, year_month)
                if not os.path.isdir(year_month_path):
                    continue

                for day in os.listdir(year_month_path):
                    if not day.isdigit():
                        continue
                    day_path = os.path.join(year_month_path, day)
                    if not os.path.isdir(day_path):
                        continue

                    for file in os.listdir(day_path):
                        if not file.endswith(".txt"):
                            continue
                        file_path = os.path.join(day_path, file)

                        with open(file_path, "r") as f:
                            content = f.read()
                            lines = content.split("\n")
                            if len(lines) <= 0:
                                continue

                            first_line = lines[0]
                            columns = first_line.split(",")
                            if len(columns) == 3:
                                valid_file_found = True  
                            if logger_name_path not in loggers_names_list:
                                loggers_names_list.append(os.path.basename(logger_name_path))
                                break  
                    break   
                break    
            
        return loggers_names_list                                       
    
    def list_measurables(self, logger_name: str) -> List[str]:
        """  
        Collects names of measurables of a given logger
        
        Args:
            logger_name (str): Logger name  

        Returns:
            A list of measurables that can be found for the specific logger 
        """
        measurables = []
        logger_name_path = os.path.join(self.loggs_dir, logger_name)
        if not os.path.isdir(logger_name_path):
            raise ValueError('Folder name is not valid')
        
        f = glob.glob(f'{self.loggs_dir}/{logger_name}/**/*.txt', recursive = True)
        for measurable_path in f:
            measurable = os.path.splitext(os.path.basename(measurable_path))[0]
            if measurable not in measurables:
                measurables.append(measurable)
        return measurables

    def get_data(self, logger_name: str, measurable: str, from_date: datetime.datetime=None, to_date: datetime.datetime=None):
        """
        Function checks if given `logger_name` and `measurable` are valid and collects timestamps and values for a given time period.

        Args:
            logger_name (str): Logger name, for example: "Location 2B 314"
            measurable (str): Measurable name, for example: "A1-H Stalas 1"
            from_date (datetime.datetime): Date from which the data will be collected
            to_date (datetime.datetime): Date to which the data will be collected

        Returns:
            times (List (datetime.datetime)): A list with timestamps
            values (List (float)): A list with the values
        """
        
        output_list = []

        logger_name_path = os.path.join(self.loggs_dir, logger_name)
        if not os.path.isdir(logger_name_path):
            raise ValueError('Folder name is not valid')

        try:
            # Determine the earliest and oldest days available in the log
            earliest_year_month = min(os.listdir(logger_name_path))
            earliest_year_month_path = os.path.join(logger_name_path,
                                                    earliest_year_month)
            earliest_date = datetime.datetime.\
                strptime(f'{earliest_year_month}', '%Y-%m').\
                    replace(day=int(min([val for val in os.listdir(earliest_year_month_path) if val.isdigit()])))

            latest_year_month = max(os.listdir(logger_name_path))
            latest_year_month_path = os.path.join(logger_name_path,
                                                    latest_year_month)
            latest_date = datetime.datetime.\
                strptime(f'{latest_year_month}', '%Y-%m').\
                    replace(day=int(max([val for val in os.listdir(latest_year_month_path) if val.isdigit()])))

        except Exception as excpt:
            print("Could not determine earliest and latest available datapoints")
            print(excpt)
            earliest_date = None
            latest_date = None

        if from_date is None:
            from_date = earliest_date

        if to_date is None:
            to_date = latest_date

        if from_date is None or to_date is None:
            raise ValueError("From and to dates not specified")

        if from_date.hour != 0 or to_date.hour != 0:
            print("Log parsing time range granularity is by day, hours are ingored")

        for year_month in os.listdir(logger_name_path):
            year_month_path = os.path.join(logger_name_path, year_month)
            if not os.path.isdir(year_month_path):
                continue

            year_month_date = datetime.datetime.strptime(f'{year_month}', '%Y-%m')
            
            from_month_number = from_date.month
            from_year_number = to_date.year
            from_year_month_date = datetime.datetime.strptime(f'{from_year_number}-{from_month_number}', '%Y-%m')
            
            to_month_number = to_date.month
            to_year_number = to_date.year
            to_year_month_date = datetime.datetime.strptime(f'{to_year_number}-{to_month_number}', '%Y-%m')
            if not (year_month_date >= from_year_month_date and year_month_date <= to_year_month_date):
                continue

            for day in os.listdir(year_month_path):
                if not day.isdigit():
                    continue
                day_path = os.path.join(year_month_path, day)
                if not os.path.isdir(day_path):
                    continue
                
                folder_date = datetime.datetime.strptime(f'{year_month}-{day}', '%Y-%m-%d')
                if not (folder_date >= from_date and folder_date <= to_date):
                    continue

                file_path = os.path.join(day_path, measurable + ".txt")
                if not os.path.isfile(file_path):
                    raise ValueError('Measurable name is not valid')
                with open(file_path, "r") as f:
                    for line in f:
                        columns = line.strip().split(',')
                        if len(columns) >= 3:
                            date_coloumn = datetime.datetime.strptime(columns[0], '%Y-%m-%d %H:%M:%S.%f')
                            value_coloumn = float(columns[2])
                            output_list.append((date_coloumn, value_coloumn))
        
        sorted_output = sorted(output_list, key=lambda x: x[0])
        sorted_output_times = [column[0] for column in sorted_output]
        sorted_output_values = [column[1] for column in sorted_output]

        return (sorted_output_times, sorted_output_values)