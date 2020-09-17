from skimage import filters, morphology, segmentation
from skimage.morphology import disk
from qgis.PyQt.QtWidgets import QMessageBox
import re
import numpy as np
import median_functions


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

def get_parameter_list():
    method_info = median_functions.getMedianFunctions.get_arguments_for_method()
    argument_names = method_info.args
    default_values = method_info.defaults
    arg_val_size_diff = len(argument_names) - len(default_values)
    parameter_list = []

    for x in range(len(argument_names)):
        parameter_list.append([])
        parameter_list[x].append(argument_names[x])

    for x in range(len(default_values)):
        parameter_list[x+arg_val_size_diff].append(default_values[x])

    return parameter_list
# TODO every function has the same logic, but the parameters are different, OPTIMIZE THE CODE
# TODO check if user inputed the correct type for parameters, if not then throw a QGIS error box with info
def set_parameter_values(included_parameters, parameter_names, parameter_values):
    for i in range(len(parameter_names)):
        for j in range(len(included_parameters)):
            if (parameter_names[i] == included_parameters[j][0]):
                included_parameters[j][1] = parameter_values[i]
                break

    return included_parameters


## Calls Segmentation functions
# Calls clear_border method
def my_clear_border(image_value, parameter_string):
    parameter_names = get_list_of_names(parameter_string)
    parameter_values = get_list_of_values(parameter_string)
    included_parameters = get_parameter_list()

    included_parameters = set_parameter_values(included_parameters, parameter_names, parameter_values)

    param_buffer_size = int(included_parameters[0][1])

    result = segmentation.clear_border(labels=image_value, buffer_size=param_buffer_size,
                                       bgval=included_parameters[1][1], in_place=included_parameters[2][1],
                                       mask= included_parameters[3][1])

    return result


# Calls find_boundaries method
def my_find_boundaries():
    pass
    # result = segmentation.find_boundaries(label_img= , connectivity=, mode= , background=)

    # return result


# Calls quickshift method
def my_quickshift(image_value, parameter_string):
    parameter_names = get_list_of_names(parameter_string)
    parameter_values = get_list_of_values(parameter_string)
    included_parameters = get_parameter_list()

    included_parameters = set_parameter_values(included_parameters, parameter_names, parameter_values)

    result = segmentation.quickshift(image=image_value, ratio=included_parameters[0][1], kernel_size=included_parameters[1][1],
                                     max_dist=included_parameters[2][1], return_tree=included_parameters[3][1], sigma=included_parameters[4][1],
                                     convert2lab=included_parameters[5][1], random_seed=[6][1])

    return result


# Calls slic method
def my_slic(image_value, parameter_string):
    parameter_names = get_list_of_names(parameter_string)
    parameter_values = get_list_of_values(parameter_string)
    included_parameters = get_parameter_list()

    included_parameters = set_parameter_values(included_parameters, parameter_names, parameter_values)
    segments_string_to_int = int(included_parameters[0][1])
    parameter_names_string = ""
    parameter_names_string = parameter_names_string.join(parameter_names)
    ## If the values were changed parse the values from included parameters string to int
    param_compactness = included_parameters[1][1]
    param_max_iter = included_parameters[2][1]
    param_sigma = included_parameters[3][1]
    param_min_size_factor = included_parameters[8][1]
    param_max_size_factor = included_parameters[9][1]

    if (parameter_names_string.find("compactness") != -1):
        param_compactness = float(included_parameters[1][1])
    if (parameter_names_string.find("max_iter") != -1):
        param_max_iter = int(included_parameters[2][1])
    if (parameter_names_string.find("sigma") != -1):
        param_sigma = int(included_parameters[3][1])
    if (parameter_names_string.find("min_size_factor") != -1):
        param_min_size_factor = float(included_parameters[8][1])
    if (parameter_names_string.find("max_size_factor") != -1):
        param_max_size_factor = int(included_parameters[9][1])

    result = segmentation.slic(image=image_value, n_segments=segments_string_to_int,
                               compactness=param_compactness, max_iter=param_max_iter,
                               sigma=param_sigma, spacing=included_parameters[4][1],
                               multichannel=included_parameters[5][1], convert2lab=included_parameters[6][1],
                               enforce_connectivity=included_parameters[7][1], min_size_factor=param_min_size_factor,
                               max_size_factor=param_max_size_factor, slic_zero=included_parameters[10][1])

    return result


