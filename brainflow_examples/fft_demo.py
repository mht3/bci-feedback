import argparse
import time
import brainflow
import numpy as np
from matplotlib import pyplot as plt

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions
import plot_fft

def main():
    BoardShim.enable_dev_board_logger()

    # use synthetic board for defaullt
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=False,default=-1)

    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.serial_port = args.serial_port
    board_id = args.board_id
    sampling_rate = BoardShim.get_sampling_rate(board_id)
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(10)
    data = board.get_current_board_data(DataFilter.get_nearest_power_of_two(sampling_rate))
    board.stop_stream()
    board.release_session()

    eeg_channels = BoardShim.get_eeg_channels(board_id)



    # demo for transforms
    fft_data = []
    for count, channel in enumerate(eeg_channels):
        # print('Original data for channel %d:' % channel)
        # print(data[channel])
    
        # demo for fft, len of data must be a power of 2
        fft_data_c = DataFilter.perform_fft(data[channel], WindowFunctions.NO_WINDOW.value)
        fft_data.append(fft_data_c)
        # print('channel %d:' % channel)
        # print(fft_data_c)

    plot_fft.plot_fft_data(fft_data)
if __name__ == "__main__":
    main()