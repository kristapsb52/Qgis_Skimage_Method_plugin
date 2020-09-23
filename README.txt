Qgis Skimage(Scikit-image) method plugin

This plugin uses Scikit-image methods to process images

Necessary packages for this plugins use:
    * scikit-image

(It is assumed that the user has Qgis 3.8 installed)
To install the package open OSGeo4W Shell as an administrator and write:

>> python -m pip install scikit-image

To upload the plugin to QGIS:
* Open QGIS and in the toolbar menu click Settings -> User Profiles -> Open Active Profile Folder
* Open python folder:
    ** If you do not have a folder called "plugins" then create one **
    -> open folder called "plugins" and download the git repository there
* After it has been downloaded, in QGIS go to Plugins -> Manage and Install Plugins... ->
go to Installed and mark the checkbox for "get Median Functions"
* After all these steps have been done, reload QGIS and enjoy the plugin!