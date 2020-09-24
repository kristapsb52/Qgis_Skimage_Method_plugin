from skimage import filters, morphology, segmentation
from skimage.morphology import disk
from qgis.PyQt.QtWidgets import QMessageBox
import re
# TODO change the names of my... methods


# Returns a list of parameter names
def get_list_of_names(parameter_string):
    tempList = re.findall("\w+=", parameter_string)
    for x in range(len(tempList)):
        tempList[x] = tempList[x].replace('=', '')

    return tempList


# Returns a list of parameter values
def get_list_of_values(parameter_string):
    resultList = []
    tempString = ""
    startOfParameter = False
    for x in range(len(parameter_string)):
        if (parameter_string[x] == ','):
            startOfParameter = False
            resultList.append(tempString)
            tempString = ""
        if (startOfParameter):
            tempString += parameter_string[x]
            if (x == len(parameter_string) - 1):
                resultList.append(tempString)
        if (parameter_string[x] == '='):
            startOfParameter = True
            if (parameter_string[x + 1] == " "):
                x += 1

    return resultList

# The method skips the first element since its not an actual value. The image is read from a path
# which is then passed as a value
def set_parameter_values(included_parameters, parameter_names, parameter_values):
    for i in range(1, len(parameter_names)):
        for j in range(1, len(included_parameters)):
            if (parameter_names[i] == included_parameters[j][0]):
                included_parameters[j][1] = parameter_values[i]
                break

    return included_parameters


## Calls Segmentation functions
# Calls clear_border method
def my_clear_border(image_value, parameter_list):

    param_buffer_size = int(parameter_list[0][1])

    result = segmentation.clear_border(labels=image_value, buffer_size=param_buffer_size,
                                       bgval=parameter_list[1][1], in_place=parameter_list[2][1],
                                       mask= parameter_list[3][1])

    return result


# Calls find_boundaries method
def my_find_boundaries(image_value, parameter_list):

    # TODO make an array that is used for this method

    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    try:
        if (parameter_names_string.find("connectivity") != -1):
            parameter_list[1][1] = int(parameter_list[1][1])
        if (parameter_names_string.find("background") != -1):
            parameter_list[3][1] = int(parameter_list[3][1])
        result = segmentation.find_boundaries(label_img=image_value, connectivity=parameter_list[1][1],
                                          mode=parameter_list[2][1], background=parameter_list[3][1])

    except:
        QMessageBox.critical(None, "test", "The data type for parameters was incorrect!")
    return result


# Calls quickshift method
def my_quickshift(image_value, parameter_list):

    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    try:
        if (parameter_names_string.find("ratio") != -1):
            parameter_list[1][1] = float(parameter_list[1][1])
        if (parameter_names_string.find("kernel_size") != -1):
            parameter_list[2][1] = int(parameter_list[2][1])
        if (parameter_names_string.find("max_dist") != -1):
            parameter_list[3][1] = int(parameter_list[3][1])
        if (parameter_names_string.find("return_tree") != -1):
            parameter_list[4][1] = bool(parameter_list[4][1])
        if (parameter_names_string.find("sigma") != -1):
            parameter_list[5][1] = int(parameter_list[5][1])
        if (parameter_names_string.find("convert2lab") != -1):
            parameter_list[6][1] = bool(parameter_list[6][1])
        if (parameter_names_string.find("random_seed") != -1):
            parameter_list[7][1] = int(parameter_list[7][1])

        result = segmentation.quickshift(image=image_value, ratio=parameter_list[1][1], kernel_size=parameter_list[2][1],
                                     max_dist=parameter_list[3][1], return_tree=parameter_list[4][1], sigma=parameter_list[5][1],
                                     convert2lab=parameter_list[6][1], random_seed=parameter_list[7][1])
    except:
        QMessageBox.critical(None, "test", "The data type for parameters was incorrect!")
    return result


# Calls slic method
def my_slic(image_value, parameter_list):
    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    ## If the values were changed parse the values from included parameters string to int
    try:
        if (parameter_names_string.find("n_segments") != -1):
            parameter_list[1][1] = int(parameter_list[1][1])
        if (parameter_names_string.find("compactness") != -1):
            parameter_list[2][1] = float(parameter_list[2][1])
        if (parameter_names_string.find("max_iter") != -1):
            parameter_list[3][1] = int(parameter_list[3][1])
        if (parameter_names_string.find("sigma") != -1):
            parameter_list[4][1] = int(parameter_list[4][1])
        if (parameter_names_string.find("min_size_factor") != -1):
            parameter_list[9][1] = float(parameter_list[9][1])
        if (parameter_names_string.find("max_size_factor") != -1):
            parameter_list[10][1] = int(parameter_list[10][1])

        QMessageBox.information(None, "Test", str(parameter_list))

        result = segmentation.slic(image=image_value, n_segments=parameter_list[1][1],
                                   compactness=parameter_list[2][1], max_iter=parameter_list[3][1],
                                   sigma=parameter_list[4][1], spacing=parameter_list[5][1],
                                   multichannel=parameter_list[6][1], convert2lab=parameter_list[7][1],
                                   enforce_connectivity=parameter_list[8][1], min_size_factor=parameter_list[9][1],
                                   max_size_factor=parameter_list[10][1], slic_zero=parameter_list[11][1])
    except:
        QMessageBox.critical(None, "test", "The data type for parameters was incorrect!")

    return result


