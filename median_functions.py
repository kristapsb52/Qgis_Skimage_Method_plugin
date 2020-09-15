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
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.core import QgsProject, QgsRasterFileWriter, QgsRasterPipe, Qgis, QgsMessageLog, QgsRasterLayer
from qgis.utils import iface
from qgis.gui import QgisInterface

# Skimage imports
from skimage import morphology
from skimage import segmentation
from skimage import filters
from skimage.io import imread
from skimage.morphology import disk
# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the dialog
from .median_functions_dialog import getMedianFunctionsDialog

import numpy as np
import os.path
import inspect
import re
import gdal
from .method_call import *

class getMedianFunctions:
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
            'getMedianFunctions_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&get Median Functions')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

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
        return QCoreApplication.translate('getMedianFunctions', message)


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
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/median_functions/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'get Module Functions'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        file_path = self.dlg.OutputFile.text()
        file_name = self.get_save_file_name()

        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&get Median Functions'),
                action)
            self.iface.removeToolBarIcon(action)


        # Method 1
        iface.addRasterLayer(file_path, file_name)

        # Method 2
        #rlayer = QgsRasterLayer(file_path, file_name)
        #QgsProject.instance().addMapLayer(rlayer)


    # Updates the method list for the chosen module
    def update_function_list(self):
        self.dlg.AvailableFunctionsBox.clear()
        # Reads file that has all the methods
        method_file = open("C:/users/nils/desktop/kristaps/qgis_data/method_list.txt", "r")

        # Reads the chosen module
        chosen_method = ""
        if(self.dlg.ModuleBox.currentIndex == 0):
            chosen_method = "Filter"
        elif (self.dlg.ModuleBox.currentIndex() == 1):
            chosen_method = "Morphology"
        elif (self.dlg.ModuleBox.currentIndex() == 2):
            chosen_method = "Segmentation"

        # Reads all the methods for the user chosen module
        allmethods = []
        methodFound = False
        for line in method_file:
            if(methodFound):
                if(line == "\n"):
                    break
                allmethods.append(line)
            if(line == chosen_method + "\n"):
                methodFound = True

        method_file.close()

        for x in range(len(allmethods)):
            allmethods[x] = allmethods[x].replace('\n', '')

        self.dlg.AvailableFunctionsBox.addItems(allmethods)

    def get_arguments_for_method(self):
        # Gets the chosen method
        chosenMethod = self.dlg.AvailableFunctionsBox.currentText()

        try:
            methodParameters = inspect.getfullargspec(getattr(filters, chosenMethod))
        except TypeError:
            self.dlg.Parameters.setText("No arguments for chosen function")
        except:
            if (self.dlg.ModuleBox.currentIndex() == 0):
                methodParameters = inspect.getfullargspec(getattr(filters, chosenMethod))
            elif (self.dlg.ModuleBox.currentIndex() == 1):
                methodParameters = inspect.getfullargspec(getattr(morphology, chosenMethod))
            elif (self.dlg.ModuleBox.currentIndex() == 2):
                methodParameters = inspect.getfullargspec(getattr(segmentation, chosenMethod))
        # Gets the parameters for method
        methodArguments = methodParameters.args

        # Sets arguments to String
        methodArgumentsString = "= , "
        return methodArgumentsString.join(methodArguments) + "= "

    # Updates the parameters for the chosen method
    def update_parameters(self):
        methodArgumentsString = self.get_arguments_for_method()
        # Prints out the parameters in the LineEdit window
        self.dlg.Parameters.setText(methodArgumentsString)

    def select_output_file(self):
        filename, _filter = QFileDialog.getSaveFileName(
            self.dlg, "Select output file ", "", "*.tif")
        self.dlg.OutputFile.setText(filename)

    # It is assumed that the biggest argument count for a method is 7
    def method_function_call_helper(self, methodCalled, parameterList, imageArgument):
        if (methodCalled == "median"):
            return my_median(imageArgument, parameterList)
        elif (methodCalled == "slic"):
            return my_slic(imageArgument, parameterList)

    def get_list_from_user_parameters(self):
        stringList = []

        parameterString = str(self.dlg.Parameters.text())
        tempArgument = ""
        for x in range(len(parameterString)):
            if(parameterString[x] != ','):
                tempArgument += parameterString[x]
            elif (parameterString[x] == ',' or x == len(parameterString)-1 ):
                stringList.append(tempArgument)
                tempArgument = ""
                x += 1

        return stringList

    # Does stuff with the image
    def method_function_call(self, imageArgument):
        methodChosen = self.dlg.AvailableFunctionsBox.currentText()
        # Takes the user parameters
        parameterList = self.dlg.Parameters.text()

        # Finds which method to use
        # Module is filters
        if (self.dlg.ModuleBox.currentIndex() == 0):
            functionToCall = self.method_function_call_helper(methodChosen, parameterList, imageArgument)

        # Module is morphology
        elif (self.dlg.ModuleBox.currentIndex() == 1):
            functionToCall = self.method_function_call_helper(methodChosen, parameterList, imageArgument)

        # Module is segmentation
        elif (self.dlg.ModuleBox.currentIndex() == 2):
            functionToCall = self.method_function_call_helper(methodChosen, parameterList, imageArgument)

        # Should return a numpy array of 2D or 3D
        return functionToCall

    def get_save_file_name(self):
        saveString = self.dlg.OutputFile.text()
        fullFileName = re.findall("(\w+[.]\w+)", saveString)
        file_name = ""
        for i in range(len(fullFileName)):
            if(fullFileName[i] != '.'):
                file_name += fullFileName[i]
            elif(fullFileName[i] == '.'):
                return file_name


    def run(self):
        """Run method that performs all the real work"""

        # List of options for modules
        modules = ["filters", "morphology", "segmentation"]
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = getMedianFunctionsDialog()
            self.dlg.ModuleBox.currentIndexChanged.connect(self.update_function_list)
            self.dlg.pushButton.clicked.connect(self.select_output_file)
            self.dlg.AvailableFunctionsBox.currentIndexChanged.connect(self.update_parameters)

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

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed
        if result:
            im = imread("C:/users/nils/Downloads/" + self.dlg.RasterLayerBox.currentText() + ".tif")
            gdalIm = gdal.Open("C:/users/nils/Downloads/" + self.dlg.RasterLayerBox.currentText() + ".tif")

            # The path where the user wants to save the image
            file_name = self.dlg.OutputFile.text()
            x_pixels = im.shape[0]
            y_pixels = im.shape[1]

            driver = gdal.GetDriverByName('GTiff')
            #dataset = driver.Create(file_name, x_pixels, y_pixels, 3, gdal.GDT_Int32)

            # Get the arguments for method to check if image is included
            methodArguments = self.get_arguments_for_method()
            isImageIncluded = re.search("image", methodArguments)

            # If image is included
            if (isImageIncluded):
                # Convert the image to a 2d array
                if(self.dlg.AvailableFunctionsBox.currentText() == "slic"):
                    dataset = driver.Create(file_name, x_pixels, y_pixels, 1, gdal.GDT_Int32)
                    resultArray = self.method_function_call(im)

                    dataset.GetRasterBand(1).WriteArray(resultArray)

                if(self.dlg.AvailableFunctionsBox.currentText() == "median"):
                    dataset = driver.Create(file_name, x_pixels, y_pixels, 3, gdal.GDT_Int32)
                    im_r = im[:,:,0]
                    im_g = im[:,:,1]
                    im_b = im[:,:,2]

                    resultArray_r = self.method_function_call(im_r)
                    resultArray_g = self.method_function_call(im_g)
                    resultArray_b = self.method_function_call(im_b)

                    dataset.GetRasterBand(1).WriteArray(resultArray_r)
                    dataset.GetRasterBand(2).WriteArray(resultArray_g)
                    dataset.GetRasterBand(3).WriteArray(resultArray_b)

                geotrans = gdalIm.GetGeoTransform()
                proj = gdalIm.GetProjection()
                dataset.SetGeoTransform(geotrans)
                dataset.SetProjection(proj)
                dataset.FlushCache()

            # If image isn't included
            else:
                # Do nothing for now
                pass

            #if not rlayer.isValid():
            #    QMessageBox.information(None, "Test", "Layer failed to load")

            self.iface.messageBar().pushMessage(
                "Success", "Output file written at " + file_name,
                level=Qgis.Success, duration=3
            )

######################################################
######################################################
######################################################
######################################################

