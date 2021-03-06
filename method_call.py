from skimage import filters, morphology, segmentation, exposure
from skimage.morphology import disk
from qgis.PyQt.QtWidgets import QMessageBox
import re
# TODO change the names of my... methods


# Returns a list of parameter names
def get_list_of_names(parameter_string):
    tempList = re.findall("\w+=\S+", parameter_string)
    word = ""
    list_of_names = []
    for x in range(len(tempList)):
        for i in range(len(tempList[x])):
            if (tempList[x][i] == "=" or tempList[x][i] == " "):
                list_of_names.append(word)
            else:
                word += tempList[x][i]
    return list_of_names


# Returns a list of parameter values
def get_list_of_values(parameter_string):
    for x in range(len(parameter_string)):
        parameter_string = parameter_string.replace(" ", "")
    resultList = []
    tempString = ""
    startOfParameter = False
    for x in range(len(parameter_string)):
        if (parameter_string[x] == ','):
            startOfParameter = False
            if(len(tempString) != 0):
                resultList.append(tempString)
            tempString = ""
        if (startOfParameter):
            tempString += parameter_string[x]
            if (x == len(parameter_string) - 1):
                resultList.append(tempString)
        if (parameter_string[x] == '='):
            startOfParameter = True

    return resultList

# The method skips the first element since its not an actual value. The image is read from a path
# which is then passed as a value
def set_parameter_values(included_parameters, parameter_names, parameter_values):
    if(len(parameter_values) == 0):
        return included_parameters

    for i in range(0, len(parameter_names)):
        for j in range(0, len(included_parameters)):
            try:
                if (parameter_names[i] == included_parameters[j][0]):
                    included_parameters[j][1] = parameter_values[i]
                    break
            except IndexError:
                included_parameters[j].append(parameter_values[i])

    return included_parameters


## Calls Segmentation functions
# Calls chan_vese method
def my_chan_vese(image_value, parameter_list):

    parameter_names_string = " "
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]
    try:
        if (parameter_names_string.find("mu") != -1):
            parameter_list[1][1] = float(parameter_list[1][1])
    except:
        return 'mu parameter was incorrect'
    try:
        if (parameter_names_string.find("lambda1") != -1):
            parameter_list[2][1] = float(parameter_list[2][1])
    except:
        return 'lambda1 parameter was incorrect'
    try:
        if (parameter_names_string.find("lambda2") != -1):
            parameter_list[3][1] = float(parameter_list[3][1])
    except:
        return 'lambda2 parameter was incorrect'
    try:
        if (parameter_names_string.find("tol") != -1):
            parameter_list[4][1] = float(parameter_list[4][1])
    except:
        return 'tol parameter was incorrect'
    try:
        if (parameter_names_string.find("max_iter") != -1):
            parameter_list[5][1] = int(parameter_list[5][1])
    except:
        return 'max_iter parameter was incorrect'
    try:
        if (parameter_names_string.find("dt") != -1):
            parameter_list[6][1] = float(parameter_list[6][1])
    except:
        return 'dt parameter was incorrect'
    try:
        if (parameter_names_string.find("extended_output") != -1):
            parameter_list[8][1] = bool(parameter_list[8][1])
    except:
        return 'extended_output parameter was incorrect'

    result = segmentation.chan_vese(image=image_value, mu=parameter_list[1][1], lambda1=parameter_list[2][1],
                                    lambda2=parameter_list[3][1], tol=parameter_list[4][1], max_iter=parameter_list[5][1],
                                    dt=parameter_list[6][1], init_level_set=parameter_list[7][1], extended_output=parameter_list[8][1])

    if (parameter_list[8][1] == True):
        return result[1] * 100
    else:
        return result * 100