## Calls Filters functions
# Calls gaussian method
def my_gaussian(image_value, parameter_list):



    param_cval = parameter_list[4][1]
    param_truncate = parameter_list[7][1]
    param_multichannel = parameter_list[5][1]

    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    try:
        param_sigma = int(parameter_list[1][1])
        if (parameter_names_string.find("cval") != -1):
            param_cval = int(parameter_list[4][1])
        if (parameter_names_string.find("truncate") != -1):
            param_truncate = float(parameter_list[7][1])
        if (parameter_names_string.find("multichannel") != -1):
            param_multichannel = bool(parameter_list[5][1])

        result = filters.gaussian(image=image_value, sigma=param_sigma, output=parameter_list[2][1],
                                  mode=parameter_list[3][1], cval=param_cval, multichannel=param_multichannel,
                                  preserve_range=parameter_list[6][1], truncate=param_truncate)
    except:
        QMessageBox.critical(None, "test", "The data type for parameters was incorrect!")

    return result * 100


# Calls laplace method
def my_laplace(image_value, parameter_list):

    try:
        param_ksize = int(parameter_list[0][1])

        result = filters.laplace(image=image_value, ksize=param_ksize, mask=parameter_list[1][1])
    except:
        QMessageBox.critical(None, "test", "The data type for parameters was incorrect!")

    return result


# Calls Median method
def my_median(image_value, parameter_list):

    try:
        cvalStringToInt = int(parameter_list[4][1])
        selemStringToInt = int(parameter_list[1][1])

        result = filters.median(image=image_value, selem=disk(selemStringToInt), mode=parameter_list[3][1],
                                cval=cvalStringToInt,
                                behavior=parameter_list[5][1])
    except:
        QMessageBox.critical(None, "test", "The data type for parameters was incorrect!")

    return result


# Calls Sobel method
def my_sobel(image_value, parameter_list):
    try:
        result = filters.sobel(image=image_value, mask=parameter_list[1][1])
    except:
        QMessageBox.critical(None, "test", "The data type for parameters was incorrect!")

    return result * 100


# Calls Sobel_h method
def my_sobel_h(image_value, parameter_list):
    try:
        result = filters.sobel_h(image=image_value, mask=parameter_list[1][1])
    except:
        QMessageBox.critical(None, "test", "The data type for parameters was incorrect!")
    return result * 100


# Calls Sobel_v method
def my_sobel_v(image_value, parameter_list):

    try:
        result = filters.sobel_h(image=image_value, mask=parameter_list[1][1])
    except:
        QMessageBox.critical(None, "test", "The data type for parameters was incorrect!")

    return result * 100


# Calls threshold_local method
def my_threshold_local(image_value, parameter_list):
    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    try:
        param_block_size = int(parameter_list[1][1])

        if(parameter_names_string.find("offset") != -1):
            parameter_list[3][1] = float(parameter_list[3][1])
        if(parameter_names_string.find("param") != -1):
            parameter_list[5][1] = int(parameter_list[5][1])
        if(parameter_names_string.find("cval") != -1):
            parameter_list[6][1] = float(parameter_list[6][1])

        result = image_value > filters.threshold_local(image=image_value, block_size=param_block_size, method=parameter_list[2][1],
                                         offset=parameter_list[3][1], mode=parameter_list[4][1],
                                         param=parameter_list[5][1],
                                         cval=parameter_list[6][1])
    except:
        QMessageBox.critical(None, "test", "The data type for parameters was incorrect!")

    return result


# Calls threshold_otsu method
def my_threshold_otsu(image_value, parameter_list):
    result = image_value <= filters.threshold_otsu(image_value)
    return result

# Calls unsharp_mask method
def my_unsharp_mask(image_value, parameter_list):

    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    try:
        param_radius = parameter_list[1][1]
        param_amount = parameter_list[2][1]

        if (parameter_names_string.find("radius") != -1):
            param_radius = float(parameter_list[1][1])
        if (parameter_names_string.find("amount") != -1):
            param_amount = float(parameter_list[2][1])

        result = filters.unsharp_mask(image=image_value, radius=param_radius, amount=param_amount,
                                      multichannel=parameter_list[3][1], preserve_range=parameter_list[4][1])
    except:
        QMessageBox.critical(None, "test", "The data type for parameters was incorrect!")

    return result * 100