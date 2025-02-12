import hou
from PySide2 import QtWidgets, QtCore, QtGui

# Dark theme stylesheet with enhanced styling for various widgets.
DARK_THEME_QSS = """
/* dark_theme.qss */
QWidget {
    background-color: #2D2D2D;
    color: #E0E0E0;
    font-family: "Segoe UI", sans-serif;
    font-size: 12px;
}
QPushButton {
    background-color: #404040;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 5px 10px;
    color: #E0E0E0;
}
QPushButton:hover {
    background-color: #505050;
    border: 1px solid #666666;
}
QPushButton:pressed {
    background-color: #303030;
}
QGroupBox {
    background-color: #353535;
    border: 1px solid #444444;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 15px;
    font-size: 13px;
    color: #E0E0E0;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px;
}
QScrollArea {
    background-color: #2D2D2D;
    border: none;
}
QScrollBar:vertical {
    background: #2D2D2D;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #505050;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    background: none;
}
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}
QListWidget {
    background-color: #353535;
    border: 1px solid #444444;
    border-radius: 4px;
    color: #E0E0E0;
}
QListWidget::item {
    padding: 4px;
}
QListWidget::item:selected {
    background-color: #505050;
}
QLineEdit {
    background-color: #353535;
    border: 1px solid #444444;
    border-radius: 4px;
    padding: 5px;
    color: #E0E0E0;
}
QMenu {
    background-color: #353535;
    border: 1px solid #444444;
    color: #E0E0E0;
}
QMenu::item:selected {
    background-color: #505050;
}
QDialog {
    background-color: #2D2D2D;
}
QLabel {
    color: #E0E0E0;
}
QCheckBox {
    color: #E0E0E0;
}
QCheckBox::indicator {
    width: 14px;
    height: 14px;
}
QCheckBox::indicator:checked {
    background-color: #505050;
    border: 1px solid #666666;
}
QCheckBox::indicator:unchecked {
    background-color: #353535;
    border: 1px solid #444444;
}
/* Invert checkbox override: when checked, its indicator becomes blue */
QCheckBox#invertCheck::indicator:checked {
    background-color: #00ffc9;
    border: 1px solid #00fff0;
}
/* All Groups checkbox override: when checked, its indicator becomes orange */
QCheckBox#allGroupsCheck::indicator:checked {
    background-color: orange;
    border: 1px solid orange;
}
"""

# Custom dialog that uses a QListWidget for group selection and a read-only QLineEdit for the target node.
class GroupSelectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(GroupSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select Groups")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet(DARK_THEME_QSS)
        
        # UI Size adjustments:
        self.resize(250, 320)  # Set default size (Width: 400, Height: 300)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setMinimumSize(200, 200)  # Ensure a minimum size
        
        self.currentNodePath = ""
        layout = QtWidgets.QVBoxLayout(self)
        
        # Target node display field.
        node_layout = QtWidgets.QHBoxLayout()
        node_label = QtWidgets.QLabel("Target Node:")
        self.node_lineedit = QtWidgets.QLineEdit()
        self.node_lineedit.setReadOnly(True)
        node_layout.addWidget(node_label)
        node_layout.addWidget(self.node_lineedit)
        layout.addLayout(node_layout)
        
        # QListWidget for group selection.
        list_label = QtWidgets.QLabel("Select groups from the list:")
        layout.addWidget(list_label)
        self.group_list = QtWidgets.QListWidget()
        self.group_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        layout.addWidget(self.group_list)
        
        # Invert and All Groups checkboxes.
        self.invertCheck = QtWidgets.QCheckBox("Invert", self)
        self.invertCheck.setObjectName("invertCheck")
        layout.addWidget(self.invertCheck)
        self.allGroupsCheck = QtWidgets.QCheckBox("All Groups", self)
        self.allGroupsCheck.setObjectName("allGroupsCheck")
        layout.addWidget(self.allGroupsCheck)
        self.allGroupsCheck.toggled.connect(self.allGroupsToggled)
        
        # OK and Cancel buttons.
        btnLayout = QtWidgets.QHBoxLayout()
        okBtn = QtWidgets.QPushButton("OK", self)
        cancelBtn = QtWidgets.QPushButton("Cancel", self)
        okBtn.clicked.connect(self.doBlast)
        cancelBtn.clicked.connect(self.close)
        btnLayout.addWidget(okBtn)
        btnLayout.addWidget(cancelBtn)
        layout.addLayout(btnLayout)
        
        # Timer to auto-refresh the target node field and group list.
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.autoRefresh)
        self.timer.start()
    
    def autoRefresh(self):
        # Refresh the node and group list based on the current Houdini selection.
        sel = hou.selectedNodes()
        if sel:
            node = sel[0]
            if node.path() != self.currentNodePath:
                self.currentNodePath = node.path()
                self.node_lineedit.setText(self.currentNodePath)
                geo = node.geometry()
                groups = []
                if geo:
                    groups = [g.name() for g in (geo.pointGroups() + geo.primGroups())]
                self.allGroups = groups
                self.group_list.clear()
                for group in groups:
                    item = QtWidgets.QListWidgetItem(group)
                    self.group_list.addItem(item)
        else:
            self.node_lineedit.clear()
            self.currentNodePath = ""
            self.group_list.clear()
    
    def allGroupsToggled(self, checked):
        # Select or clear all groups based on the checkbox state.
        if checked:
            self.group_list.selectAll()
        else:
            self.group_list.clearSelection()
    
    def getSelectedGroups(self):
        return [item.text() for item in self.group_list.selectedItems()]
    
    def isInvertChecked(self):
        return self.invertCheck.isChecked()
    
    def doBlast(self):
        selected_groups = self.getSelectedGroups()
        if self.isInvertChecked():
            selected_groups = [grp for grp in self.allGroups if grp not in selected_groups]
        if selected_groups:
            blast_groups_from_selected(selected_groups)
        else:
            hou.ui.displayMessage("No groups selected.")

# Blast node creation function with color gradient feature.
def blast_groups_from_selected(selected_groups):
    sel = hou.selectedNodes()
    if not sel:
        return
    node = sel[0]
    geo = node.geometry()
    if not geo:
        return
    point_groups = [g.name() for g in geo.pointGroups()]
    num_groups = len(selected_groups)
    
    for i, group in enumerate(selected_groups):
        blast = node.createOutputNode("blast", node_name="blast_" + group)
        if not blast:
            continue
        if blast.parm("group"):
            blast.parm("group").set(group)
        if blast.parm("entity"):
            blast.parm("entity").set(0 if group in point_groups else 1)
        if blast.parm("negate"):
            blast.parm("negate").set(1)
        
        # Apply a color gradient to the blast node.
        fade_factor = i / (num_groups - 1) if num_groups > 1 else 0
        red, green, blue = 1.0 - fade_factor * 0.5, 1.0, fade_factor * 0.8
        blast.setColor(hou.Color((red, green, blue)))
        
        # Schedule Houdini's automatic node placement.
        QtCore.QTimer.singleShot(0, lambda b=blast: b.moveToGoodPosition())

# Show the dialog modelessly.
def show_group_selection_ui():
    global gDialog
    gDialog = GroupSelectionDialog()
    gDialog.setModal(False)
    gDialog.show()

# Run the tool.
show_group_selection_ui()
