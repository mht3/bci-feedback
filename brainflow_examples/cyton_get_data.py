import argparse
import time
import numpy as np

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

def main():
    CYTON_BOARD_ID = 0
    BoardShim.enable_dev_board_logger()

    # Option for entering alternative serial port. Default is "COM3" a "dev/tty..." port may be needed for linux.
    # TODO: Add more arguments if necessary
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='COM3')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default="file://brainflow_examples/data/cyton_data.csv:w")
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.serial_port = args.serial_port
    board = BoardShim(CYTON_BOARD_ID, params)

    board.prepare_session()

    # Write stream file to the data folder and call it cyton_data.csv
    # TODO: What should our sample size be
    board.start_stream(45000, args.streamer_params) #"data/cyton_data.csv")

    # Get 10 seconds of data
    time.sleep(10)    
    data = board.get_board_data()  # get all data and remove it from internal buffer
    board.stop_stream()
    board.release_session()

    print("Data Shape: ", data.shape)
    print(data)


if __name__ == "__main__":
    main()