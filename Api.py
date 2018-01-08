#!-*-coding:utf-8-*-
from PyQt4 import QtGui

class ApiOS:
    FILE_EXTENDED = u'.vscan'
    FILE_FORMAT = u'VScan Data Base of Virus file [.vscan] (*.vscan)'

    DIALOG_OPEN_DATA_NAME = u'Открыть базу вирусов'   
    DIALOG_SAVE_DATA_NAME = u"Сохранить базу вирусов"
    DIALOG_OPEN_FOLDER_NAME = u"Сканирование директории"
      
    MESSAGE_WARNING = u'Предупреждение'
    MESSAGE_ERROR = u'Ошибка'
    
    EXCEPTIONS = [u"vscan"]

    def add_extended_to_file_name(self, file_name_without):
        return unicode(file_name_without) + self.FILE_EXTENDED

    def is_have_extended(self, file_path):
        extended_len = len(self.FILE_EXTENDED)
        extended = file_path[-extended_len:]

        if extended == self.FILE_EXTENDED:
            return True
        return False

  
    def show_open_data_dialog(self, parent_window):
        file_data_path = QtGui.QFileDialog.getOpenFileName(parent_window,
                                                           self.DIALOG_OPEN_DATA_NAME,
                                                           '',
                                                           self.FILE_FORMAT)
        if file_data_path:
            return file_data_path
        else:
            return None

    def show_save_data_dialog(self, parent_window):
        file_schema_path = QtGui.QFileDialog.getSaveFileName(parent_window,
                                                             self.DIALOG_SAVE_PROJECT_NAME,
                                                             '',
                                                             self.FILE_FORMAT)
        if file_schema_path:
            return file_schema_path
        else:
            return None

    def show_create_data_dialog(self, parent_window):

        new_schema_file_path = QtGui.QFileDialog.getSaveFileName(parent_window,
                                                                 self.DIALOG_SAVE_PROJECT_NAME,
                                                                 '',
                                                                 self.FILE_FORMAT)

        if new_schema_file_path:
            if self.is_have_extended(new_schema_file_path):
                return new_schema_file_path
            else:
                return self.add_extended_to_file_name(new_schema_file_path)
        else:
            return None

    def show_open_folder_dialog(self, parent_window):
        folder_path = QtGui.QFileDialog.getExistingDirectory(parent_window,
                                                             self.DIALOG_OPEN_FOLDER_NAME,
                                                             '',
                                                             QtGui.QFileDialog.ShowDirsOnly)
        if folder_path:
            return folder_path
        else:
            return None

    def show_variants_to_delete_node(self):
        message_box = QtGui.QMessageBox()
        message_box.setText(u'Вы действительно хотите удалить выбранный элемент?')
        message_box.setWindowTitle(self.MESSAGE_WARNING)
        message_box.addButton(QtGui.QMessageBox.Yes)
        message_box.addButton(QtGui.QMessageBox.No)
        message_box.setDefaultButton(QtGui.QMessageBox.No)
        variant_select = message_box.exec_()

        if variant_select == QtGui.QMessageBox.Yes:
            return True

        if variant_select == QtGui.QMessageBox.No:
            return False
   
    def send_system_message(self, title, text):
        message_box = QtGui.QMessageBox()
        message_box.setText(text)
        message_box.setWindowTitle(title)
        message_box.exec_()
