# Welcome furhatos-sama's home!

## Short description 
Hi there!
This repository contains the bits and bytes that make fuhatos-sama work. 

Furhatos-sama is a virtual interactive research assistant developed using the [Furhat SDK](https://furhat.io/). This is a small project conceptualized by [Raghavendra](mr-envyr.github.io) to demonstrate a tiny subset of possibilities of intelligent assistants.

## Setup and Usage
To use the code, you'll need to setup a few things. Following is an outline of the steps you can follow to run the code in your own PC. Ensure that your PC meets the minimum requirements to run the Furhat SDK.

### Requirements:
- Python: 3.11.5
- Exa AI library: 1.7.2
- HuggingFace Hub: 0.28.1
- Furhat Remote-API: 1.0.2
- Furhat SDK: 2.8.0

### Steps to setup the requirements
1. Install Python either [directly](https://www.python.org/downloads/) or by downloading and installing [Anaconda](https://www.anaconda.com/).
2. Create a [virtual environment](https://virtualenv.pypa.io/en/latest/) and activate it.
3. Once it is activated, run `pip install exa-py==1.7.2 huggingface_hub: 0.28.1 furhat-remote-api`
4. Install the Furhat SDK by following [this page](https://www.furhatrobotics.com/requestsdk).
5. Obtain your [HuggingFace API token](https://huggingface.co/docs/hub/security-tokens) and [Exa AI API key](https://dashboard.exa.ai/api-keys) using the respective links.
6. Create a file named `_keys.json` with the following format in the root folder containing the code and paste your keys in the suitable quotes in the file. 
``` 
{
    "EXA_KEY": "KEY HERE",
    "HF_KEY": "KEY HERE"
} 
``` 

### Running the code
1. Once everything is setup, start the Furhat Desktop Launcher and start the remote skill.
2. Navigate to the folder containing the code and `.json` file with the keys and fire up a terminal.
3. Activate your python environment inside the terminal and run `python furhat_interact.py`.
4. Interact and let me know how it goes!

## Demonstration
A short video demonstration of the final prototype can be found [here](https://youtu.be/TrYep9gGgWQ).

