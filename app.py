import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QStyle,
    QStyleFactory,
    QDialog,
    QListWidget,
    QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QColor, QPalette

class OrderDialog(QDialog):
    def __init__(self, checked_items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("순서 설정")
        self.setGeometry(200, 200, 400, 500)
        
        layout = QHBoxLayout(self)
        
        # 왼쪽 패널: 리스트 위젯
        left_panel = QVBoxLayout()
        self.list_widget = QListWidget()
        for item in checked_items:
            self.list_widget.addItem(item)
        left_panel.addWidget(self.list_widget)
        
        # 오른쪽 패널: 버튼들
        right_panel = QVBoxLayout()
        self.up_button = QPushButton("↑ 위로")
        self.down_button = QPushButton("↓ 아래로")
        self.start_button = QPushButton("시작")
        
        right_panel.addWidget(self.up_button)
        right_panel.addWidget(self.down_button)
        right_panel.addStretch()
        right_panel.addWidget(self.start_button)
        
        # 버튼 연결
        self.up_button.clicked.connect(self.move_item_up)
        self.down_button.clicked.connect(self.move_item_down)
        self.start_button.clicked.connect(self.accept)
        
        # 레이아웃 설정
        layout.addLayout(left_panel, 3)
        layout.addLayout(right_panel, 1)
    
    def move_item_up(self):
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row - 1, item)
            self.list_widget.setCurrentItem(item)
    
    def move_item_down(self):
        current_row = self.list_widget.currentRow()
        if current_row < self.list_widget.count() - 1:
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row + 1, item)
            self.list_widget.setCurrentItem(item)

    def get_ordered_items(self):
        return [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
    
class UltraModernMidasLinker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Midas Linker Pro")
        self.setGeometry(100, 100, 1200, 700)
        self.setFixedSize(1200, 700)  # Fixed size
        
        # Set application style
        self.setStyle(QStyleFactory.create("Fusion"))
        
        # Set color palette
        palette = self.create_palette()
        self.setPalette(palette)

        self.setStyleSheet(self.create_stylesheet())
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.checkbox_groups = [
            ("모델링 형태", ["타입분할(태양광)", "타입분할(건물)", "건물 / 태양광 통합"]),
            ("건물", ["크레인", "지진", "바닥 활하중", "기타 고정하중", "펄린"]),
            ("태양광 형태", ["기본형", "부착형", "알류미늄"]),
            ("건물 정보", ["토지위(푸팅)", "토지위(파일)", "슬라브위", "건물위"]),
            ("태양광 기타해석", ["접합부", "안전로프"]),
        ]
        self.checkboxes = []

        self.create_left_panel()
        self.create_right_panel()

    def create_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(50, 50, 50))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(50, 50, 50))
        palette.setColor(QPalette.ColorRole.Text, QColor(50, 50, 50))
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(50, 50, 50))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        return palette

    def create_stylesheet(self):
        return """
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
                font-size: 14px;
                color: #323232;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                background-color: #ffffff;
                font-size: 14px;
                color: #323232;
            }
            QPushButton {
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                background-color: #2a82da;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a92ea;
            }
            QCheckBox {
                font-size: 14px;
                color: #323232;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #d0d0d0;
                border-radius: 2px;
                background-color: #ffffff;
            }
            QCheckBox::indicator:checked {
                border-color: #2a82da;
                image: url(./assets/checkmark.png);
            }
            QFrame {
                background-color: #ffffff;
                border-radius: 8px;
            }
            QFrame#LeftPanel, QFrame#RightPanel {
                padding: 20px;
            }
        """

    def create_left_panel(self):
        left_panel = QFrame()
        left_panel.setObjectName("LeftPanel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)

        title = QLabel("Midas Linker Pro")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #2a82da; margin-bottom: 20px;"
        )
        left_layout.addWidget(title)

        # File location entries
        file_locations = ["태양광", "건물", "디자인"]
        for location in file_locations:
            hlayout = QHBoxLayout()
            label = QLabel(f"{location}")
            label.setFixedWidth(50)
            entry = QLineEdit()
            entry.setPlaceholderText(f"{location} 파일 위치")
            button = QPushButton("찾아보기")
            button.setFixedWidth(90)
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            button.clicked.connect(lambda _, e=entry: self.browse_file(e))
            
            hlayout.addWidget(label)
            hlayout.addWidget(entry)
            hlayout.addWidget(button)
            hlayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            left_layout.addLayout(hlayout)

        left_layout.addSpacing(20)

        # Basic info entries
        basic_info = ["태양광 명칭", "풍속 (m/s)", "설하중 (kN/m²)", "노풍도"]
        for info in basic_info:
            entry = QLineEdit()
            entry.setPlaceholderText(info)
            left_layout.addWidget(entry)

        left_layout.addStretch()

        create_button = QPushButton("프로젝트 생성")
        create_button.setFixedHeight(50)
        create_button.setStyleSheet(
            """
            QPushButton {
                background-color: #34c759;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2db84c;
            }
        """
        )
        create_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        create_button.clicked.connect(self.create_project)
        left_layout.addWidget(create_button)

        self.main_layout.addWidget(left_panel, 1)

    def create_right_panel(self):
        right_panel = QFrame()
        right_panel.setObjectName("RightPanel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(20)

        # Grid Layout for Checkboxes
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        row = 0
        for group_name, options in self.checkbox_groups:
            group_label = QLabel(group_name)
            group_label.setStyleSheet(
                "font-size: 20px; font-weight: bold; color: #2a82da;"
            )
            grid_layout.addWidget(group_label, row, 0, 1, 2)
            row += 1

            for index, option in enumerate(options):
                checkbox = QCheckBox(option)
                checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                grid_layout.addWidget(checkbox, row + index // 2, index % 2)
                self.checkboxes.append(checkbox)  # 체크박스 리스트에 추가

            row += (len(options) + 1) // 2

        right_layout.addLayout(grid_layout)
        right_layout.addStretch()
        self.main_layout.addWidget(right_panel, 1)

    def browse_file(self, entry):
        filename, _ = QFileDialog.getOpenFileName(self, "파일 선택")
        if filename:
            entry.setText(filename)

    def create_project(self):
        checked_items = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        
        if not checked_items:
            print("선택된 항목이 없습니다.")
            return
        
        order_dialog = OrderDialog(checked_items, self)
        if order_dialog.exec() == QDialog.DialogCode.Accepted:
            ordered_items = order_dialog.get_ordered_items()
            print("선택된 항목 순서:")
            for idx, item in enumerate(ordered_items, 1):
                print(f"{idx}. {item}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UltraModernMidasLinker()
    window.show()
    sys.exit(app.exec())