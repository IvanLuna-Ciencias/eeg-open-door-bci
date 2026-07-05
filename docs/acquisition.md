# EEG Acquisition and Signal Scoring

This document summarizes the acquisition and real-time scoring approach used in the EEG Open Door BCI Demo.

## Hardware

The current version is designed for a MindRove EEG device using WiFi communication.

The board is initialized in the main script through the MindRove/BrainFlow-style API.

## Acquisition flow

The general acquisition flow is:

```text
MindRove EEG device
        |
        v
BoardShim acquisition
        |
        v
Current EEG buffer
        |
        v
Selected EEG channels
        |
        v
Real-time visualization and simple score estimation
```

## EEG channels

The script retrieves the available EEG channels from the board and selects the first channels for visualization.

The number of visualized channels is defined in:

```text
configs/demo_eeg.json
```

Parameter:

```json
"n_visual_channels": 6
```

## Visualization window

The public-facing window displays multi-channel EEG signals using `pyqtgraph`.

The plotted time window is defined by:

```json
"plot_window_sec": 5.0
```

## Score window

The score computation uses a shorter EEG segment defined by:

```json
"score_window_sec": 2.0
```

## Computed scores

The demo computes simple EEG-derived scores from one selected EEG channel.

These scores are intended for demonstration and visualization purposes, not for clinical diagnosis.

## Calm score

The calm score is based on the relative contribution of alpha activity with respect to alpha and beta activity:

```text
calm = alpha / (alpha + beta)
```

Higher values suggest stronger relative alpha contribution.

## Activation score

The activation score is based on the relative contribution of beta activity:

```text
act = beta / (alpha + beta)
```

Higher values suggest stronger relative beta contribution.

## Blink detection

Blink detection is estimated using a peak amplitude threshold.

If the absolute EEG amplitude exceeds the threshold, the blink flag is activated.

This is a simple heuristic intended for real-time demonstration.

## Signal quality

Signal quality is estimated using the standard deviation of the EEG segment.

Very low standard deviation may indicate poor contact or flat signal.

Very high standard deviation may indicate artifacts, saturation, or unstable acquisition.

## Important limitations

The current scoring approach is intentionally simple.

It is useful for:

- outreach demonstrations,
- visual explanation of EEG concepts,
- basic real-time signal visualization,
- public BCI demonstrations.

It is not intended as:

- a validated clinical EEG metric,
- a robust mental state classifier,
- a medical diagnostic tool,
- a replacement for calibrated BCI models.

## Future improvements

Possible improvements include:

- multi-channel score estimation,
- artifact rejection,
- adaptive thresholds,
- calibration per user,
- frequency band normalization,
- machine learning-based state classification,
- offline/online validation using labeled EEG recordings.
