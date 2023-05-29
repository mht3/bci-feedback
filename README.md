# bci-feedback

## Setting up the Environment

See ```onboard.md``` for more detailed instructions.

```
conda env create -f environment.yml
conda activate OpenBCI
```

## Code Structure
```bci-feedback/``` contains:

```ML_Models/```:

- ```real_ssvep_experiment.py```: Main SSVEP experiment with 3 flashing LED's at 2.5, 3, and 3.5 HZ.
- Contains many other python files, including unused CNN code from the Army Research Lab

```Overcooked/```:

- ```data/```: Location for EEG data with human-machine teaming trials of the game Overcooked. 
    The game was played online here: https://humancompatibleai.github.io/overcooked-demo/
- ```data_collection.py```: Code to collect EEG data for Overcooked trials in 30 second intervals.

```brainflow_examples/```:

- ```cyton_get_data_collection.py```: Sample code to collect data from the OpenBCI Cyton 8-channel board.
- Contains many other Python example files for EEG data collection along with views of FFT plots.

 
```DataCollection/```:

- ```experiment.py```: Contains code to get EEG data for the SSVEP LED experiment seen in ML_Models.

```Experiment_Data/```:

- Contains data from each participant of the SSVEP LED experiment.

## Additional Environment Notes

### Updating the Environment
```
conda env update --name OpenBCI --file environment.yml --prune
```

### Reverting to the original environment 

Good to use if a mistake was made when downloading packages that aren't yet on the environment.yml file. 
For example, installing Matplotlib with conda broke pyqt5 (which was installed with pip). One option is to uninstall all the contingencies with Matplotlib, but an easier option sometimes is just to revert to what's on the environment.yml file and reactivate the environment. 

```
conda deactivate
conda env remove -n OpenBCI
conda env create -f environment.yml
conda activate OpenBCI
```
