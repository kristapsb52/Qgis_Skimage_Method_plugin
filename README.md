#Qgis Skimage(Scikit-image) method plugin

### This plugin uses Scikit-image methods to process images and is used for GeoTiff images only

Necessary packages for this plugins use:
    * scikit-image

(It is assumed that the user has Qgis 3.8 or newer version installed)

To install the package open OSGeo4W Shell as an administrator and write:
> py3_env
>
> python -m pip install scikit-image

To upload the plugin to QGIS:
* Open QGIS and in the toolbar menu click Settings -> User Profiles -> Open Active Profile Folder
* Open python folder:
    #### If you do not have a folder called "plugins" then create one
    ##### (For the next step make sure that Qgis is closed)
    * open folder called "plugins" and download the git repository there
    * If the repository was downloaded through zip then extract it there
* After it has been downloaded, in QGIS go to Plugins -> Manage and Install Plugins... ->
go to Installed and mark the checkbox for "get Median Functions"
* After all these steps have been done, reload QGIS and enjoy the plugin!
    * If the plugin wasn't installed then try adding it as zip, to do that follow these instructions:
    * Download the plugin from github as a zip file (Click on "Code" -> Download ZIP)
    * Open QGIS and in the toolbar click "Plugins" -> "Manage and install plugins" -> "Install from ZIP"
    -> Locate the installed zip and install the plugin to QGIS