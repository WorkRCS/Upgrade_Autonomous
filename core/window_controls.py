"""Accessible in-app window controls, also available without OS decorations."""
from PyQt6.QtCore import Qt, QRect, QRectF, QEvent
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QAbstractButton, QHBoxLayout, QWidget


def initial_geometry(screen, default_width, default_height):
    """Keep the initial frame inside the work area, including nonzero origins.

    Leave space for native frame decorations; centering a fixed 780px client
    window on a 720px work area previously placed its title bar above the screen.
    """
    width = min(default_width, max(320, screen.width() - 32))
    height = min(default_height, max(300, screen.height() - 64))
    return QRect(screen.left() + max(16, (screen.width()-width)//2),
                 screen.top() + max(32, (screen.height()-height)//2), width, height)


class WindowButton(QAbstractButton):
    def __init__(self, action, window, parent=None):
        super().__init__(parent)
        self.action = action
        self.target = window
        self.setFixedSize(28, 32)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAccessibleName(action + ' window')
        self.setToolTip(action + ' window')
        self.clicked.connect(self._activate)

    def _activate(self):
        if self.action == 'Close':
            self.target.close()
        elif self.action == 'Minimize':
            self.target.showMinimized()
        elif self.target.isMaximized() or self.target.isFullScreen():
            self.target.showNormal()
        else:
            self.target.showMaximized()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = {'Close': '#FF5F57', 'Minimize': '#FEBC2E', 'Maximize': '#28C840'}[self.action]
        painter.setPen(QPen(QColor(color).darker(112), .7))
        painter.setBrush(QColor(color).darker(115) if self.isDown() else QColor(color))
        painter.drawEllipse(QRectF(7, 9, 14, 14))
        # Symbols remain visible: color is not the only indication of an action.
        painter.setPen(QPen(QColor('#352A2A'), 1.15, Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap))
        if self.action == 'Close':
            painter.drawLine(12, 14, 16, 18)
            painter.drawLine(16, 14, 12, 18)
        elif self.action == 'Minimize':
            painter.drawLine(11, 16, 17, 16)
        else:
            painter.drawRect(QRectF(11.5, 13.5, 5, 5))
        if self.hasFocus():
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor('#007AFF'), 1.5))
            painter.drawRoundedRect(QRectF(2, 3, 24, 26), 7, 7)


class WindowControls(QWidget):
    def __init__(self, window, parent=None):
        super().__init__(parent)
        self.setAccessibleName('Window controls')
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.close_button = WindowButton('Close', window, self)
        self.minimize_button = WindowButton('Minimize', window, self)
        self.maximize_button = WindowButton('Maximize', window, self)
        for button in (self.close_button, self.minimize_button, self.maximize_button):
            layout.addWidget(button)
        window.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.WindowStateChange:
            restore = watched.isMaximized() or watched.isFullScreen()
            label = 'Restore window' if restore else 'Maximize window'
            self.maximize_button.setToolTip(label)
            self.maximize_button.setAccessibleName(label)
        return super().eventFilter(watched, event)
