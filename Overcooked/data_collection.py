import time
import argparse
import os
from brainflow.board_shim import BoardShim, BrainFlowInputParams

def get_data(filename, gametype, collection_time=30):
    ''' 
    Collects EEG data in 30 second intervals by default for each type of game played. 
    
    Parameters
    ----
    filename        :   name of the file to store data into
    gametype        :   type of game. Choose from assymetric_advantages, coordination_ring,
                        counter_circuit, cramped_room, or forced_coordination
    collection_time :   seconds to collect data for
    '''
    CYTON_BOARD_ID = 0
    BoardShim.enable_dev_board_logger()

    params = BrainFlowInputParams()
    params.serial_port = 'COM3'
    board = BoardShim(CYTON_BOARD_ID, params)

    board.prepare_session()

    # Write stream file to the csv file filename.
    # Sample size is arbitrary because we stop data aquisition after daq_time seconnds
    board.start_stream(45000, filename) 

    # Get daq_time seconds of data
    time.sleep(collection_time)    
    board.stop_stream()
    board.release_session()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--gametype', type=str, help='Choose type of overcooked game', required=True, default='cramped_room')
    parser.add_argument('--trial', type=str, help='current trial in game', required=True, default='1')

    args = parser.parse_args()

    gametype = args.gametype
    trial = "trial_" + args.trial
    directory = "file://Overcooked/data/"
    filename = directory + gametype + "/" + trial + ".csv:w"

    get_data(filename, gametype)
    print("Successfully converted {} trial {} to csv.".format(gametype, args.trial))
    
if __name__ == "__main__":
    main()