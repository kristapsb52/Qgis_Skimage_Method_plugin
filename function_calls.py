from skimage import segmentation
from skimage import filters

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
        if( parameter_string[x] == ','):
            startOfParameter = False
            resultList.append(tempString)
            tempString = ""
        if(startOfParameter):
            tempString += parameter_string[x]
            if ( x == len(parameter_string) - 1):
                resultList.append(tempString)
        if( parameter_string == '='):
            startOfParameter = True
            x += 1

    return resultList

## Calls Segmentation functions
# Calls clear_border method
def my_clear_border():

    result = segmentation.clear_border(labels= , buffer_size=, bgval= , in_place= , mask=)

    return result
# Calls find_boundaries method
def my_find_boundaries():

    result = segmentation.find_boundaries(label_img= , connectivity=, mode= , background=)

    return result
# Calls quickshift method
def my_quickshift():

    result = segmentation.quickshift(image= , ratio= , kernel_size= , max_dist= , return_tree= , sigma= , convert2lab= , random_seed=)

    return result
# Calls slic method
def my_slic():

    result = segmentation.slic(image= , n_segments= , compactness= , max_iter= , sigma= , spacing= , multichannel= , convert2lab= ,
                               enforce_connectivity= ,min_size_factor= , max_size_factor= , slic_zero=)

    return result

## Calls Filters functions
# Calls gaussian method

# Calls laplace method

# Calls Median method
def my_median():

    result = filters.median(image=, selem=, out=, mode=, cval=, behavior=)

    return result
# Calls Sobel method

# Calls Sobel_v method

# Calls Sobel_h method

# Calls threshold_local method

# Calls threshold_otsu method

# Calls unsharp_mask method