# Calls Felzenszwalb method
def my_felzenszwalb(image_value, parameter_list):
    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    try:
        if (parameter_names_string.find("scale") != -1):
            parameter_list[1][1] = int(parameter_list[1][1])
    except:
        return 'scale parameter was incorrect'
    try:
        if (parameter_names_string.find("sigma") != -1):
            parameter_list[2][1] = float(parameter_list[2][1])
    except:
        return 'sigma parameter was incorrect'
    try:
        if (parameter_names_string.find("min_size") != -1):
            parameter_list[3][1] = int(parameter_list[3][1])
    except:
        return 'min_size parameter was incorrect'
    try:
        if (parameter_names_string.find("multichannel") != -1):
            parameter_list[4][1] = bool(parameter_list[4][1])
    except:
        return 'multichannel parameter was incorrect'
    result = segmentation.felzenszwalb(image=image_value, scale=parameter_list[1][1], sigma=parameter_list[2][1],
                                       min_size=parameter_list[3][1], multichannel=parameter_list[4][1])

    return result

# Calls inverse_gaussian_gradient
def my_inverse_gaussian_gradient(image_value, parameter_list):
    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    try:
        if (parameter_names_string.find("alpha") != -1):
            parameter_list[1][1] = float(parameter_list[1][1])
    except:
        return 'alpha parameter was incorrect'
    try:
        if (parameter_names_string.find("sigma") != -1):
            parameter_list[2][1] = float(parameter_list[2][1])
    except:
        return 'sigma parameter was incorrect'

    result = segmentation.inverse_gaussian_gradient(image=image_value, alpha=parameter_list[1][1], sigma=parameter_list[2][1])

    return result * 100

# Calls quickshift method
def my_quickshift(image_value, parameter_list):

    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    try:
        if (parameter_names_string.find("ratio") != -1):
            parameter_list[1][1] = float(parameter_list[1][1])
    except:
        return 'ratio parameter was incorrect'
    try:
        if (parameter_names_string.find("kernel_size") != -1):
            parameter_list[2][1] = int(parameter_list[2][1])
    except:
        return 'kernel_size parameter was incorrect'
    try:
        if (parameter_names_string.find("max_dist") != -1):
            parameter_list[3][1] = int(parameter_list[3][1])
    except:
        return 'max_dist parameter was incorrect'
    try:
        if (parameter_names_string.find("return_tree") != -1):
            parameter_list[4][1] = bool(parameter_list[4][1])
    except:
        return 'return_tree parameter was incorrect'
    try:
        if (parameter_names_string.find("sigma") != -1):
            parameter_list[5][1] = int(parameter_list[5][1])
    except:
        return 'sigma parameter was incorrect'
    try:
        if (parameter_names_string.find("convert2lab") != -1):
            parameter_list[6][1] = bool(parameter_list[6][1])
    except:
        return 'convert2lab parameter was incorrect'
    try:
        if (parameter_names_string.find("random_seed") != -1):
            parameter_list[7][1] = int(parameter_list[7][1])
    except:
        return 'random_seed parameter was incorrect'
    result = segmentation.quickshift(image=image_value, ratio=parameter_list[1][1], kernel_size=parameter_list[2][1],
                                 max_dist=parameter_list[3][1], return_tree=parameter_list[4][1], sigma=parameter_list[5][1],
                                 convert2lab=parameter_list[6][1], random_seed=parameter_list[7][1])

    return result


# Calls slic method
def my_slic(image_value, parameter_list):
    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    try:
        if (parameter_names_string.find("n_segments") != -1):
            parameter_list[1][1] = int(parameter_list[1][1])
    except:
        return 'n_segments parameter was incorrect'
    try:
        if (parameter_names_string.find("compactness") != -1):
            parameter_list[2][1] = float(parameter_list[2][1])
    except:
        return 'compactness parameter was incorrect'
    try:
        if (parameter_names_string.find("max_iter") != -1):
            parameter_list[3][1] = int(parameter_list[3][1])
    except:
        return 'max_iter parameter was incorrect'
    try:
        if (parameter_names_string.find("sigma") != -1):
            parameter_list[4][1] = int(parameter_list[4][1])
    except:
        return 'sigma parameter was incorrect'
    try:
        if (parameter_names_string.find("min_size_factor") != -1):
            parameter_list[9][1] = float(parameter_list[9][1])
    except:
        return 'min_size_factor parameter was incorrect'
    try:
        if (parameter_names_string.find("max_size_factor") != -1):
            parameter_list[10][1] = int(parameter_list[10][1])
    except:
        return 'max_size_factor parameter was incorrect'

    result = segmentation.slic(image=image_value, n_segments=parameter_list[1][1],
                               compactness=parameter_list[2][1], max_iter=parameter_list[3][1],
                               sigma=parameter_list[4][1], spacing=parameter_list[5][1],
                               multichannel=parameter_list[6][1], convert2lab=parameter_list[7][1],
                               enforce_connectivity=parameter_list[8][1], min_size_factor=parameter_list[9][1],
                               max_size_factor=parameter_list[10][1], slic_zero=parameter_list[11][1])

    return result


