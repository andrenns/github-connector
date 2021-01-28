import os
import pandas as pd
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.utils import constants
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.visualization.petrinet import visualizer as pn_visualizer


def run_inductive_miner():
    log_csv = pd.read_csv('results-processDiscovery.csv', sep=',')
    log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
    log_csv = log_csv.sort_values('timestamp')
    parameters = {constants.PARAMETER_CONSTANT_CASEID_KEY: "issue",
                  constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "newValue",
                  constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "timestamp"}
    event_log = log_converter.apply(log_csv, parameters=parameters)

    net, initial_marking, final_marking = inductive_miner.apply(event_log, parameters=parameters)
    parameters = {pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"}
    gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters)
    pn_visualizer.save(gviz, "alpha.svg")
