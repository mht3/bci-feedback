import argparse
import time
import numpy as np

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

'''
General (board agnostic) way to get data from any board in the brainflow library. 
This is directly from brainflow documentation.
See the github for how this can be used with the specific board,
however if the cyton board is being used, just use cyton_get_data.py.

For Cyton, run the following:
    python get_data.py --log --board-id 0 --serial-port COM3

For Synthetic, run the following:
    python get_data.py --log --board-id -1
'''
def main():
    BoardShim.enable_dev_board_logger()

    '''
    Neat command line option for additional arguments.
    This HAS to be done for the brainflow library to keep things board agnostic.
    The parser is sent into a BrainFlowInputParams structure to internally hold more info about the board.
    For more info on argparse see https://docs.python.org/3/library/argparse.html
    For more info on why this is important for Brainflow see https://brainflow.readthedocs.io/en/stable/UserAPI.html#user-api
    '''
    parser = argparse.ArgumentParser()

    '''
    The next parser.add_argument lines add additional arguments for the command line. For example, typing --serial-port COM3

    CYTON: Only needs --serial-port
            Windows: --serial-port COM3
            Linux: --serial-port dev/tty/...
            TODO: Add Linux port number once we get the computer running.

    SYNTHETIC: Default when no arguments arge given.
    '''
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='file://brainflow_examples/data/synthetic_data.csv:w')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')

    #Default board is synthetic board
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=True,default=-1)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    parser.add_argument('--log', action='store_true', required=False)

    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file

    if (args.log):
        BoardShim.enable_dev_board_logger()
    else:
        BoardShim.disable_board_logger()

    board = BoardShim(args.board_id, params)
    board.prepare_session()

    # board.start_stream () # use this for default options
    #first argument of start_stream is the number of samples
    board.start_stream(45000, args.streamer_params)
    time.sleep(5)

    # data = board.get_current_board_data (256) # get latest 256 packages or less, doesnt remove them from internal buffer
    
    data = board.get_board_data()  # get all data and remove it from internal buffer
    board.stop_stream()
    board.release_session()

    print(data)


if __name__ == "__main__":
    main()