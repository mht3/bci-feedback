'''
Pseudocode
------
Create a folder for participant with 3 folders; 1 for each LED

Run through 5 trials

For each trial 

    5 second rest
    5 second DAQ for LED1
    Add csv file to LED 1 folder using time%40==10 algorithm

    5 seconds rest
    5 second DAQ for LED 2
    Add csv file to LED 2 folder using time%40==20 algorithm

    5 seconds rest
    5 second DAQ for LED 3
    Add csv file to LED 3 folder using time%40==30 algorithm

    sleep for 10 seconds

Total time should be 3:20 seconds for the experiment
'''

import time
import argparse
import os
from brainflow.board_shim import BoardShim, BrainFlowInputParams

def get_data(daq_time, filename):
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
    time.sleep(daq_time)    
    board.stop_stream()
    board.release_session()

def main():

    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--person-number', type=str, help='person number', required=True, default='')
    args = parser.parse_args()

    num_trials = 5
    num_leds = 3
    trial_break_time = 10
    daq_time = 5
    cycle_break_time = 5
    person = args.person_number

    '''
    time%40 algorithm for storing to a respective LED file comes fromthe time per trial + trial rest time
    '''
    # Might not need this since we are using a for loop
    mod_number = (cycle_break_time + daq_time)*num_leds + trial_break_time

    print("Starting Experiment")
    for i in range(num_trials):
        print("Trial ", i+1)

        # Creates the directory for csv files
        directory = "Experiment_Data/Person" + str(person) + "/Trial" + str(i+1)
        os.makedirs(directory)

        for j in range(1, num_leds+1):
            # DAQ LED 1
            print("Get ready for LED ", j)
            time.sleep(cycle_break_time)
            print("Look at LED ", j)

            # 5 Second DAQ Here (takes 5 seconds)
            # Create the csv file
            file = directory + "/LED" + str(j) + ".csv"
            open(file, "w")
            filename = "file://" + file + ":w"
            get_data(daq_time, filename)

            print("LED {} Data -> csv\n".format(j))

        time.sleep(trial_break_time)

    print("Done")
    end = time.time()

    print("Time to run:")
    print(end - start)

if __name__ == "__main__":
    main()