# Troubleshooting

This document lists common issues and possible solutions for the EEG Open Door BCI Demo.

## The script cannot find the configuration file

Error example:

```text
Configuration file not found
```

Possible solutions:

1. Run the script from the repository root:

```powershell
cd C:\GitHub\eeg-open-door-bci
python scripts\run_eeg_open_door_demo.py
```

2. Or pass the configuration path explicitly:

```powershell
python scripts\run_eeg_open_door_demo.py --config configs\demo_eeg.json
```

3. Check that the file exists:

```text
configs/demo_eeg.json
```

## Only one screen is detected

Possible causes:

- The second monitor is not connected.
- Windows is using Duplicate mode instead of Extend mode.
- The display was connected after launching the application.

Possible solutions:

1. Set Windows to Extend mode:

```text
Win + P -> Extend
```

2. Close and restart the Python script.

3. Verify the detected screens printed in the terminal.

## Both windows appear on the same screen

Possible causes:

- Windows only detects one screen.
- `user_screen_index` and `public_screen_index` point to the same display.
- The monitor order is different from the expected setup.

Possible solutions:

1. Open:

```text
configs/demo_eeg.json
```

2. Swap:

```json
"user_screen_index": 0,
"public_screen_index": 1
```

to:

```json
"user_screen_index": 1,
"public_screen_index": 0
```

3. Restart the script.

## MindRove connection fails

Possible causes:

- MindRove device is turned off.
- The device is not charged.
- The computer is not connected to the correct WiFi/device network.
- The MindRove SDK/package is not correctly installed.
- Another process is already using the device.

Possible solutions:

1. Turn the MindRove device off and on again.
2. Check WiFi/device connection.
3. Restart the Python script.
4. Close other programs that may be using the device.
5. Verify the MindRove SDK installation.

## PyQt5 import error

Error example:

```text
ModuleNotFoundError: No module named 'PyQt5'
```

Solution:

```powershell
pip install -r requirements.txt
```

Make sure the correct virtual environment is activated.

## pyqtgraph import error

Error example:

```text
ModuleNotFoundError: No module named 'pyqtgraph'
```

Solution:

```powershell
pip install -r requirements.txt
```

## mindrove import error

Error example:

```text
ModuleNotFoundError: No module named 'mindrove'
```

Possible solutions:

1. Activate the virtual environment where MindRove is installed.
2. Install the MindRove SDK/package according to the device setup.
3. Verify that the package is available:

```powershell
python -c "import mindrove; print('MindRove import OK')"
```

## EEG traces look flat

Possible causes:

- Poor electrode contact.
- Incorrect device placement.
- Device not streaming correctly.
- Very low signal amplitude.
- Wrong channel mapping.

Possible solutions:

1. Check electrode contact.
2. Adjust the EEG device.
3. Restart acquisition.
4. Verify that the board is streaming data.
5. Check the selected EEG channels.

## EEG traces look saturated or unstable

Possible causes:

- Motion artifacts.
- Poor electrode contact.
- Excessive blinking or facial movement.
- Unstable wireless connection.

Possible solutions:

1. Ask the user to stay still.
2. Improve electrode contact.
3. Reduce cable/device movement.
4. Restart the device if needed.

## The interface freezes or updates slowly

Possible causes:

- Very high visualization load.
- Computer performance limitations.
- Too many channels plotted.
- Update interval too low.

Possible solutions:

1. Reduce:

```json
"n_visual_channels": 6
```

2. Increase:

```json
"public_update_interval_sec": 0.1
```

3. Close unnecessary applications.

## Git shows unexpected files

Before committing, always run:

```powershell
git status
```

Do not commit:

- virtual environments,
- raw data,
- generated outputs,
- local configuration files,
- `__pycache__`,
- personal paths,
- temporary files.

If an unwanted untracked file appears, inspect it first. If it is safe to remove:

```powershell
git clean -n
git clean -f
```
