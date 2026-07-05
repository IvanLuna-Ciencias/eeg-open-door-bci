# Windows Setup

This document describes the basic setup required to run the EEG Open Door BCI Demo on Windows.

## 1. Clone the repository

```powershell
git clone https://github.com/YOUR_USERNAME/eeg-open-door-bci.git
cd eeg-open-door-bci
```

Replace `YOUR_USERNAME` with your GitHub username.

## 2. Create or activate a Python virtual environment

If you already have a working virtual environment with the required MindRove dependencies, you can activate it directly.

Example:

```powershell
& "C:\GitHub\your-existing-env\Scripts\Activate.ps1"
```

Alternatively, create a new virtual environment:

```powershell
python -m venv env310
.\env310\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

## 3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

## 4. Install MindRove dependencies

The MindRove SDK/package must be installed separately according to the official device setup.

This repository does not include the MindRove SDK itself.

## 5. Configure the demo

The default configuration file is:

```text
configs/demo_eeg.json
```

Before running the demo, check:

- `user_screen_index`
- `public_screen_index`
- `n_visual_channels`
- stage durations
- fullscreen mode

## 6. Run the demo

From the repository root:

```powershell
python scripts\run_eeg_open_door_demo.py
```

Or explicitly passing the configuration file:

```powershell
python scripts\run_eeg_open_door_demo.py --config configs\demo_eeg.json
```

## 7. Recommended display setup

For open-door demonstrations, use two screens in Windows Extend mode:

```text
Win + P -> Extend
```

Typical setup:

- Screen 0: user-facing instructions.
- Screen 1: public EEG visualization.

If the windows appear on the wrong screens, edit:

```text
configs/demo_eeg.json
```

and change:

```json
"user_screen_index": 0,
"public_screen_index": 1
```

## Notes

Do not commit virtual environments, personal configuration files, raw EEG data, generated outputs, or local hardware-specific files.
