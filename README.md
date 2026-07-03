\# EEG Open Door BCI Demo



Real-time EEG demonstration for open-door and outreach activities using a MindRove EEG device, PyQt5 graphical interfaces, and simple EEG-derived state scores.



\## Overview



This repository contains a real-time EEG-based demonstration designed for public presentations. The system acquires EEG signals from a MindRove device through WiFi and displays two graphical interfaces:



\* A \*\*user-facing window\*\* with instructions and cognitive/relaxation tasks.

\* A \*\*public-facing window\*\* with EEG signals, state scores, blink detection, signal quality estimation, and a simple visual feedback element.



The current version is intended as a functional demo for showing basic concepts of brain-computer interfaces, EEG visualization, and real-time biomedical signal processing.



\## Main Features



\* Real-time EEG acquisition using MindRove WiFi.

\* Multi-channel EEG visualization.

\* Simple EEG score estimation:



&#x20; \* Calm state based on alpha/beta ratio.

&#x20; \* Activation state based on beta activity.

&#x20; \* Blink detection using peak amplitude.

&#x20; \* Signal quality heuristic based on standard deviation.

\* Dual-screen interface for user instructions and public visualization.

\* Interactive task stages for demonstration purposes.



\## Demo Stages



The current demo includes four stages:



1\. \*\*REST\*\*

&#x20;  The user remains still and looks at the center of the screen.



2\. \*\*CALM / BREATHING\*\*

&#x20;  The user follows a slow breathing animation.



3\. \*\*FOCUS / STROOP\*\*

&#x20;  The user performs a Stroop-style cognitive task.



4\. \*\*STRESS / RAPID COUNTING\*\*

&#x20;  The user counts backwards quickly in steps of seven.



\## Repository Structure



```text

eeg-open-door-bci/

│

├── scripts/

│   └── run\_eeg\_open\_door\_demo.py

│

├── configs/

│

├── docs/

│

├── assets/

│   └── figures/

│

├── requirements.txt

├── .gitignore

└── README.md

```



\## Main Script



Run the current demo with:



```bash

python scripts/run\_eeg\_open\_door\_demo.py

```



\## Requirements



Install the Python dependencies with:



```bash

pip install -r requirements.txt

```



The MindRove SDK/package must be installed separately according to the device setup.



\## Hardware



\* MindRove EEG device.

\* Computer with WiFi connection.

\* Optional second monitor for separating the public and user interfaces.



\## Notes



This repository contains an initial functional version of the EEG open-door demo. Future versions may include:



\* Configuration files for experiment parameters.

\* A demo mode without EEG hardware.

\* Modular code organization.

\* Improved documentation.

\* Example screenshots and diagrams.

\* More robust EEG preprocessing and state estimation.



\## Status



Initial functional demo version.