## Calls Filters functions
# Calls gaussian method
def my_gaussian(image_value, parameter_list):
    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    try:
        if (parameter_names_string.find("sigma") != -1):
            parameter_list[1][1] = int(parameter_list[1][1])
    except:
        return 'Sigma parameter was incorrect'
    try:
        if (parameter_names_string.find("cval") != -1):
            parameter_list[4][1] = int(parameter_list[4][1])
    except:
        return 'cval parameter was incorrect'
    try:
        if (parameter_names_string.find("truncate") != -1):
            parameter_list[7][1] = float(parameter_list[7][1])
    except:
        return 'truncate parameter was incorrect'
    try:
        if (parameter_names_string.find("multichannel") != -1):
            parameter_list[5][1] = bool(parameter_list[5][1])
    except:
        return 'multichannel parameter was incorrect'


    result = filters.gaussian(image=image_value, sigma=parameter_list[1][1], output=parameter_list[2][1],
                              mode=parameter_list[3][1], cval=parameter_list[4][1], multichannel=parameter_list[5][1],
                              preserve_range=parameter_list[6][1], truncate=parameter_list[7][1])

    return result * 100


# Calls laplace method
def my_laplace(image_value, parameter_list):

    try:
        param_ksize = int(parameter_list[1][1])
    except:
        return 'ksize parameter was incorrect'

    result = filters.laplace(image=image_value, ksize=param_ksize, mask=parameter_list[2][1])

    return result * 100


# Calls Median method
# def my_median(image_value, parameter_list):
#     parameter_names_string = ""
#     for x in range(len(parameter_list)):
#         parameter_names_string += parameter_list[x][0]
#     try:
#         if (parameter_names_string.find("selem") != -1):
#             parameter_list[1][1] = int(parameter_list[1][1])
#         if (parameter_names_string.find("cval") != -1):
#             parameter_list[4][1] = int(parameter_list[4][1])
#
#         result = filters.median(image=image_value, selem=disk(parameter_list[1][1]), out=parameter_list[2][2], mode=parameter_list[3][1],
#                                 cval=parameter_list[4][1], behavior=parameter_list[5][1])
#     except:
#         QMessageBox.critical(None, "test", "The data type for parameters was incorrect!")
#
#     return result

# Calss prewitt method
def my_prewitt(image_value, parameter_list):
    try:
        result = filters.prewitt(image=image_value, mask=parameter_list[1][1])
    except:
        return 'Parameters were incorrect'

    return result * 100

def my_prewitt_h(image_value, parameter_list):
    try:
        result = filters.prewitt_h(image=image_value, mask=parameter_list[1][1])
    except:
        return 'Parameters were incorrect'

    return result * 100
def my_prewitt_v(image_value, parameter_list):
    try:
        result = filters.prewitt_v(image=image_value, mask=parameter_list[1][1])
    except:
        return 'Parameters were incorrect'

    return result * 100

# Calls Sobel method
def my_sobel(image_value, parameter_list):
    try:
        result = filters.sobel(image=image_value, mask=parameter_list[1][1])
    except:
        return 'Parameters were incorrect'

    return result * 100


# Calls Sobel_h method
def my_sobel_h(image_value, parameter_list):
    try:
        result = filters.sobel_h(image=image_value, mask=parameter_list[1][1])
    except:
        return 'Parameters were incorrect'

    return result * 100


# Calls Sobel_v method
def my_sobel_v(image_value, parameter_list):

    try:
        result = filters.sobel_v(image=image_value, mask=parameter_list[1][1])
    except:
        return 'Parameters were incorrect'

    return result * 100


