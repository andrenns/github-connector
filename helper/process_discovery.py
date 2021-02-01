import pandas as pd
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.utils import constants
from pm4py.visualization.petrinet import visualizer as pn_visualizer
from helper.arango import get_stored_data, save_analysis_results
import csv
from datetime import datetime
from helper.env_reader import ENV


def list_to_csv():
    data = get_stored_data()
    keys = data[0].keys()
    current_date_time = datetime.now().strftime('%m-%d-%YT%H:%m:%s')
    file_absolute_path = ENV['STORED_DATA_PATH'] + '/' + ENV['STORED_DATA_NAME'] + current_date_time + '.csv'
    with open(file_absolute_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    return [file_absolute_path, current_date_time]


def run_inductive_miner():
    file_absolute_path, current_date_time = list_to_csv()
    log_csv = pd.read_csv(file_absolute_path, sep=',')
    log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
    log_csv = log_csv.sort_values('timestamp')
    parameters = {constants.PARAMETER_CONSTANT_CASEID_KEY: "issue_id",
                  constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "old_value",
                  constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "timestamp"}
    event_log = log_converter.apply(log_csv, parameters=parameters)

    net, initial_marking, final_marking = inductive_miner.apply(event_log, parameters=parameters)
    parameters = {pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"}
    gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters)
    save_absolute_path = ENV['ANALYSIS_PATH'] + '/' + ENV['ANALYSIS_NAME'] + current_date_time + '.svg'
    pn_visualizer.save(gviz, save_absolute_path)
    data_used_file_name = ENV['STORED_DATA_NAME'] + current_date_time + '.csv'
    analysis_result_file_name = ENV['ANALYSIS_NAME'] + current_date_time + '.svg'
    save_analysis_results(data_used_file_name, analysis_result_file_name, current_date_time)
