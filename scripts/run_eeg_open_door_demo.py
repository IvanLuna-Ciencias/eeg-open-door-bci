import time
import random
import numpy as np

import json
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds
from mindrove.data_filter import DataFilter

def load_config(config_path: str):
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

# ----------------------------- Utils: simple EEG scores -----------------------------
def compute_scores_one_channel(x_uV: np.ndarray, srate: int):
    """
    Retorna calm(0..1), act(0..1), blink(0/1), quality(0..1)
    - calm: alpha/(alpha+beta)
    - act: beta/(alpha+beta)
    - blink: umbral de pico
    - quality: heurística por std
    """
    std = float(np.std(x_uV))
    if std < 1.0:
        quality = 0.2
    elif std < 3.0:
        quality = 0.6
    elif std > 200.0:
        quality = 0.3
    else:
        quality = 1.0

    blink = 1 if (np.max(np.abs(x_uV)) > 150.0) else 0

    calm = 0.5
    act = 0.5
    try:
        nfft = 256
        overlap = 128
        window = 3  # HANNING (en la mayoría de builds MindRove/BrainFlow-style)
        psd, freqs = DataFilter.get_psd_welch(x_uV, nfft, overlap, srate, window)
        alpha = DataFilter.get_band_power(psd, freqs, 8.0, 12.0)
        beta  = DataFilter.get_band_power(psd, freqs, 13.0, 30.0)
        eps = 1e-9
        calm = float(alpha / (alpha + beta + eps))
        act  = float(beta  / (alpha + beta + eps))
    except Exception:
        pass

    return calm, act, blink, quality


# ----------------------------- Stage definitions -----------------------------
STAGES = []

