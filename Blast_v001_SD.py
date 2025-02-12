import hou
from PySide2 import QtWidgets, QtCore, QtGui

# Dark theme stylesheet with enhanced styling for various widgets,
# including QListWidget (used for group selection) and checkboxes.
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
QListWidget {
    background-color: #353535;
    border: 1px solid #444444;
    border-radius: 4px;
    color: #E0E0E0;
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
QCheckBox {
    color: #E0E0E0;
}
QCheckBox::indicator {
    width: 14px;
    height: 14px;
}
"""

class GroupSelectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(GroupSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select Groups")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet(DARK_THEME_QSS)
        self.resize(250, 180)
        self.currentNodePath = ""

        layout = QtWidgets.QVBoxLayout(self)
        
        node_layout = QtWidgets.QHBoxLayout()
        node_label = QtWidgets.QLabel("Target Node:")
        self.node_lineedit = QtWidgets.QLineEdit()
        self.node_lineedit.setReadOnly(True)
        node_layout.addWidget(node_label)
        node_layout.addWidget(self.node_lineedit)
        layout.addLayout(node_layout)
        
        list_label = QtWidgets.QLabel("Select groups from the list:")
        layout.addWidget(list_label)
        self.group_list = QtWidgets.QListWidget()
        self.group_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        layout.addWidget(self.group_list)
        
        self.invertCheck = QtWidgets.QCheckBox("Invert", self)
        self.invertCheck.setObjectName("invertCheck")
        layout.addWidget(self.invertCheck)
        self.allGroupsCheck = QtWidgets.QCheckBox("All Groups", self)
        self.allGroupsCheck.setObjectName("allGroupsCheck")
        layout.addWidget(self.allGroupsCheck)
        self.allGroupsCheck.toggled.connect(self.allGroupsToggled)
        
        btnLayout = QtWidgets.QHBoxLayout()
        okBtn = QtWidgets.QPushButton("OK", self)
        cancelBtn = QtWidgets.QPushButton("Cancel", self)
        okBtn.clicked.connect(self.doBlast)
        cancelBtn.clicked.connect(self.close)
        btnLayout.addWidget(okBtn)
        btnLayout.addWidget(cancelBtn)
        layout.addLayout(btnLayout)
        
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.autoRefresh)
        self.timer.start()
    
    def autoRefresh(self):
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

        # Apply color gradient (smooth transition)
        fade_factor = i / (num_groups - 1) if num_groups > 1 else 0
        red, green, blue = 1.0 - fade_factor * 0.5, 1.0, fade_factor * 0.8
        blast.setColor(hou.Color((red, green, blue)))
        
        QtCore.QTimer.singleShot(0, lambda b=blast: b.moveToGoodPosition())

# Show the dialog modelessly.
def show_group_selection_ui():
    global gDialog
    gDialog = GroupSelectionDialog()
    gDialog.setModal(False)
    gDialog.show()

# Run the tool.
show_group_selection_ui()
