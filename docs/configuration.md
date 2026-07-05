# Configuration

The EEG Open Door BCI Demo uses a JSON configuration file to define the main runtime parameters.

Default configuration file:

```text
configs/demo_eeg.json
```

The script can be executed using the default configuration:

```powershell
python scripts\run_eeg_open_door_demo.py
```

or with an explicit configuration path:

```powershell
python scripts\run_eeg_open_door_demo.py --config configs\demo_eeg.json
```

## Configuration sections

The configuration file is organized into the following sections:

```json
{
  "board": {},
  "display": {},
  "eeg": {},
  "stages": []
}
```

## Board parameters

```json
"board": {
  "wifi_connection": true,
  "stream_buffer_size": 45000
}
```

### `wifi_connection`

Defines whether the MindRove board uses WiFi communication.

Recommended value:

```json
true
```

### `stream_buffer_size`

Defines the internal stream buffer size used when starting acquisition.

Example:

```json
45000
```

## Display parameters

```json
"display": {
  "fullscreen": true,
  "user_screen_index": 0,
  "public_screen_index": 1
}
```

### `fullscreen`

Defines whether the windows open in fullscreen mode.

Recommended for public demos:

```json
true
```

### `user_screen_index`

Screen index used for the user-facing instruction window.

Typical value:

```json
0
```

### `public_screen_index`

Screen index used for the public EEG visualization window.

Typical value:

```json
1
```

If the windows appear on the wrong monitors, swap these values.

## EEG parameters

```json
"eeg": {
  "n_visual_channels": 6,
  "plot_window_sec": 5.0,
  "score_window_sec": 2.0,
  "public_update_interval_sec": 0.1
}
```

### `n_visual_channels`

Number of EEG channels displayed in the public visualization window.

Typical value:

```json
6
```

### `plot_window_sec`

Time window shown in the EEG plots.

Example:

```json
5.0
```

### `score_window_sec`

Time window used to compute the EEG-derived scores.

Example:

```json
2.0
```

### `public_update_interval_sec`

Time interval between updates of the public visualization.

Example:

```json
0.1
```

This corresponds approximately to a 10 Hz visual update rate.

## Stage parameters

The `stages` section defines the demo sequence.

Each stage includes:

```json
{
  "name": "REST",
  "title": "REPOSO",
  "instruction": "Quédate quieto.\nParpadea normal.\nMira al centro.",
  "duration": 10
}
```

### `name`

Internal stage identifier.

Examples:

```text
REST
CALMA
ENFOQUE
ESTRES
```

### `title`

Title displayed in the user-facing window.

### `instruction`

Instructions displayed to the user.

Line breaks can be inserted with:

```text
\n
```

### `duration`

Stage duration in seconds.

## Local configurations

Personal or machine-specific configurations should not be committed.

Use filenames such as:

```text
configs/lab_pc.local.json
configs/my_laptop.local.json
```

These files are ignored by Git through:

```gitignore
configs/*.local.json
```

## Recommended practice

Keep `configs/demo_eeg.json` as a clean public example and create local configuration files for specific computers, monitors, or hardware setups.
