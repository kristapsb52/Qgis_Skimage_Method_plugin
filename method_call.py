from skimage import filters, morphology, segmentation
from skimage.morphology import disk
from qgis.PyQt.QtWidgets import QMessageBox
import re

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

def set_parameter_values(included_parameters, parameter_names, parameter_values):
    for i in range(len(parameter_names)):
        for j in range(len(included_parameters)):
            if (parameter_names[i] == included_parameters[j][0]):
                included_parameters[j][1] = parameter_values[i]
                break

    return included_parameters

## Calls Segmentation functions
# Calls clear_border method
def my_clear_border():
    pass
    # result = segmentation.clear_border(labels= , buffer_size=, bgval= , in_place= , mask=)

    # return result


# Calls find_boundaries method
def my_find_boundaries():
    pass
    # result = segmentation.find_boundaries(label_img= , connectivity=, mode= , background=)

    # return result


# Calls quickshift method
def my_quickshift():
    pass
    # result = segmentation.quickshift(image= , ratio= , kernel_size= , max_dist= , return_tree= , sigma= , convert2lab= , random_seed=)

    # return result


# Calls slic method
def my_slic(image_value, parameter_string):
    parameter_names = get_list_of_names(parameter_string)
    parameter_values = get_list_of_values(parameter_string)
    included_parameters = [["n_segments", True], ["compactness", True], ["max_iter", True], ["sigma", True], ["spacing", None], ["multichannel", True], ["convert2lab", None],
                           ["enforce_connectivity", True], ["min_size_factor", True], ["max_size_factor", True], ["slic_zero", False]]

    included_parameters = set_parameter_values(included_parameters, parameter_names, parameter_values)
    QMessageBox.information(None, "Test", str(included_parameters))
    segments_string_to_int = int(included_parameters[0][1])

    result = segmentation.slic(image_value, segments_string_to_int, included_parameters[1][1], included_parameters[2][1], included_parameters[3][1], included_parameters[4][1],
                               included_parameters[5][1], included_parameters[6][1], included_parameters[7][1], included_parameters[8][1], included_parameters[9][1],
                               included_parameters[10][1])


    return result

## Calls Filters functions
# Calls gaussian method

# Calls laplace method

# Calls Median method
def my_median(image_value, parameter_string):
    parameter_names = get_list_of_names(parameter_string)
    parameter_values = get_list_of_values(parameter_string)
    included_parameters = [["selem", True], ["out", True], ["mode", True], ["cval", True], ["behavior", True]]

    included_parameters = set_parameter_values(included_parameters, parameter_names, parameter_values)

    cvalStringToInt = int(included_parameters[3][1])
    selemStringToInt = int(included_parameters[0][1])

    result = filters.median(image=image_value, selem=disk(selemStringToInt), mode=included_parameters[2][1],
                            cval=cvalStringToInt,
                            behavior=included_parameters[4][1])

    return result
# Calls Sobel method

# Calls Sobel_v method

# Calls Sobel_h method

# Calls threshold_local method

# Calls threshold_otsu method

# Calls unsharp_mask method