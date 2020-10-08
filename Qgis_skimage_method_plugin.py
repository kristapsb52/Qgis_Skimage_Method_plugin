# -*- coding: utf-8 -*-
"""
/***************************************************************************
 getMedianFunctions
                                 A QGIS plugin
 This plugin shows a drop box with all the available functions for the chosen module
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-09-01
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Kristaps Blumbergs
        email                : kristapsb52@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox, QDialog, QPushButton
from qgis.core import QgsProject, QgsRasterFileWriter, QgsRasterPipe, Qgis, QgsMessageLog, QgsRasterLayer, QgsCoordinateReferenceSystem, QgsApplication, QgsTask
from qgis.utils import iface
from qgis.gui import QgsDialog


from skimage.io import imread
# Initialize Qt resources from file resources.py

# Import the code for the dialog
from .Qgis_skimage_method_plugin_dialog import getMedianFunctionsDialog
from .Qgis_skimage_method_usermanual_dialog import userManualDialog
import os.path
import inspect
import gdal
import osr
from .method_call import *

class QgisSkimageMethods:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'QgisSkimageMethod{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Qgis Skimage Method')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        self.tm = QgsApplication.taskManager()

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Qgis Skimage Method', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToRasterMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        icon_path = dir_path + "/icon.png"
        self.add_action(
            icon_path,
            text=self.tr(u'get Module Functions'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        # try:
        #     file_path = self.dlg.OutputFile.text()
        #     file_name = self.get_save_file_name()
        # except:
        #     pass
        for action in self.actions:
            self.iface.removePluginRasterMenu(
                self.tr(u'&Qgis Skimage Method'),
                action)
            self.iface.removeToolBarIcon(action)

        # Method 1
        # iface.addRasterLayer(file_path, file_name)

        # Method 2
        # rlayer = QgsRasterLayer(file_path, file_name)
        # QgsProject.instance().addMapLayer(rlayer)

    def completed(self, exception, result=None ):

        if exception is None:
            if result is None:
                QMessageBox.information(None, "Warning", str(exception))
            else:
                if self.dlg.checkBox.isChecked():
                    QMessageBox.information(None, "Completed", 'Image processing completed')
                    self.iface.addRasterLayer(result, "Result") # TODO Fix add raster layer
        else:
            QMessageBox.warning(None, "Error", "{}".format(exception))
            raise exception

    def stopped(self, task):
        QgsMessageLog.logMessage(
            'Task "{name}" was canceled'.format(
                name=task.description()),
            "Wasting time", Qgis.Info)

    # Updates the method list for the chosen module
    def update_function_list(self):
        self.dlg.AvailableFunctionsBox.clear()

        # Reads file that has all the methods
        dir_path = os.path.dirname(os.path.realpath(__file__))
        method_file = open(dir_path + "\method_list.txt", "r")

        # Reads the chosen module
        chosen_method = "Filter"
        if (self.dlg.ModuleBox.currentIndex == 0):
            chosen_method = "Filter"
        elif (self.dlg.ModuleBox.currentIndex() == 1):
            chosen_method = "Exposure"
        elif (self.dlg.ModuleBox.currentIndex() == 2):
            chosen_method = "Segmentation"

        # Reads all the methods for the user chosen module
        allmethods = []
        methodFound = False
        for line in method_file:
            if (methodFound):
                if (line == "\n"):
                    break
                allmethods.append(line)
            if (line == chosen_method + "\n"):
                methodFound = True

        method_file.close()
        result_methods = []
        for x in range(len(allmethods)):
            allmethods[x] = allmethods[x].replace('\n', '')
            if (allmethods[x] != chosen_method):
                result_methods.append(allmethods[x])

        self.dlg.AvailableFunctionsBox.addItems(result_methods)

    def update_info_box(self):
        self.dlg.InfoBox.clear()
        method_doc = ""
        chosenMethod = self.dlg.AvailableFunctionsBox.currentText()
        try:
            if (self.dlg.ModuleBox.currentIndex() == 0):
                method_doc = inspect.getdoc(getattr(filters, chosenMethod))
            elif (self.dlg.ModuleBox.currentIndex() == 1):
                method_doc = inspect.getdoc(getattr(exposure, chosenMethod))
            elif (self.dlg.ModuleBox.currentIndex() == 2):
                method_doc = inspect.getdoc(getattr(segmentation, chosenMethod))
        except AttributeError:
            pass

        parameter_line = False
        for line in method_doc.splitlines():
            if (line == "Parameters"):
                parameter_line = True
            if (line == "Returns"):
                parameter_line = False
            if (parameter_line):
                self.dlg.InfoBox.addItem(line)



    def get_arguments_for_method(self):
        # Gets the chosen method
        chosenMethod = self.dlg.AvailableFunctionsBox.currentText()
        method_info = ""
        try:
            if (self.dlg.ModuleBox.currentIndex() == 0):
                method_info = inspect.getfullargspec(getattr(filters, chosenMethod))
            elif (self.dlg.ModuleBox.currentIndex() == 1):
                method_info = inspect.getfullargspec(getattr(exposure, chosenMethod))
            elif (self.dlg.ModuleBox.currentIndex() == 2):
                method_info = inspect.getfullargspec(getattr(segmentation, chosenMethod))

        except TypeError:
            self.dlg.Parameters.setText("No arguments for chosen function")
        except AttributeError:
            pass
        # Gets the parameters for method
        return method_info

    # Updates the parameters for the chosen method
    def update_parameters(self):
        method_info = self.get_arguments_for_method()
        try:
            methodArguments = method_info.args
            # Prints out the parameters in the LineEdit window
            methodArgumentsString = "= , "
            self.dlg.Parameters.setText(methodArgumentsString.join(methodArguments) + "= ")
        except AttributeError:
            pass

    def select_output_file(self):
        filename, _filter = QFileDialog.getSaveFileName(
            self.dlg, "Select output file ", "", "*.tif")
        self.dlg.OutputFile.setText(filename)

    def method_function_call_helper(self, methodCalled, parameterList, imageArgument):
        # if (methodCalled == "median"):
        #     return my_median(imageArgument, parameterList)
        if (methodCalled == "slic"):
            return my_slic(imageArgument, parameterList)
        elif (methodCalled == "gaussian"):
            return my_gaussian(imageArgument, parameterList)
        elif (methodCalled == "sobel"):
            return my_sobel(imageArgument, parameterList)
        elif (methodCalled == "sobel_h"):
            return my_sobel_h(imageArgument, parameterList)
        elif (methodCalled == "sobel_v"):
            return my_sobel_v(imageArgument, parameterList)
        elif (methodCalled == "threshold_local"):
            return my_threshold_local(imageArgument, parameterList)
        elif (methodCalled == "threshold_otsu"):
            return my_threshold_otsu(imageArgument, parameterList)
        elif (methodCalled == "unsharp_mask"):
            return my_unsharp_mask(imageArgument, parameterList)
        elif (methodCalled == "quickshift"):
            return my_quickshift(imageArgument, parameterList)
        elif (methodCalled == "find_boundaries"):
            return my_find_boundaries(imageArgument, parameterList)
        elif (methodCalled == "chan_vese"):
            return my_chan_vese(imageArgument, parameterList)
        elif (methodCalled == "felzenszwalb"):
            return my_felzenszwalb(imageArgument, parameterList)
        elif (methodCalled == "inverse_gaussian_gradient"):
            return my_inverse_gaussian_gradient(imageArgument, parameterList)
        elif (methodCalled == "prewitt"):
            return my_prewitt(imageArgument, parameterList)
        elif (methodCalled == "prewitt_h"):
            return my_prewitt_h(imageArgument, parameterList)
        elif (methodCalled == "prewitt_v"):
            return my_prewitt_v(imageArgument, parameterList)
        elif (methodCalled == "adjust_gamma"):
            return my_adjust_gamma(imageArgument, parameterList)
        elif (methodCalled == "adjust_log"):
            return my_adjust_log(imageArgument, parameterList)
        elif (methodCalled == "adjust_sigmoid"):
            return my_adjust_sigmoid(imageArgument, parameterList)
        elif (methodCalled == "equalize_hist"):
            return my_equalize_hist(imageArgument, parameterList)
        elif (methodCalled == "laplace"):
            return my_laplace(imageArgument, parameterList)

    # Does stuff with the image
    def method_function_call(self, imageArgument):
        methodChosen = self.dlg.AvailableFunctionsBox.currentText()

        # Takes the user parameters
        parameterString = self.dlg.Parameters.text()

        # Gets the list of methods parameter names and their default values
        parameter_list = self.get_parameter_list()
        parameter_names = get_list_of_names(parameterString)
        parameter_values = get_list_of_values(parameterString)
        parameter_list = set_parameter_values(parameter_list, parameter_names, parameter_values)


        return self.method_function_call_helper(methodChosen, parameter_list, imageArgument)


    def get_save_file_name(self):
        saveString = self.dlg.OutputFile.text()
        fullFileName = re.findall("(\w+[.]\w+)", saveString)
        file_name = ""
        for i in range(len(fullFileName)):
            if (fullFileName[i] != '.'):
                file_name += fullFileName[i]
            elif (fullFileName[i] == '.'):
                return file_name

    def get_parameter_list(self):
        method_info = self.get_arguments_for_method()
        argument_names = method_info.args
        default_values = method_info.defaults
        arg_val_size_diff = len(argument_names) - len(default_values)
        parameter_list = []

        for x in range(len(argument_names)):
            parameter_list.append([])
            parameter_list[x].append(argument_names[x])

        for x in range(len(default_values)):
            parameter_list[x + arg_val_size_diff].append(default_values[x])

        return parameter_list

    def user_manual_window(self):
        self.user_manual.show()
        # Reads user manual txt and outputs all the information to user info
        dir_path = os.path.dirname(os.path.realpath(__file__))
        user_manual_info = open(dir_path + "\manual.txt", "r")

        for line in user_manual_info:
            self.user_manual.userInfo.addItem(line)

        self.user_manual.closeButton.clicked.connect(self.close_user_manual)


    def close_user_manual(self):
        self.user_manual.close()

    def image_processing(self, task, wait_time):
        file_name = self.dlg.OutputFile.text()

        # Reads the path of the chosen Raster layer/Image
        layers = QgsProject.instance().mapLayersByName(self.dlg.RasterLayerBox.currentText())
        layer_path = layers[0].dataProvider().dataSourceUri()
        im = imread(layer_path)
        gdalIm = gdal.Open(layer_path)

        # The path where the user wants to save the image

        x_pixels = im.shape[1]
        y_pixels = im.shape[0]
        driver = gdal.GetDriverByName('GTiff')
        ## TODO Make it so its possible to pass a grayscale image
        if (self.dlg.AvailableFunctionsBox.currentText() == "slic" or
                self.dlg.AvailableFunctionsBox.currentText() == "chan_vese" or
                self.dlg.AvailableFunctionsBox.currentText() == "felzenszwalb" or
                self.dlg.AvailableFunctionsBox.currentText() == "inverse_gaussian_gradient" or
                self.dlg.AvailableFunctionsBox.currentText() == "prewitt" or
                self.dlg.AvailableFunctionsBox.currentText() == "prewitt_h" or
                self.dlg.AvailableFunctionsBox.currentText() == "prewitt_v" or
                self.dlg.AvailableFunctionsBox.currentText() == "threshold_otsu" or
                self.dlg.AvailableFunctionsBox.currentText() == "threshold_local"):
            im = imread(layer_path, as_gray=True)
            dataset = driver.Create(file_name, x_pixels, y_pixels, 1, gdal.GDT_Int32)

            resultArray = self.method_function_call(im)
            if (type(resultArray) == str):
                raise Exception(resultArray)
            dataset.GetRasterBand(1).WriteArray(resultArray)

        if (self.dlg.AvailableFunctionsBox.currentText() == "median" or
                self.dlg.AvailableFunctionsBox.currentText() == "laplace" or
                self.dlg.AvailableFunctionsBox.currentText() == "gaussian" or
                self.dlg.AvailableFunctionsBox.currentText() == "sobel" or
                self.dlg.AvailableFunctionsBox.currentText() == "sobel_h" or
                self.dlg.AvailableFunctionsBox.currentText() == "sobel_v" or
                self.dlg.AvailableFunctionsBox.currentText() == "unsharp_mask" or
                self.dlg.AvailableFunctionsBox.currentText() == "clear_border" or
                self.dlg.AvailableFunctionsBox.currentText() == "find_boundaries" or
                self.dlg.AvailableFunctionsBox.currentText() == "adjust_gamma" or
                self.dlg.AvailableFunctionsBox.currentText() == "adjust_log" or
                self.dlg.AvailableFunctionsBox.currentText() == "adjust_sigmoid" or
                self.dlg.AvailableFunctionsBox.currentText() == "equalize_hist"):
            if (im.ndim == 3):
                dataset = driver.Create(file_name, x_pixels, y_pixels, 3, gdal.GDT_Int32)

                resultArray_r = self.method_function_call(im[:, :, 0])
                resultArray_g = self.method_function_call(im[:, :, 1])
                resultArray_b = self.method_function_call(im[:, :, 2])

                if (type(resultArray_r) == str or type(resultArray_g) == str or type(resultArray_b) == str):
                    raise Exception(resultArray_r)

                dataset.GetRasterBand(1).WriteArray(resultArray_r)
                dataset.GetRasterBand(2).WriteArray(resultArray_g)
                dataset.GetRasterBand(3).WriteArray(resultArray_b)
            else:
                dataset = driver.Create(file_name, x_pixels, y_pixels, 1, gdal.GDT_Int32)
                resultArray = self.method_function_call(im)
                dataset.GetRasterBand(1).WriteArray(resultArray)

        if (self.dlg.AvailableFunctionsBox.currentText() == "quickshift"):
            dataset = driver.Create(file_name, x_pixels, y_pixels, 1, gdal.GDT_Int32)

            resultArray = self.method_function_call(im)
            if (type(resultArray) == str):
                raise Exception(resultArray)
            dataset.GetRasterBand(1).WriteArray(resultArray)

        proj = gdalIm.GetProjection()

        # If the chosen layer has a projection then add that, to the processed image
        if proj != "":
            geotrans = gdalIm.GetGeoTransform()
            dataset.SetProjection(proj)
            dataset.SetGeoTransform(geotrans)
        dataset.FlushCache()

        if (task.isCanceled):
            self.stopped(task)
            return file_name

    def run(self):
        """Run method that performs all the real work"""

        # List of options for modules
        modules = ["filters", "exposure", "segmentation"]
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = getMedianFunctionsDialog()
            self.user_manual = userManualDialog()

            self.dlg.ModuleBox.currentIndexChanged.connect(self.update_function_list)
            self.dlg.pushButton.clicked.connect(self.select_output_file)
            self.dlg.AvailableFunctionsBox.currentIndexChanged.connect(self.update_parameters)
            self.dlg.AvailableFunctionsBox.currentIndexChanged.connect(self.update_info_box)
            self.dlg.UserManualButton.clicked.connect(self.user_manual_window)

        # Fetch the currently loaded layers
        layers = QgsProject.instance().layerTreeRoot().children()

        # Clear the contents of the comboBoxes from previous runs
        self.dlg.RasterLayerBox.clear()
        self.dlg.ModuleBox.clear()
        self.dlg.AvailableFunctionsBox.clear()
        self.dlg.OutputFile.clear()

        # Populate the comboBox with names of all the loaded layers
        self.dlg.RasterLayerBox.addItems([layer.name() for layer in layers])

        # Clears and fills the Module box with options available for user
        self.dlg.ModuleBox.addItems(modules)
        self.update_function_list()
        self.update_info_box()
        self.update_parameters()

        # show the dialog
        self.dlg.show()

        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed
        if result:
            task = QgsTask.fromFunction("Image processing", self.image_processing, on_finished=self.completed, wait_time=3)
            self.tm.addTask(task)
