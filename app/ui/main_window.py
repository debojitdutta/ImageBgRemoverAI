from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QComboBox,
    QGroupBox,
)

from PIL import Image

from app.core.remover import BackgroundRemover


class ProcessingWorker(QThread):
    """
    Runs AI background removal in a separate thread
    so the GUI does not freeze.
    """

    finished = Signal(object)
    error = Signal(str)

    def __init__(self, image, model_name):
        super().__init__()

        self.image = image
        self.model_name = model_name

    def run(self):
        try:
            remover = BackgroundRemover(self.model_name)

            result = remover.remove_background(
                self.image
            )

            self.finished.emit(result)

        except Exception as e:
            self.error.emit(str(e))


class ImageLabel(QLabel):
    """
    QLabel designed for displaying images.
    """

    def __init__(self, title):
        super().__init__()

        self.title = title

        self.setAlignment(Qt.AlignCenter)

        self.setText(title)

        self.setMinimumSize(400, 350)

        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #555;
                border-radius: 10px;
                background-color: #202020;
                color: #aaaaaa;
                font-size: 16px;
            }
        """)

    def set_image(self, image: Image.Image):
        """
        Displays a PIL image inside the label.
        """

        image = image.convert("RGBA")

        data = image.tobytes("raw", "RGBA")

        qimage = QImage(
            data,
            image.width,
            image.height,
            QImage.Format_RGBA8888
        )

        pixmap = QPixmap.fromImage(qimage)

        scaled_pixmap = pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.setPixmap(scaled_pixmap)

    def clear_image(self):
        self.clear()
        self.setText(self.title)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "BackgroundAI - AI Background Remover"
        )

        self.setMinimumSize(1000, 700)

        self.original_image = None
        self.result_image = None
        self.current_file = None

        self.worker = None

        self.setup_ui()

    def setup_ui(self):

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout(
            central_widget
        )

        # ---------------------------------
        # Title
        # ---------------------------------

        title = QLabel(
            "BackgroundAI"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: bold;
                padding: 15px;
            }
        """)

        main_layout.addWidget(
            title
        )

        subtitle = QLabel(
            "Local AI Background Removal"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setStyleSheet("""
            QLabel {
                color: #999999;
                font-size: 14px;
            }
        """)

        main_layout.addWidget(
            subtitle
        )

        # ---------------------------------
        # Image preview area
        # ---------------------------------

        image_layout = QHBoxLayout()

        original_group = QGroupBox(
            "Original Image"
        )

        original_group_layout = QVBoxLayout(
            original_group
        )

        self.original_label = ImageLabel(
            "No image selected"
        )

        original_group_layout.addWidget(
            self.original_label
        )

        result_group = QGroupBox(
            "Background Removed"
        )

        result_group_layout = QVBoxLayout(
            result_group
        )

        self.result_label = ImageLabel(
            "Result will appear here"
        )

        result_group_layout.addWidget(
            self.result_label
        )

        image_layout.addWidget(
            original_group
        )

        image_layout.addWidget(
            result_group
        )

        main_layout.addLayout(
            image_layout
        )

        # ---------------------------------
        # Model selection
        # ---------------------------------

        controls_layout = QHBoxLayout()

        controls_layout.addWidget(
            QLabel("AI Model:")
        )

        self.model_combo = QComboBox()

        self.model_combo.addItems([
            "u2net",
            "u2netp",
            "u2net_human_seg",
            "u2net_cloth_seg",
        ])

        controls_layout.addWidget(
            self.model_combo
        )

        controls_layout.addStretch()

        # ---------------------------------
        # Buttons
        # ---------------------------------

        self.open_button = QPushButton(
            "Open Image"
        )

        self.remove_button = QPushButton(
            "Remove Background"
        )

        self.reprocess_button = QPushButton(
            "Reprocess"
        )

        self.save_button = QPushButton(
            "Save Result"
        )

        self.clear_button = QPushButton(
            "Clear"
        )

        controls_layout.addWidget(
            self.open_button
        )

        controls_layout.addWidget(
            self.remove_button
        )

        controls_layout.addWidget(
            self.reprocess_button
        )

        controls_layout.addWidget(
            self.save_button
        )

        controls_layout.addWidget(
            self.clear_button
        )

        main_layout.addLayout(
            controls_layout
        )

        # ---------------------------------
        # Progress bar
        # ---------------------------------

        self.progress_bar = QProgressBar()

        self.progress_bar.setRange(
            0,
            0
        )

        self.progress_bar.hide()

        main_layout.addWidget(
            self.progress_bar
        )

        # ---------------------------------
        # Status
        # ---------------------------------

        self.status_label = QLabel(
            "Ready"
        )

        self.status_label.setAlignment(
            Qt.AlignCenter
        )

        main_layout.addWidget(
            self.status_label
        )

        # ---------------------------------
        # Button connections
        # ---------------------------------

        self.open_button.clicked.connect(
            self.open_image
        )

        self.remove_button.clicked.connect(
            self.remove_background
        )

        self.reprocess_button.clicked.connect(
            self.reprocess
        )

        self.save_button.clicked.connect(
            self.save_result
        )

        self.clear_button.clicked.connect(
            self.clear_all
        )

        # Initial states

        self.remove_button.setEnabled(
            False
        )

        self.reprocess_button.setEnabled(
            False
        )

        self.save_button.setEnabled(
            False
        )

    # ---------------------------------
    # Open image
    # ---------------------------------

    def open_image(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )

        if not file_path:
            return

        try:

            image = Image.open(
                file_path
            ).convert("RGBA")

            self.original_image = image

            self.current_file = file_path

            self.original_label.set_image(
                image
            )

            self.result_image = None

            self.result_label.clear_image()

            self.remove_button.setEnabled(
                True
            )

            self.reprocess_button.setEnabled(
                False
            )

            self.save_button.setEnabled(
                False
            )

            self.status_label.setText(
                f"Loaded: {Path(file_path).name}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Could not open image:\n{e}"
            )

    # ---------------------------------
    # Remove background
    # ---------------------------------

    def remove_background(self):

        if self.original_image is None:
            return

        self.process_image(
            self.original_image
        )

    # ---------------------------------
    # Reprocess
    # ---------------------------------

    def reprocess(self):

        if self.original_image is None:
            return

        self.process_image(
            self.original_image
        )

    # ---------------------------------
    # Start processing
    # ---------------------------------

    def process_image(
        self,
        image
    ):

        model_name = (
            self.model_combo.currentText()
        )

        self.status_label.setText(
            f"Processing using {model_name}..."
        )

        self.progress_bar.show()

        self.set_buttons_enabled(
            False
        )

        self.worker = ProcessingWorker(
            image,
            model_name
        )

        self.worker.finished.connect(
            self.processing_finished
        )

        self.worker.error.connect(
            self.processing_error
        )

        self.worker.start()

    # ---------------------------------
    # Processing complete
    # ---------------------------------

    def processing_finished(
        self,
        result
    ):

        self.result_image = result

        self.result_label.set_image(
            result
        )

        self.progress_bar.hide()

        self.status_label.setText(
            "Background removed successfully."
        )

        self.set_buttons_enabled(
            True
        )

        self.reprocess_button.setEnabled(
            True
        )

        self.save_button.setEnabled(
            True
        )

    # ---------------------------------
    # Processing error
    # ---------------------------------

    def processing_error(
        self,
        error
    ):

        self.progress_bar.hide()

        self.status_label.setText(
            "Processing failed."
        )

        self.set_buttons_enabled(
            True
        )

        QMessageBox.critical(
            self,
            "Processing Error",
            error
        )

    # ---------------------------------
    # Save result
    # ---------------------------------

    def save_result(self):

        if self.result_image is None:
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Result",
            "background_removed.png",
            "PNG Image (*.png)"
        )

        if not save_path:
            return

        try:

            self.result_image.save(
                save_path,
                "PNG"
            )

            self.status_label.setText(
                f"Saved: {Path(save_path).name}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Save Error",
                f"Could not save image:\n{e}"
            )

    # ---------------------------------
    # Clear everything
    # ---------------------------------

    def clear_all(self):

        self.original_image = None

        self.result_image = None

        self.current_file = None

        self.original_label.clear_image()

        self.result_label.clear_image()

        self.remove_button.setEnabled(
            False
        )

        self.reprocess_button.setEnabled(
            False
        )

        self.save_button.setEnabled(
            False
        )

        self.status_label.setText(
            "Ready"
        )

    # ---------------------------------
    # Button state
    # ---------------------------------

    def set_buttons_enabled(
        self,
        enabled
    ):

        self.open_button.setEnabled(
            enabled
        )

        self.clear_button.setEnabled(
            enabled
        )

        self.model_combo.setEnabled(
            enabled
        )

        if self.original_image is not None:
            self.remove_button.setEnabled(
                enabled
            )

        if self.result_image is not None:
            self.reprocess_button.setEnabled(
                enabled
            )

            self.save_button.setEnabled(
                enabled
            )