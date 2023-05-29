# Onboard

Welcome to the team! We're excited to have you onboard for this semester and hopefully beyond. This file should give a nice intro to what our human-machine teaming (HMT) research group is doing with OpenBCI and also how to get everything set up. By the end of this tutorial you should be able to collect data using our EEG headset.

## Background

Our OpenBCI project began in summer 2021 and started with a driving question: How can we use a brain computer interface to improve reinforcement learning algorithms?

- [Here](https://docs.google.com/presentation/d/1sMLpdJm1mx1yXpkU7T3wM_N2oY4K5vgJkq-RaVjhDls/edit?usp=sharing) is a link to our phase 1 presentation at the end of the 2021 summer. This was before we assembled the headset and contains some background information on OpenBCI as well as summaries of important research papers that utilized it.

- [Here](https://docs.google.com/presentation/d/1IzRpEpWFFlqtfDbAe5gzxEzJ8An5t3B8egbdIZ9fJbE/edit?usp=sharing) is a link to a summary of our fall 2021 progress. These should get you up to speed on all the background knowledge you need to get coding and collecting data!

## Environment Setup

Our code requires many, many packages and trying to download all at once can be a headache. This is exactly why we use Conda. If you haven't heard of it, no worries. In short, it's just a package manager that allows everyone to work with the same versions of imports. If you're curious, checkout the file ```environment.yml``` which contains a list of all the packages we use.

### Installing Git

You may or may not already have Git installed on your computer. If you've already done this, feel free to move on to the next step. Git essentially allows you to use terminal or command line to interface with a GitHub repository and do things such as clone, push, pull, and even create new branches. Our GitHub is where **everyone** can see your work, but Git looks at **your local** changes and allows you to push them up to the shared repository.

Follow the instructions [here](https://git-scm.com/downloads) to install Git. Git-SCM provides some great instructions for both MacOS and Windows, so make sure to click on the one for your computer. As always, if you run into any problems, don't hesitate to reach out to myself (Matt) or Rupal.

If you're using a windows computer, the git download above comes with a nice CLI called Git Bash. This is what I use as my command line instead of the gross windows command line. :)

If you're using a Mac, I would suggest to just use the built in Terminal instead of Git Bash.

### Installing Conda

Run the following command on terminal or git bash to see if you have conda already installed.

```
conda update -n base conda
```

If conda is not installed, I would recommend installing [anaconda](https://www.anaconda.com/products/individual). This is what I prefer, however there are also other alternatives such as [miniconda](https://docs.conda.io/en/latest/miniconda.html) that also work. Slightly more detailed instructions for [windows](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) or [MacOS](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html) are also available to you.

Make sure when following the instructions to click yes to **add to path**. I've run into many bugs solely because I did not have conda added to my path so beware!

Before we move forward, let's just double check that everything is working as intended. MacOS terminal works well after installing conda with the instructions above, however if you're using git bash on windows, you may have to follow further instructions to get conda working (I know ugh).

In the command line/terminal, type 

```
conda list
```

This should work with MacOS and if it does you can move on to the next section.

Git bash probably will throw an error such as ```conda: command not found```. One thing you have to do is add a conda shell script to your /.bashrc. All this does is tell Git Bash to initialize conda, automatically giving you the conda command. Follow [these](https://discuss.codecademy.com/t/setting-up-conda-in-git-bash/534473) instructions to get this done.  

### Cloning the Repo 

The goal here is to get a local copy of our GitHub repo onto your computer.

First, change directories to a location that you want to have the research files in. For example, if you have a research folder in documents, you could do

```
cd documents/research
```

Next clone the repo with our special link. This should make a folder called ```bci-feedback``` wherever your current directory is, so make sure it does that.

```
git clone https://github.com/Tran-Research-Group/bci-feedback.git
```

Change directories again into the ```bci-feedback``` folder and run a quick ```ls``` to see if everything is as expected.

```
cd bci-feedback/
ls
```

Great! Let's move on to installing all of our packages with conda.

### Installing Packages with conda

Type the following to create an environment called OpenBCI. This command does a lot behind the scenes, but just know it's downloading all the packages you need and putting it into our environment. It should take a LONG time to run.

```
conda env create -f environment.yml
```

Check if the environment is added

```
conda env list
```

You should see your base environment and a new one called OpenBCI. It's important to note that by default you are always on your base environment. Before doing any work, switch to our environment with this command:

```
conda activate OpenBCI
```

Finally, you've  gotten everything you need to get started with our research. Don't worry too much about the steps above. These are just one time things. All you need to do now is activate the OpenBCI environment before doing any coding. Great Work!!!

Now you can run our current python scripts and make new ones.

For example, you should be able to run the code that got us 99% accuracy on our SSVEP experiment. Assuming you're in the bci-feedback directory, run

```
python ML_Models/real_ssvep_experiment.py
```

This should output the classification accuracy as well as the confusion matrix you've seen in the slides from the fall semester.

## OpenBCI GUI

Follow the tutorial [here](https://docs.openbci.com/Software/OpenBCISoftware/GUIDocs/) for installing the OpenBCI GUI ([download here](https://openbci.com/downloads)). Unfortunately, the GUI is not yet notarized, so I ran into many issues with my computer not allowing the GUI to open. Follow the instructions as best as you can, and if you can't get the GUI to open, reach out to me over slack and I'd be happy to help. (I would just recommend following the tutorial up to OpenBCI's [help video](https://docs.openbci.com/Software/OpenBCISoftware/GUIDocs/#tutorial).

One important thing to do that isn't clarified in their tutorial is to install a [VCP](https://ftdichip.com/drivers/vcp-drivers/) driver allowing the cyton board to connect to your computer via USB. Just follow the link embedded in the VCP text and download the correct VCP for your machine. 

![image](https://user-images.githubusercontent.com/60635839/153344958-49a129f4-7392-4792-902f-8d5391e24f7d.png)

Creating a folder on my desktop worked best for me. Inside that folder I also had another called ```vcp_driver```, where I put the VCP files. The main GUI is a .exe file called ```OpenBCI_GUI```. If you click on this, the GUI should pop up within 10 seconds. If after waiting a while no GUI opens, reach out to me and I can try my best to help.

Plug the CYTON dongle into your computer, put the headset on, and you're ready to begin!

### GUI Navigation Steps

- Click on CYTON

![image](https://user-images.githubusercontent.com/60635839/153347466-06bec1ed-bc95-4334-8e47-bb3d272fef10.png)


- Find the Serial Port that Cyton is connected to and select it. Press 8 channels and click start session

![image](https://user-images.githubusercontent.com/60635839/153347515-66224f92-80bc-4fd1-938c-5417c177a26d.png)

- Click on Start Data Stream

![image](https://user-images.githubusercontent.com/60635839/153347589-d5e6c376-4364-4430-a562-30b82c3236b4.png)

- You should see something like this with live data! Press stop data stream whenever you’re done. While the GUI is running, you should be able to see which electrodes are mounted in the Time Series section. If an electrode isn't positioned correctly on your head, the GUI will outline a channel in red and say that it needs to be adjusted.

![image](https://user-images.githubusercontent.com/60635839/153347548-187aeac1-0c82-4bc9-9902-e71d24b4157c.png)



## BrainFlow Library

[BrainFlow](https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference) is a great open-source package funded by OpenBCI. One important thing to note is that BrainFlow is a board agnostic package. What I mean by that is that it can work with several different boards. Not only does it work with our Cyton board, it also works with the Ganglion and other BCI's that were created by companies other than OpenBCI. To get started, you should see a folder called ```brainflow_examples/```. This folder contains examples I've pulled from documentation and tweaked slightly for our needs. 

Take a look at the file called ```get_data.py```. This is an example of board agnostic code. The first import you should see is something called argparse. Argparse allows you to put in extra arguments in the command line when running a program. This allows us to specify which board and serial port we're using. Run the following command to collect synthetic data for 5 seconds.

```
python brainflow_examples/get_data.py --log --board-id -1
```

Notice that the only argument you needed was a board-id of -1. No serial port was needed! Why is that? This is because OpenBCI has the option to run fake data without the use of a headset. It has no purpose other that allowing yourself to get familiar with the program without having to use the OpenBCI headset.

If you want to use the Cyton board with the OpenBCI headset, type

```
python brainflow_examples/get_data.py --log --board-id 0 --serial-port COM3
```

As you can see here the board id has changed from -1 to 0. By default, 0 is a variable representing our Cyton board, while -1 is a variable to represent the synthetic board. You've also probably noticed that there is another argument called serial port. When using the cyton board, you need to put in your serial port in order for BrainFlow to connect to the board. For MacOS and Windows, this is usually COM3 by default.

Adding in arguments every time is a lot of work, right? Especially when we know that we're using the Cyton board. Let's look at an example where we don't need all of these arguments. Look at ```cyton_get_data.py```. This file sets argparse defaults specifically for our board so that we don't have to go through the headache of adding different arguments each time we run the code.

Make sure you understand how we do this in the code. Here is a code snippet from that file. As you can see, I made a global variable called CYTON_BOARD_ID. Also look at some other defaults listed below. By defualt, the serial port is COM3 so there is no need to type that every time. The second argument you see is called streamer-params. This is where you can pick a file to save the data to. By default, it saves the data in ```brainflow_examples/data/cyton_data.csv```.

```
CYTON_BOARD_ID = 0
BoardShim.enable_dev_board_logger()

parser = argparse.ArgumentParser()
parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='COM3')
parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default="file://brainflow_examples/data/cyton_data.csv:w")
args = parser.parse_args()

params = BrainFlowInputParams()
params.serial_port = args.serial_port
board = BoardShim(CYTON_BOARD_ID, params)
```

## Conclusion

Great! That concludes our tutorial on getting started with OpenBCI. You should now have all the tools you need for collecting data and using OpenBCI with the BrainFlow library. Feel free to make new python files for your data collection needs. Please don't hesitate to reach out if you have any questions. 

Best of luck,

Matt