# ----------------------------- User Window (instructions/tests) -----------------------------
class UserWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BCI Usuario (Instrucciones)")
        self.setStyleSheet("background-color: black; color: white;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.stage_title = QtWidgets.QLabel("ETAPA")
        self.stage_title.setAlignment(QtCore.Qt.AlignCenter)
        self.stage_title.setFont(QtGui.QFont("Arial", 36, QtGui.QFont.Bold))
        layout.addWidget(self.stage_title)

        self.instruction = QtWidgets.QLabel("Instrucciones")
        self.instruction.setAlignment(QtCore.Qt.AlignCenter)
        self.instruction.setWordWrap(True)
        self.instruction.setFont(QtGui.QFont("Arial", 22))
        layout.addWidget(self.instruction, stretch=1)

        self.timer_label = QtWidgets.QLabel("Tiempo: --")
        self.timer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.timer_label.setFont(QtGui.QFont("Arial", 28, QtGui.QFont.Bold))
        layout.addWidget(self.timer_label)

        # Test area
        self.test_widget = QtWidgets.QStackedWidget()
        layout.addWidget(self.test_widget, stretch=3)

        self.page_blank = QtWidgets.QLabel("")
        self.page_blank.setAlignment(QtCore.Qt.AlignCenter)
        self.test_widget.addWidget(self.page_blank)

        # Breathing circle (CALMA)
        self.breath_canvas = BreathWidget()
        self.test_widget.addWidget(self.breath_canvas)

        # Stroop (ENFOQUE)
        self.stroop_widget = StroopWidget()
        self.test_widget.addWidget(self.stroop_widget)

        # Controls
        btn_row = QtWidgets.QHBoxLayout()
        self.btn_prev = QtWidgets.QPushButton("⟵ Anterior")
        self.btn_next = QtWidgets.QPushButton("Siguiente ⟶")
        for b in (self.btn_prev, self.btn_next):
            b.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
            b.setStyleSheet("padding: 12px; background:#222; color:white; border:1px solid #555;")
        btn_row.addWidget(self.btn_prev)
        btn_row.addWidget(self.btn_next)
        layout.addLayout(btn_row)

        # state
        self.stage_idx = 0
        self.stage_started_t = time.time()

        # internal timer to update countdown + tests
        self.ui_timer = QtCore.QTimer()
        self.ui_timer.timeout.connect(self._tick)
        self.ui_timer.start(50)

        self.set_stage(0)

    def set_stage(self, idx: int):
        idx = int(np.clip(idx, 0, len(STAGES)-1))
        self.stage_idx = idx
        self.stage_started_t = time.time()

        st = STAGES[idx]
        self.stage_title.setText(st["title"])
        self.instruction.setText(st["instruction"])

        # Switch test widget page
        if st["name"] == "CALMA":
            self.test_widget.setCurrentWidget(self.breath_canvas)
            self.breath_canvas.reset()
        elif st["name"] == "ENFOQUE":
            self.test_widget.setCurrentWidget(self.stroop_widget)
            self.stroop_widget.reset()
        else:
            self.test_widget.setCurrentWidget(self.page_blank)

    def _tick(self):
        st = STAGES[self.stage_idx]
        elapsed = time.time() - self.stage_started_t
        remaining = max(0, int(st["duration"] - elapsed))
        self.timer_label.setText(f"Tiempo: {remaining:02d}s")

        # Update breathing/stroop animations
        if st["name"] == "CALMA":
            self.breath_canvas.update_breath(elapsed)
        elif st["name"] == "ENFOQUE":
            self.stroop_widget.update_stroop(elapsed)

    def next_stage(self):
        self.set_stage(self.stage_idx + 1)

    def prev_stage(self):
        self.set_stage(self.stage_idx - 1)


class BreathWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(300)
        self.phase = "INHALA"
        self.scale = 0.5

    def reset(self):
        self.phase = "INHALA"
        self.scale = 0.5
        self.update()

    def update_breath(self, elapsed):
        # 4s inhale, 6s exhale (period 10s)
        t = elapsed % 10.0
        if t < 4.0:
            self.phase = "INHALA"
            self.scale = 0.4 + 0.6 * (t / 4.0)
        else:
            self.phase = "EXHALA"
            self.scale = 1.0 - 0.6 * ((t - 4.0) / 6.0)
        self.update()

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.fillRect(self.rect(), QtGui.QColor("black"))

        w, h = self.width(), self.height()
        r = int(min(w, h) * 0.28 * self.scale)
        cx, cy = w//2, h//2

        p.setPen(QtGui.QPen(QtGui.QColor("white"), 6))
        p.drawEllipse(QtCore.QPoint(cx, cy), r, r)

        p.setPen(QtGui.QPen(QtGui.QColor("white"), 2))
        p.setFont(QtGui.QFont("Arial", 28, QtGui.QFont.Bold))
        text = self.phase
        p.drawText(self.rect(), QtCore.Qt.AlignCenter, text)


class StroopWidget(QtWidgets.QWidget):
    COLORS = [
        ("ROJO",   QtGui.QColor(255, 60, 60)),
        ("AZUL",   QtGui.QColor(80, 140, 255)),
        ("VERDE",  QtGui.QColor(80, 220, 120)),
        ("AMARILLO", QtGui.QColor(255, 220, 80)),
    ]

    def __init__(self):
        super().__init__()
        self.word = "ROJO"
        self.color = QtGui.QColor("white")
        self.last_change = 0.0

    def reset(self):
        self.last_change = 0.0
        self._new_item()
        self.update()

    def _new_item(self):
        w, c = random.choice(self.COLORS)
        # fuerza mismatch (palabra y color diferentes)
        w2, c2 = random.choice(self.COLORS)
        tries = 0
        while w2 == w and tries < 10:
            w2, c2 = random.choice(self.COLORS)
            tries += 1
        self.word = w
        self.color = c2

    def update_stroop(self, elapsed):
        # cambia cada 1s
        if elapsed - self.last_change >= 1.0:
            self.last_change = elapsed
            self._new_item()
            self.update()

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.fillRect(self.rect(), QtGui.QColor("black"))

        p.setPen(QtGui.QPen(self.color))
        p.setFont(QtGui.QFont("Arial", 60, QtGui.QFont.Bold))
        p.drawText(self.rect(), QtCore.Qt.AlignCenter, self.word)


# ----------------------------- Public Window (EEG + rocket/score) -----------------------------
class PublicWindow(QtWidgets.QWidget):
    def __init__(self, n_channels: int, srate: int):
        super().__init__()
        self.setWindowTitle("BCI Público (Señales + Estado)")
        self.setStyleSheet("background-color: #0b1220; color: white;")

        self.n_channels = n_channels
        self.srate = srate

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        self.top_label = QtWidgets.QLabel("Estado: -- | calm=-- act=-- blink=-- q=--")
        self.top_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        layout.addWidget(self.top_label)

        # Rocket/score bar
        self.rocket = RocketWidget()
        layout.addWidget(self.rocket, stretch=1)

        # --- EEG plots: uno por canal (grid) ---
        self.plots_widget = pg.GraphicsLayoutWidget()
        self.plots_widget.setBackground((10, 12, 18))
        layout.addWidget(self.plots_widget, stretch=4)

        self.plots = []
        self.curves = []
        self.zero_lines = []

        # Auto-escala robusta por canal
        self.last_ranges = [80.0] * self.n_channels  # rango inicial suave

        # Layout: 2 columnas si hay >=6, si no 1 columna
        cols = 2 if self.n_channels >= 6 else 1
        rows = int(np.ceil(self.n_channels / cols))

        for i in range(self.n_channels):
            r = i // cols
            c = i % cols
            p = self.plots_widget.addPlot(row=r, col=c)
            p.showGrid(x=True, y=True, alpha=0.25)
            p.setLabel("left", f"Ch {i}", units="uV")

            # En cada columna, solo el plot de la última fila muestra valores del eje X
            if r != rows - 1:
                p.getAxis("bottom").setStyle(showValues=False)
            else:
                p.setLabel("bottom", "Tiempo", units="s")

            # link de X dentro de cada columna (para que se muevan juntos)
            if r > 0:
                p.setXLink(self.plots[c])  # primer plot de esa columna

            # curva y línea cero
            curve = p.plot([], [])
            zero = pg.InfiniteLine(pos=0, angle=0, pen=pg.mkPen((120, 120, 120), width=1))
            p.addItem(zero)

            self.plots.append(p)
            self.curves.append(curve)
            self.zero_lines.append(zero)

    def update_visuals(self, stage_name: str, calm: float, act: float, blink: int, quality: float,
                       eeg_matrix_uV: np.ndarray):
        self.top_label.setText(
            f"Estado: {stage_name} | calm={calm:.2f} act={act:.2f} blink={blink} q={quality:.2f}"
        )

        self.rocket.set_values(calm=calm, blink=blink)

        # eeg_matrix_uV shape: (n_channels, n_samples)
        n_ch = min(self.n_channels, eeg_matrix_uV.shape[0])
        for i in range(n_ch):
            x = eeg_matrix_uV[i, :].astype(np.float64)

            # centrar visualmente (robusto)
            x = x - np.median(x)

            m = x.shape[0]
            t = np.linspace(-m / self.srate, 0, m)
            self.curves[i].setData(t, x)

            # auto-escala robusta (percentiles ignoran picos)
            lo = np.percentile(x, 5)
            hi = np.percentile(x, 95)
            r = float(max(10.0, (hi - lo) * 0.75))

            # suavizado para que no "salte"
            prev = self.last_ranges[i]
            r_s = 0.85 * prev + 0.15 * r
            self.last_ranges[i] = r_s

            self.plots[i].setYRange(-r_s, r_s, padding=0.02)

class RocketWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(120)
        self.calm = 0.5
        self.blink = 0
        self._blink_until = 0.0

    def set_values(self, calm: float, blink: int):
        self.calm = float(np.clip(calm, 0, 1))
        if blink == 1:
            self._blink_until = time.time() + 0.18
        self.update()

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.fillRect(self.rect(), QtGui.QColor("#0b1220"))

        w, h = self.width(), self.height()

        # track
        p.setPen(QtGui.QPen(QtGui.QColor("#3a455a"), 3))
        p.drawRoundedRect(10, 10, w-20, h-20, 16, 16)

        # rocket position from calm
        y = int((h-40) * (1.0 - self.calm)) + 20  # calm high -> up
        x = w//2

        shaking = (time.time() < self._blink_until)
        dx = random.randint(-10, 10) if shaking else 0

        # rocket = simple square
        p.setBrush(QtGui.QColor("white"))
        p.setPen(QtCore.Qt.NoPen)
        p.drawRoundedRect(x-18+dx, y-18, 36, 36, 8, 8)

        # calm text
        p.setPen(QtGui.QPen(QtGui.QColor("white")))
        p.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
        p.drawText(20, h-10, f"CALMA: {self.calm:.2f}")


# ----------------------------- Controller: acquisition + windows -----------------------------
class Controller(QtCore.QObject):
    def __init__(self, board, board_id, user_win: UserWindow, pub_win: PublicWindow, config: dict):
        super().__init__()
        self.board = board
        self.board_id = board_id
        self.user_win = user_win
        self.pub_win = pub_win

        self.eeg_channels = BoardShim.get_eeg_channels(board_id)
        self.srate = BoardShim.get_sampling_rate(board_id)

        # toma 6 EEG (si tu lista trae 8, recortamos para visual)
        self.pick_channels = self.eeg_channels[:min(6, len(self.eeg_channels))]

        # loop timers
        self.win_sec = config["eeg"]["plot_window_sec"]
        self.win_n = int(self.win_sec * self.srate)
        self.score_n = int(config["eeg"]["score_window_sec"] * self.srate)

        self.public_update_interval_sec = config["eeg"]["public_update_interval_sec"]
        self._last_pub_update = 0.0

        # connect buttons
        self.user_win.btn_next.clicked.connect(self.user_win.next_stage)
        self.user_win.btn_prev.clicked.connect(self.user_win.prev_stage)

        # update loop
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_loop)
        self.timer.start(50)

        # score smoothing
        self.calm_hist = []
        self.act_hist = []

    def update_loop(self):
        # grab latest data
        data = self.board.get_current_board_data(max(self.win_n, self.score_n))
        if data is None or data.shape[1] < int(0.5*self.srate):
            return

        # EEG matrix for plot (picked channels)
        eeg_mat = np.vstack([data[ch, -self.win_n:].astype(np.float64) for ch in self.pick_channels])

        # scores from first picked channel
        x0 = data[self.pick_channels[0], -self.score_n:].astype(np.float64)
        calm, act, blink, quality = compute_scores_one_channel(x0, self.srate)

        # smoothing (2s ~ 20 pts if we update ~10Hz)
        self.calm_hist.append(calm)
        self.act_hist.append(act)
        if len(self.calm_hist) > 20:
            self.calm_hist.pop(0)
            self.act_hist.pop(0)
        calm_s = float(np.mean(self.calm_hist))
        act_s = float(np.mean(self.act_hist))

        # stage name from user window selection
        stage_name = STAGES[self.user_win.stage_idx]["name"]

        # public update at ~10 Hz (para no saturar)
        now = time.time()
        if now - self._last_pub_update >= self.public_update_interval_sec:
            self._last_pub_update = now
            self.pub_win.update_visuals(stage_name, calm_s, act_s, blink, quality, eeg_mat)


