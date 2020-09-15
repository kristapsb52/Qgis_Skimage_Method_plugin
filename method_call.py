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
    included_parameters = [["n_segments", True], ["compactness", 10.], ["max_iter", 10], ["sigma", 0], ["spacing", None], ["multichannel", True], ["convert2lab", None],
                           ["enforce_connectivity", True], ["min_size_factor", 0.5], ["max_size_factor", 3], ["slic_zero", False]]

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

    QMessageBox.information(None, "Test", str(included_parameters))
    result = segmentation.slic(image=image_value, n_segments=segments_string_to_int,
                            compactness=param_compactness, max_iter=param_max_iter,
                            sigma=param_sigma, spacing=included_parameters[4][1],
                            multichannel=included_parameters[5][1], convert2lab=included_parameters[6][1],
                            enforce_connectivity=included_parameters[7][1], min_size_factor=param_min_size_factor,
                            max_size_factor=param_max_size_factor, slic_zero=included_parameters[10][1])

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