# Calls threshold_local method
def my_threshold_local(image_value, parameter_list):
    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    try:
        if(parameter_names_string.find("block_size") != -1):
            parameter_list[1][1] = int(parameter_list[1][1])
    except:
        return 'block_size parameter was incorrect'
    try:
        if(parameter_names_string.find("offset") != -1):
            parameter_list[3][1] = float(parameter_list[3][1])
    except:
        return 'offset parameter was incorrect'
    try:
        if(parameter_names_string.find("param") != -1):
            parameter_list[5][1] = int(parameter_list[5][1])
    except TypeError:
        pass
    try:
        if(parameter_names_string.find("cval") != -1):
            parameter_list[6][1] = float(parameter_list[6][1])
    except:
        return 'cval parameter was incorrect'

    result = image_value > filters.threshold_local(image=image_value, block_size=parameter_list[1][1], method=parameter_list[2][1],
                                         offset=parameter_list[3][1], mode=parameter_list[4][1], param=parameter_list[5][1],
                                         cval=parameter_list[6][1])

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
        if (parameter_names_string.find("radius") != -1):
            parameter_list[1][1] = float(parameter_list[1][1])
    except:
        return 'radius parameter was incorrect'
    try:
        if (parameter_names_string.find("amount") != -1):
            parameter_list[2][1] = float(parameter_list[2][1])
    except:
        return 'amount parameter was incorrect'

    result = filters.unsharp_mask(image=image_value, radius=parameter_list[1][1], amount=parameter_list[2][1],
                                multichannel=parameter_list[3][1], preserve_range=parameter_list[4][1])

    return result * 100

## Calls exposure methods
# Calls adjust_gamma method
def my_adjust_gamma(image_value, parameter_list):
    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    try:
        if (parameter_names_string.find("gamma") != -1):
            parameter_list[1][1] = float(parameter_list[1][1])
    except:
        return 'gamma parameter was incorrect'
    try:
        if (parameter_names_string.find("gain") != -1):
            parameter_list[2][1] = float(parameter_list[2][1])
    except:
        return 'gain parameter was incorrect'
    result = exposure.adjust_gamma(image=image_value, gamma=parameter_list[1][1], gain=parameter_list[2][1])

    return result

# Calls adjust_log method
def my_adjust_log(image_value, parameter_list):
    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]
    try:
        if (parameter_names_string.find("gain") != -1):
            parameter_list[1][1] = float(parameter_list[1][1])
    except:
        return 'gain parameter was incorrect'
    try:
        if (parameter_names_string.find("inv") != -1):
            parameter_list[2][1] = bool(parameter_list[2][1])
    except:
        return 'inv parameter was incorrect'

    result = exposure.adjust_log(image=image_value, gain=parameter_list[1][1], inv=parameter_list[2][1])

    return result
# Calls adjust_sigmoid method
def my_adjust_sigmoid(image_value, parameter_list):
    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]

    try:
        if (parameter_names_string.find("cutoff") != -1):
            parameter_list[1][1] = float(parameter_list[1][1])
    except:
        return 'cutoff parameter was incorrect'
    try:
        if (parameter_names_string.find("gain") != -1):
            parameter_list[2][1] = float(parameter_list[2][1])
    except:
        return 'gain parameter was incorrect'
    try:
        if (parameter_names_string.find("inv") != -1):
            parameter_list[3][1] = bool(parameter_list[3][1])
    except:
        return 'inv parameter was incorrect'

    result = exposure.adjust_sigmoid(image=image_value, cutoff=parameter_list[1][1],
                                     gain=parameter_list[2][1], inv=parameter_list[3][1])

    return result
# Calls equalize_hist method
def my_equalize_hist(image_value, parameter_list):
    parameter_names_string = ""
    for x in range(len(parameter_list)):
        parameter_names_string += parameter_list[x][0]
    try:
        if (parameter_names_string.find("nbins") != -1):
            parameter_list[1][1] = int(parameter_list[1][1])
    except:
        return 'nbins parameter was incorrect'

    result = exposure.equalize_hist(image=image_value, nbins=parameter_list[1][1])
    return result * 100