def move_window_to_screen(window: QtWidgets.QWidget, screen: QtGui.QScreen, fullscreen=True):
    geom = screen.geometry()
    window.setGeometry(geom)
    window.move(geom.topLeft())

    if fullscreen:
        window.showFullScreen()
    else:
        window.show()


def main():
    config = load_config("configs/demo_eeg.json")

    global STAGES
    STAGES = config["stages"]

    # ------------ Connect MindRove (WiFi default) ------------
    params = MindRoveInputParams()
    params.wifi_connection = True

    # Board ID for MindRove WiFi setup
    board_id = BoardIds.MINDROVE_WIFI_BOARD.value

    BoardShim.enable_dev_board_logger()

    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream(45000)

    # ------------ Qt app + windows ------------
    app = QtWidgets.QApplication([])

    screens = app.screens()

    print(f"Detected screens: {len(screens)}")
    for i, screen in enumerate(screens):
        print(f"Screen {i}: {screen.name()} | geometry={screen.geometry()}")

    user_idx = config["display"]["user_screen_index"]
    pub_idx = config["display"]["public_screen_index"]

    if len(screens) < 2:
        print("⚠️ Only one screen detected. Connect two monitors in Extend mode.")
        user_screen = screens[0]
        pub_screen = screens[0]
    else:
        user_screen = screens[user_idx]
        pub_screen = screens[pub_idx]

    user_win = UserWindow()
    pub_win = PublicWindow(
        n_channels=config["eeg"]["n_visual_channels"],
        srate=BoardShim.get_sampling_rate(board_id)
    )
    fullscreen = config["display"]["fullscreen"]

    move_window_to_screen(user_win, user_screen, fullscreen=fullscreen)
    move_window_to_screen(pub_win, pub_screen, fullscreen=fullscreen)
    controller = Controller(board, board_id, user_win, pub_win, config)    
    
    try:
        app.exec()
    finally:
        try:
            board.stop_stream()
        except Exception:
            pass
        try:
            board.release_session()
        except Exception:
            pass


if __name__ == "__main__":
    main()