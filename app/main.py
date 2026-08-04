import sys
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from PySide6.QtGui import QIcon, QFont, QFontDatabase

def main():

    app = QApplication(sys.argv)
    
    font_id1 = QFontDatabase.addApplicationFont(
        "assets/fonts/OrangeAvenueDEMO-Regular.otf"
    )
    
    font_id2 = QFontDatabase.addApplicationFont(
            "assets/fonts/OrangeAvenueOutlineDEMO-Regular.otf"
        )

    if font_id1 != -1:
        font_family = (
            QFontDatabase.applicationFontFamilies(
                font_id1
            )[0]
        )
        
        app.setFont(
            QFont(
                font_family,
                14
                )
            )
        
        print(
            f"Default application font loaded: "
            f"{font_family}"
        ) 
    else:
        print(
            "Warning: Failed to load "
            "Orange Avenue Regular font." )

    app.setApplicationName(
        "BackgroundRemoverAI"
    )

    app.setWindowIcon(
        QIcon("assets/app_icon.ico")
    )

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()