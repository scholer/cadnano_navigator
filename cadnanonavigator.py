# The MIT License
#
# Copyright (c) 2011 Wyss Institute at Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# http://www.opensource.org/licenses/mit-license.php
"""


Updating the mainwindow's statusbar:
    self.win.statusBar().showMessage(statusString)
"""
import os
import util
import cadnano_api

try:
    qt_available = util.chosenQtFramework or util.find_available_qt_framework()
except AttributeError as e:
    msg = "AttributeError: %s - this cadnano might be too old for this plugin, aborting load." % (e, )
    print msg
    raise ImportError(msg)

#from cadnanonavigator_ui import Ui_Navigator
if qt_available.lower() == 'pyside':
    print "Autobreak: Using PySide."
    from pyside_ui.navigator_ui import Ui_Dialog
else:
    print "Autobreak: Using PyQt4."
    from navigator_ui import Ui_Dialog

util.qtWrapImport('QtGui', globals(), ['QIcon', 'QPixmap', 'QAction'])
util.qtWrapImport('QtGui', globals(), ['QDialog', 'QKeySequence', 'QDialogButtonBox', 'QIntValidator'])
util.qtWrapImport('QtCore', globals(), ['Qt'])



class NavigatorHandler(object):
    def __init__(self, document, window):
        self.doc, self.win = document, window
        icon10 = QIcon()
        icon_path = os.path.join(os.path.dirname(__file__), "res", "Navigator_32x32.png")
        icon10.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
        self.actionNavigator = QAction(window)
        self.actionNavigator.setIcon(icon10)
        self.actionNavigator.setText('Navigator')
        self.actionNavigator.setToolTip("Use the navigator to quickly navigate around the cadnano views.")
        self.actionNavigator.setObjectName("actionNavigator")
        self.actionNavigator.triggered.connect(self.actionNavigateSlot)
        self.win.menuPlugins.addAction(self.actionNavigator)
        # add to main tool bar
        self.win.topToolBar.insertAction(self.win.actionFiltersLabel, self.actionNavigator)
        self.win.topToolBar.insertSeparator(self.win.actionFiltersLabel)
        self.navigatorDialog = None
        self.use_animation = cadnano_api.ANIMATE_ENABLED_DEFAULT


    def actionNavigateSlot(self):
        """Only show the dialog if staple strands exist."""
        print "cadnanonavigator.NavigatorHandler.actionOpenConsoleSlot() invoked (DEBUG)"
        part = self.doc.controller().activePart()
        if part != None:  # is there a part?
            for o in list(part.oligos()):
                if o.isStaple():  # is there a staple oligo?
                    if self.navigatorDialog == None:
                        self.navigatorDialog = NavigatorDialog(self.win, self)
                        self.make_ui_connections()
                    self.navigatorDialog.show()
                    return
        print "You should open a document before you use the navigator."


    def make_ui_connections(self):
        """
        Note: Using a QtDialog has some disadvantages.
        For instance, it is hard to get correct button focus behavior.
        Dialogs are set up for default-button behavior, which is not really what I want in this widget.
        You can use flat=True to make the button look more like a label.
        """
        uiDia = self.navigatorDialog
        # You connect a signal to a function/slot.
        uiDia.centerOnStrandButton.clicked.connect(self.centerOnStrandSlot)
        uiDia.centerOnSelectedButton.clicked.connect(self.centerOnSelectedSlot)
        uiDia.follow5pButton.clicked.connect(self.followStrand5pSlot)
        uiDia.follow3pButton.clicked.connect(self.followStrand3pSlot)
        uiDia.sliceToSelectedButton.clicked.connect(self.sliceToSelectedSlot)
        # In theory I might be able to bind uiDia.activeBaseIndexInput to part._activeBaseIndex,
        # but that would not invoke the partActiveSliceIndexSignal signal.
        # Alternatively, you could bind to the window's slicer...
        uiDia.activeBaseIndexInput.setValidator(QIntValidator(uiDia.activeBaseIndexInput))
        uiDia.activeBaseIndexInput.editingFinished.connect(self.setActiveBaseIndexSlot)



    ### SLOTS ###


    def centerOnStrandSlot(self):
        """
        Slots are the callback functions registrered to signals with connect(), e.g.:
            mvh.virtualHelixNumberChangedSignal.connect(vhItem.virtualHelixNumberChangedSlot)
        To emit a signal, one just call <signal>.emit(<args>), e.g.:
            virtualHelixNumberChangedSignal.emit(self, number)  # from model/virtualhelix.py
        With vhItem.virtualHelixNumberChangedSlot connected (registered) to virtualHelixNumberChangedSignal,
        invoking virtualHelixNumberChangedSignal.emit(vhelix, number) would call
            vhItem.virtualHelixNumberChangedSlot(vhelix, number).
        A slots should thus be prepared to consume the same number of arguments as could be passed
        by the signal's emit().
        Typically, a signal would be emitted by its parent, e.g. a button emits a clicked() signal
        when it is pressed.
        """
        print "centerOnStrandSlot() invoked by pressing centerOnStrandButton."
        cadnano_api.centerOnStrand(None, animate=self.use_animation)

    def centerOnSelectedSlot(self):
        print "centerOnStrandSlot() invoked by pressing centerOnStrandButton."
        cadnano_api.centerOnSelected(None, animate=self.use_animation)

    def followStrand5pSlot(self):
        print "centerOnStrandSlot() invoked by pressing centerOnStrandButton."
        cadnano_api.follow_strand_5p(None, animate=self.use_animation)

    def followStrand3pSlot(self):
        print "centerOnStrandSlot() invoked by pressing centerOnStrandButton."
        cadnano_api.follow_strand_3p(None, animate=self.use_animation)

    def sliceToSelectedSlot(self):
        print "centerOnStrandSlot() invoked by pressing centerOnStrandButton."
        cadnano_api.move_active_baseindex_to_strand()

    def setActiveBaseIndexSlot(self, *args):
        #print "setActiveBaseIndexSlot() invoked with args: {}".format(args)
        val = self.navigatorDialog.activeBaseIndexInput.text()
        try:
            val = val.toInt()[0]
        except AttributeError:
            val = int(val)
        cadnano_api.set_active_baseindex(val)



class NavigatorDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, handler):
        QDialog.__init__(self, parent, Qt.Sheet)
        self.setupUi(self)
        self.handler = handler
        # Setting keyboard shortcuts:
        #fb = self.buttonBox.button(QDialogButtonBox.Cancel)
        #fb.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_R ))


    def keyPressEvent(self, e):
        return QDialog.keyPressEvent(self, e)

    def closeDialog(self):
        self.close()

    def accept(self):
        pass