## Calls Filters functions
# Calls gaussian method
def my_gaussian(image_value, parameter_string):
    parameter_names = get_list_of_names(parameter_string)
    parameter_values = get_list_of_values(parameter_string)
    included_parameters = get_parameter_list()

    included_parameters = set_parameter_values(included_parameters, parameter_names, parameter_values)

    param_sigma = int(included_parameters[0][1])
    param_cval = included_parameters[3][1]
    param_truncate = included_parameters[6][1]
    param_multichannel = included_parameters[4][1]

    parameter_names_string = ""
    parameter_names_string = parameter_names_string.join(parameter_names)
    if (parameter_names_string.find("cval") != -1):
        param_cval = int(included_parameters[3][1])
    if (parameter_names_string.find("truncate") != -1):
        param_truncate = float(included_parameters[6][1])
    if (parameter_names_string.find("multichannel") != -1):
        param_multichannel = bool(included_parameters[4][1])

    result = filters.gaussian(image=image_value, sigma=param_sigma, output=included_parameters[1][1],
                              mode=included_parameters[2][1], cval=param_cval, multichannel=param_multichannel,
                              preserve_range=included_parameters[5][1], truncate=param_truncate)

    return result * 100


# Calls laplace method
def my_laplace(image_value, parameter_string):
    parameter_values = get_list_of_values(parameter_string)
    parameter_names = get_list_of_names(parameter_string)
    included_parameters = get_parameter_list()

    included_parameters = set_parameter_values(included_parameters, parameter_names, parameter_values)

    param_ksize = int(included_parameters[0][1])

    result = filters.laplace(image=image_value, ksize=param_ksize, mask=included_parameters[1][1])

    return result


# Calls Median method
def my_median(image_value, parameter_string):
    parameter_names = get_list_of_names(parameter_string)
    parameter_values = get_list_of_values(parameter_string)
    included_parameters = get_parameter_list()

    included_parameters = set_parameter_values(included_parameters, parameter_names, parameter_values)

    cvalStringToInt = int(included_parameters[3][1])
    selemStringToInt = int(included_parameters[0][1])

    result = filters.median(image=image_value, selem=disk(selemStringToInt), mode=included_parameters[2][1],
                            cval=cvalStringToInt,
                            behavior=included_parameters[4][1])

    return result


# Calls Sobel method
def my_sobel(image_value, parameter_string):
    parameter_names = get_list_of_names(parameter_string)
    parameter_values = get_list_of_values(parameter_string)
    included_parameters = get_parameter_list()

    ## mask is an array of bool
    included_parameters = set_parameter_values(included_parameters, parameter_names, parameter_values)

    result = filters.sobel(image=image_value, mask=included_parameters[0][1])

    return result * 100


# Calls Sobel_h method
def my_sobel_h(image_value, parameter_string):
    parameter_names = get_list_of_names(parameter_string)
    parameter_values = get_list_of_values(parameter_string)
    included_parameters = get_parameter_list()

    ## mask is an array of bool
    included_parameters = set_parameter_values(included_parameters, parameter_names, parameter_values)

    result = filters.sobel_h(image=image_value, mask=included_parameters[0][1])

    return result * 100


# Calls Sobel_v method
def my_sobel_v(image_value, parameter_string):
    parameter_names = get_list_of_names(parameter_string)
    parameter_values = get_list_of_values(parameter_string)
    included_parameters = get_parameter_list()

    ## mask is an array of bool
    included_parameters = set_parameter_values(included_parameters, parameter_names, parameter_values)

    result = filters.sobel_h(image=image_value, mask=included_parameters[0][1])

    return result * 100


# Calls threshold_local method
def my_threshold_local(image_value, parameter_string):
    parameter_names = get_list_of_names(parameter_string)
    parameter_values = get_list_of_values(parameter_string)
    included_parameters = get_parameter_list()

    included_parameters = set_parameter_values(included_parameters, parameter_names, parameter_values)
    param_block_size = int(included_parameters[0][1])

    result = image_value > filters.threshold_local(image=image_value, block_size=param_block_size, method=included_parameters[1][1],
                                     offset=included_parameters[2][1], mode=included_parameters[3][1],
                                     param=included_parameters[4][1],
                                     cval=included_parameters[5][1])

    return result


# Calls threshold_otsu method
def my_threshold_otsu(image_value, parameter_string):
    result = image_value <= filters.threshold_otsu(image_value)
    return result

# Calls unsharp_mask method
def my_unsharp_mask(image_value, parameter_string):
    parameter_names = get_list_of_names(parameter_string)
    parameter_values = get_list_of_values(parameter_string)
    included_parameters = get_parameter_list()

    included_parameters = set_parameter_values(included_parameters, parameter_names, parameter_values)

    parameter_names_string = ""
    parameter_names_string = parameter_names_string.join(parameter_names)

    param_radius = included_parameters[0][1]
    param_amount = included_parameters[1][1]

    if (parameter_names_string.find("radius") != -1):
        param_radius = float(included_parameters[0][1])
    if (parameter_names_string.find("amount") != -1):
        param_amount = float(included_parameters[1][1])

    result = filters.unsharp_mask(image=image_value, radius=param_radius, amount=param_amount,
                                  multichannel=included_parameters[2][1], preserve_range=included_parameters[3][1])

    return result * 100