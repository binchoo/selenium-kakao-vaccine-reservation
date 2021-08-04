def wrap_setLayout(self, layout):
    self.setLayout(layout)
    self._layout = layout

def wrap_addChild(self, widget):
    layout = self._layout
    if layout is None:
        return None
    layout.addWidget(widget)
    return widget

def apply_qwidget_wrapping():
    from PyQt5.QtWidgets import QWidget
    QWidget.useLayout = wrap_setLayout
    QWidget.addChild = wrap_addChild