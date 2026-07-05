# Testing Checklist

Use this checklist before running the EEG Open Door BCI Demo in a public or laboratory setting.

## 1. Repository and environment

- [ ] The repository is cloned or updated.
- [ ] The correct Python virtual environment is activated.
- [ ] Dependencies were installed with:

```powershell
pip install -r requirements.txt
```

- [ ] The MindRove SDK/package is installed.
- [ ] The script is executed from the repository root or with an explicit config path.

## 2. Configuration

- [ ] The configuration file exists:

```text
configs/demo_eeg.json
```

- [ ] `user_screen_index` is correct.
- [ ] `public_screen_index` is correct.
- [ ] `fullscreen` is correctly configured.
- [ ] `n_visual_channels` matches the intended visualization.
- [ ] Stage durations are appropriate for the demo.

## 3. Display setup

- [ ] Two monitors are connected if dual-screen mode is required.
- [ ] Windows display mode is set to Extend:

```text
Win + P -> Extend
```

- [ ] The user-facing window appears on the intended screen.
- [ ] The public-facing EEG window appears on the intended screen.

## 4. Hardware

- [ ] The MindRove device is charged.
- [ ] The MindRove device is turned on.
- [ ] The computer is connected to the correct WiFi/device network.
- [ ] The EEG electrodes are placed correctly.
- [ ] Electrode contact is stable.

## 5. Execution

Run:

```powershell
python scripts\run_eeg_open_door_demo.py
```

Or:

```powershell
python scripts\run_eeg_open_door_demo.py --config configs\demo_eeg.json
```

Confirm:

- [ ] The application starts without errors.
- [ ] The instruction window opens.
- [ ] The public visualization window opens.
- [ ] EEG traces are visible.
- [ ] Scores update in real time.
- [ ] Blink detection reacts to strong blink artifacts.
- [ ] The Next and Previous buttons change stages.

## 6. Public demonstration

Before presenting:

- [ ] Test the full stage sequence.
- [ ] Verify that the audience-facing screen is readable.
- [ ] Verify that the user instructions are readable.
- [ ] Confirm that the EEG traces are visually stable.
- [ ] Confirm that no private files, user data, or personal paths are displayed.
- [ ] Have a backup explanation ready in case the hardware connection fails.

## 7. After the demo

- [ ] Stop the application safely.
- [ ] Turn off or disconnect the device.
- [ ] Do not commit generated data or local configuration files.
- [ ] Check `git status` before committing any changes.
