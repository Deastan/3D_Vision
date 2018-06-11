import cv2
import numpy as np
import matplotlib.pyplot as plt

######################################################################################################
# Initializations:
# Initializing average color histograms for bees and shadows (on white background) in all BGR-colors
blueShadow_static=\
    [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.87814589e-05, 0.00000000e+00, 3.75629179e-05, 0.00000000e+00, 5.63443768e-05, 1.87814589e-05, 1.87814589e-05, 1.87814589e-05, 3.75629179e-05, 1.87814589e-05, 0.00000000e+00, 5.63443768e-05, 3.75629179e-05, 5.63443768e-05, 3.75629179e-05, 5.63443768e-05, 7.51258358e-05, 1.31470213e-04, 5.63443768e-05, 3.75629179e-05, 1.87814589e-05, 1.69033130e-04, 9.39072947e-05, 1.31470213e-04, 1.12688754e-04, 1.69033130e-04, 2.06596048e-04, 7.51258358e-05, 1.31470213e-04, 1.12688754e-04, 9.39072947e-05, 7.51258358e-05, 9.39072947e-05, 1.50251672e-04, 1.12688754e-04, 7.51258358e-05, 1.12688754e-04, 2.06596048e-04, 7.51258358e-05, 5.63443768e-05, 1.31470213e-04, 1.31470213e-04, 2.62940425e-04, 1.12688754e-04, 7.51258358e-05, 1.50251672e-04, 1.31470213e-04, 1.87814589e-04, 9.39072947e-05, 9.39072947e-05, 5.63443768e-05, 9.39072947e-05, 5.63443768e-05, 1.87814589e-05, 9.39072947e-05, 9.39072947e-05, 9.39072947e-05, 5.63443768e-05, 5.63443768e-05, 7.51258358e-05, 5.63443768e-05, 5.63443768e-05, 1.12688754e-04, 1.87814589e-04, 9.39072947e-05, 9.39072947e-05, 3.75629179e-05, 1.31470213e-04, 5.63443768e-05, 3.75629179e-05, 5.63443768e-05, 5.63443768e-05, 1.87814589e-05, 3.75629179e-05, 1.87814589e-05, 5.63443768e-05, 0.00000000e+00, 3.75629179e-05, 2.25377507e-04, 9.39072947e-05, 9.39072947e-05, 1.87814589e-05, 5.63443768e-05, 2.25377507e-04, 1.50251672e-04, 7.51258358e-05, 3.75629179e-05, 3.00503343e-04, 1.69033130e-04, 3.75629179e-05, 1.31470213e-04, 1.50251672e-04, 7.51258358e-05, 3.75629179e-05, 5.63443768e-05, 5.63443768e-05, 5.63443768e-05, 1.12688754e-04, 3.19284802e-04, 2.81721884e-04, 1.69033130e-04, 2.91657287e-04, 3.24274918e-03, 5.07144219e-03, 9.12813841e-03, 1.47930239e-02, 1.49769269e-02, 1.76297147e-02, 1.68944963e-02, 1.87849930e-02, 1.91295077e-02, 2.68923490e-02, 3.19649150e-02, 3.96338875e-02, 3.29647127e-02, 3.03698529e-02, 2.82396564e-02, 2.84971413e-02, 1.99613961e-02, 2.08202862e-02, 1.65958376e-02, 1.41599379e-02, 1.32966849e-02, 1.25697993e-02, 1.18354126e-02, 9.23941902e-03, 8.57758916e-03, 9.44287052e-03, 8.47693444e-03, 1.05152679e-02, 9.78407982e-03, 7.94416346e-03, 9.93113691e-03, 9.39771720e-03, 9.41547734e-03, 9.80971071e-03, 1.04960008e-02, 1.07680015e-02, 1.41137149e-02, 1.38497820e-02, 1.46198347e-02, 1.37980713e-02, 1.42780333e-02, 1.62356271e-02, 1.52869608e-02, 1.57757726e-02, 1.53830379e-02, 1.86419895e-02, 1.69246810e-02, 1.63776996e-02, 1.35864248e-02, 1.33817706e-02, 1.34196223e-02, 1.28120415e-02, 1.38641453e-02, 1.34524439e-02, 9.78722668e-03, 9.44196376e-03, 7.75420475e-03, 7.70666228e-03, 1.00428349e-02, 1.16390991e-02, 1.12365721e-02, 1.02989553e-02, 1.80290752e-02, 1.33958202e-02, 1.72473051e-02, 1.43594053e-02, 7.47998836e-03, 2.04717902e-03, 2.70453009e-03, 1.50251672e-04, 1.50251672e-04, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00]
greenShadow_static=\
    [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.87814589e-05, 3.75629179e-05, 0.00000000e+00, 1.87814589e-05, 1.87814589e-05, 0.00000000e+00, 3.75629179e-05, 1.87814589e-05, 1.87814589e-05, 1.87814589e-05, 0.00000000e+00, 1.87814589e-05, 1.87814589e-05, 0.00000000e+00, 1.12688754e-04, 5.63443768e-05, 3.75629179e-05, 3.75629179e-05, 5.63443768e-05, 3.75629179e-05, 1.12688754e-04, 1.31470213e-04, 7.51258358e-05, 1.87814589e-05, 7.51258358e-05, 1.12688754e-04, 1.31470213e-04, 3.75629179e-05, 1.87814589e-04, 2.62940425e-04, 1.12688754e-04, 7.51258358e-05, 1.69033130e-04, 1.50251672e-04, 9.39072947e-05, 1.31470213e-04, 1.69033130e-04, 9.39072947e-05, 5.63443768e-05, 1.12688754e-04, 3.00503343e-04, 2.06596048e-04, 9.39072947e-05, 1.12688754e-04, 1.69033130e-04, 1.31470213e-04, 1.50251672e-04, 5.63443768e-05, 3.00503343e-04, 1.12688754e-04, 1.31470213e-04, 1.50251672e-04, 3.75629179e-05, 9.39072947e-05, 1.31470213e-04, 1.31470213e-04, 9.39072947e-05, 1.69033130e-04, 9.39072947e-05, 1.50251672e-04, 1.87814589e-05, 9.39072947e-05, 1.12688754e-04, 1.12688754e-04, 1.12688754e-04, 1.87814589e-04, 2.25377507e-04, 1.31470213e-04, 9.39072947e-05, 1.69033130e-04, 9.39072947e-05, 9.39072947e-05, 7.51258358e-05, 3.75629179e-05, 5.63443768e-05, 2.81721884e-04, 1.50251672e-04, 2.62940425e-04, 9.76025554e-04, 3.58538397e-03, 4.91909040e-03, 1.35781052e-02, 2.25598296e-02, 1.72902602e-02, 1.42589969e-02, 1.72830549e-02, 1.79040041e-02, 1.53806898e-02, 1.38828483e-02, 1.84963926e-02, 3.03871209e-02, 3.07273184e-02, 2.86524208e-02, 2.50727921e-02, 2.40571376e-02, 2.38731278e-02, 2.29553225e-02, 1.84525770e-02, 1.63294168e-02, 1.63676749e-02, 1.13297130e-02, 1.26173964e-02, 1.13776801e-02, 1.13164993e-02, 8.16091968e-03, 9.16413644e-03, 8.63271490e-03, 7.81297702e-03, 8.40410614e-03, 7.34314861e-03, 8.26131302e-03, 6.62620814e-03, 8.17251523e-03, 7.50900478e-03, 8.37258154e-03, 8.97955613e-03, 8.71806036e-03, 8.76143718e-03, 1.24586242e-02, 1.13137464e-02, 1.17804497e-02, 1.14110048e-02, 1.14751994e-02, 1.12113719e-02, 1.31775446e-02, 1.31402239e-02, 1.39514413e-02, 1.43809759e-02, 1.72309887e-02, 1.74207044e-02, 1.83700453e-02, 1.89758261e-02, 1.70259593e-02, 1.57907801e-02, 1.36815812e-02, 1.43627441e-02, 1.19508840e-02, 1.14670756e-02, 1.08833785e-02, 7.23381194e-03, 7.93829808e-03, 1.08699335e-02, 1.42529256e-02, 1.65840550e-02, 1.83475899e-02, 1.66061411e-02, 1.70413433e-02, 1.94933672e-02, 1.29641744e-02, 6.01006686e-04, 5.63443768e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00]
redShadow_static=\
    [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.87814589e-05, 3.75629179e-05, 0.00000000e+00, 1.87814589e-05, 1.87814589e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 5.63443768e-05, 3.75629179e-05, 1.87814589e-05, 5.63443768e-05, 1.87814589e-05, 5.63443768e-05, 1.87814589e-05, 1.87814589e-05, 3.75629179e-05, 5.63443768e-05, 7.51258358e-05, 1.87814589e-05, 7.51258358e-05, 1.87814589e-05, 1.87814589e-05, 9.39072947e-05, 1.12688754e-04, 9.39072947e-05, 1.31470213e-04, 1.31470213e-04, 1.87814589e-04, 9.39072947e-05, 1.87814589e-04, 1.69033130e-04, 1.50251672e-04, 3.75629179e-05, 1.31470213e-04, 2.06596048e-04, 1.50251672e-04, 7.51258358e-05, 9.39072947e-05, 2.44158966e-04, 1.50251672e-04, 2.06596048e-04, 1.12688754e-04, 1.31470213e-04, 1.31470213e-04, 1.12688754e-04, 1.31470213e-04, 3.75629179e-05, 1.87814589e-04, 2.25377507e-04, 9.39072947e-05, 7.51258358e-05, 1.87814589e-04, 1.87814589e-05, 7.51258358e-05, 1.69033130e-04, 7.51258358e-05, 2.06596048e-04, 1.87814589e-04, 1.31470213e-04, 9.39072947e-05, 7.51258358e-05, 1.87814589e-04, 5.63443768e-05, 7.51258358e-05, 1.31470213e-04, 9.39072947e-05, 1.31470213e-04, 2.62940425e-04, 1.31470213e-04, 3.75629179e-05, 9.39072947e-05, 9.39072947e-05, 1.50251672e-04, 1.69033130e-04, 5.63443768e-05, 5.63443768e-05, 5.54597713e-04, 2.97383539e-03, 1.18752172e-02, 1.22875364e-02, 1.28744968e-02, 1.46433678e-02, 1.70850949e-02, 1.42024883e-02, 1.88074467e-02, 2.02186654e-02, 2.81591412e-02, 3.88098220e-02, 3.58062673e-02, 3.00451159e-02, 2.33386346e-02, 2.23546691e-02, 1.75281951e-02, 1.65812521e-02, 1.74414140e-02, 1.70351637e-02, 1.95879234e-02, 1.96221250e-02, 1.57459052e-02, 1.07677924e-02, 1.05157278e-02, 9.17153522e-03, 8.10667246e-03, 8.74846737e-03, 8.31789681e-03, 8.98233159e-03, 7.71422323e-03, 7.15810409e-03, 6.80215169e-03, 7.91528239e-03, 8.82863051e-03, 9.85299985e-03, 8.80570176e-03, 8.59502123e-03, 1.32956674e-02, 1.23914016e-02, 1.21770769e-02, 1.18723732e-02, 1.13842918e-02, 1.19603432e-02, 1.33592847e-02, 1.36577074e-02, 1.35404663e-02, 1.58322585e-02, 1.58184389e-02, 1.73138122e-02, 1.89446628e-02, 2.05494715e-02, 1.60029149e-02, 1.52802466e-02, 1.40602912e-02, 1.39085337e-02, 1.23429161e-02, 1.22622704e-02, 1.00004958e-02, 7.19842348e-03, 7.91491816e-03, 9.96088391e-03, 1.44261141e-02, 1.72727145e-02, 1.80418031e-02, 1.54333524e-02, 1.39970852e-02, 1.80438831e-02, 1.56499230e-02, 6.76132522e-04, 5.63443768e-05, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00]
blueBee_static =\
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.3041210224308814e-05, 9.12884715701617e-05, 0.00021934175473537526, 0.0004386835094707505, 0.0006664842468666825, 0.0007164256792780402, 0.0007970317597017678, 0.0010138792847672713, 0.0011978387533345275, 0.0010674266510914395, 0.0014446454539454535, 0.0018683833470371275, 0.002055271186077752, 0.0028151313919290203, 0.0031604610374693885, 0.002876942017142132, 0.004318773732302282, 0.004364913680054491, 0.005437558405472164, 0.006773287811839904, 0.007482756354229253, 0.00803532291514994, 0.008528317117341847, 0.007703976464198489, 0.009643002821477042, 0.011268644376324561, 0.010851424074563007, 0.01088486146179958, 0.010873474579461015, 0.00928806505515571, 0.009243330775017471, 0.007699089416084766, 0.0073205229210071944, 0.00682392580868121, 0.006313914408087995, 0.006422204571386168, 0.005691694360353674, 0.005071228888672362, 0.005369728415587085, 0.005171795451691133, 0.005425089046150903, 0.004612703418089157, 0.004965519470944031, 0.00417291722350121, 0.004878019975956972, 0.004174338106258146, 0.004578763273888874, 0.004240319095565936, 0.004565953408852346, 0.0036874226714701526, 0.0042878951334257565, 0.004399588725259803, 0.0039030415204246945, 0.003950941757776134, 0.004278933530029481, 0.0038782959101772013, 0.0037745620324128246, 0.00371748900443257, 0.004062285988975472, 0.004073419814411769, 0.003964221911460042, 0.0032992492036296134, 0.0030769115089572135, 0.003647887348424549, 0.0038242184581081685, 0.003488147167763363, 0.00413523354425597, 0.003603923976262739, 0.004841429522867073, 0.0038327982374117167, 0.003934815818461946, 0.003909510053010387, 0.003357150536410934, 0.0042271596126212735, 0.004998648234466221, 0.004737035052788195, 0.004736134327002875, 0.0046020082165674605, 0.003830342273942406, 0.004348054441162718, 0.004305385885351833, 0.003939054584335309, 0.0033840434111081265, 0.0032675478832323254, 0.0035085424680721313, 0.00349462451650793, 0.003540423812732429, 0.0037667785476317526, 0.0033138521256306478, 0.0031204291434779887, 0.0028266712697390985, 0.0034521174464377563, 0.003198133574882491, 0.003055278766532456, 0.0032844130661837632, 0.003178006128705998, 0.00308598922468931, 0.003138302919759498, 0.003124154975073986, 0.0027472807546251488, 0.002623317293587682, 0.00314465028709586, 0.0031390248271769244, 0.0035443098479235376, 0.002897860346106377, 0.0028599156600554085, 0.00350713844173703, 0.0029431934618586487, 0.0036453682256283003, 0.003275635902644141, 0.003911086536677196, 0.0036587988095602084, 0.003472422586294444, 0.004559160057199445, 0.004205968367736959, 0.004234989311560695, 0.004735324752212357, 0.00547479975052102, 0.0055750368969664935, 0.0060542824435419786, 0.00692900399166865, 0.0073364112439522, 0.006312776789135181, 0.00569960372078417, 0.005060210732139224, 0.005640407402274849, 0.005997293476446377, 0.006031386950976665, 0.007105951989776076, 0.0074269902388827205, 0.00679689169309021, 0.0069785528511475846, 0.007273319425174323, 0.007282118583965335, 0.007513901616396601, 0.007403446059969302, 0.00667726347653971, 0.007762866224121663, 0.008414769640278085, 0.009616599384988543, 0.009651363623476036, 0.008906692611026938, 0.007480704978130624, 0.008047168808285314, 0.007599730924205059, 0.008851414794541096, 0.008663010640283264, 0.012454827526954105, 0.010977913095474192, 0.012712176504955887, 0.01222987417590661, 0.014086618274538047, 0.01391198875477081, 0.014966608266556514, 0.013075929878336038, 0.012811264360356983, 0.01293328956933716, 0.013514515103134622, 0.013030555523561948, 0.011110330463480422, 0.011137226152035428, 0.009739296431284022, 0.010389625858456175, 0.009665355993194675, 0.008470940980580391, 0.008676876322416364, 0.007032651555721687, 0.006280277278695639, 0.0053879688347590465, 0.0038682797283524435, 0.004059568083127613, 0.0039034051466958447, 0.003138761015597511, 0.002112914156692521, 0.0029812589685628567, 0.0029834303841878695, 0.002919775498645282, 0.0053350892311736335, 0.003200393894633186, 0.00258493353028065, 0.005785327424913836, 0.0023797800754964712, 0.00020515345478417857, 0.00016412276382734287, 4.103069095683572e-05, 4.103069095683572e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
greenBee_static =\
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0682391146434217e-05, 0.0, 0.00015774163752664162, 0.00028704203552679103, 0.0005965605575893892, 0.0008812437740383057, 0.0012391857924933317, 0.0010138792847672713, 0.0008099375593340795, 0.0006308311395145694, 0.0004909837609599828, 0.00036404218203770806, 0.00032963618952053085, 0.0006177899292902606, 0.0006367958925052544, 0.000424530595003503, 0.0007910670067110827, 0.0010188677441070146, 0.0010901113242822549, 0.0013356709100582446, 0.0015902140133517678, 0.0010719007171082315, 0.001327027825179119, 0.0018707609300189203, 0.0020754343682794214, 0.0022343358911961174, 0.002775313745566761, 0.0025854189092874473, 0.002760203470729567, 0.002900018936943532, 0.003565900849477773, 0.0033761855131893685, 0.004042263051484493, 0.0035312420213211466, 0.0041216814156015006, 0.004093861630014563, 0.003906965972157839, 0.004461530887427982, 0.00484316541822553, 0.004848775207688176, 0.005345864439650662, 0.005318138700752297, 0.005957997625909604, 0.00634074431919739, 0.006901755826146546, 0.00682834889185634, 0.006778659610758335, 0.006871486394473794, 0.006118413292145746, 0.007190778076758156, 0.006693478043764062, 0.005801977143297916, 0.006427410941446647, 0.0060284520441021535, 0.005978234513306576, 0.00636199549073545, 0.005583502917218381, 0.005766423821537413, 0.006065328303295898, 0.005369653974248239, 0.004960917201804258, 0.005333148230615341, 0.005506255692857529, 0.005288239169289891, 0.00454021644333835, 0.004453195345116724, 0.004570173180949579, 0.004792959808258068, 0.004630789606324389, 0.004945381534364444, 0.0045816895525982995, 0.004749671843684539, 0.00421141405289946, 0.005692376269482703, 0.006299765425652606, 0.006681325630280413, 0.007100013413010653, 0.006338885150856286, 0.00634005919637014, 0.00607926303906834, 0.005410376931422268, 0.0050414747678605605, 0.004937674193713648, 0.004501965376058745, 0.004263835413030709, 0.004813075764973839, 0.004296006294703771, 0.004767029344804538, 0.004201374672023549, 0.0044163403927728094, 0.003929547828232596, 0.004064083158165328, 0.0035969839040232844, 0.0035644861433212437, 0.003966202515286171, 0.004439476659499004, 0.0035904359340961523, 0.003533523717247499, 0.003577319363023284, 0.003570862326039729, 0.0035504711475620176, 0.003283688891556664, 0.003309097064533565, 0.00339580000391415, 0.00341884754704185, 0.0034240790980040237, 0.0032093218827429233, 0.0032934891267974095, 0.004255655917072432, 0.003721510808664628, 0.00436584077833941, 0.004375675540622316, 0.005634092073554954, 0.00555835924223431, 0.0064839580511033, 0.005630166522196054, 0.005910577020373346, 0.0049138211348392444, 0.0058849125933179295, 0.00546349302976493, 0.005107335176630527, 0.005057466500617673, 0.005018486314431552, 0.00452739209677476, 0.005434561674114469, 0.005025401931939201, 0.007787606319714267, 0.007002018500652217, 0.005561923477488111, 0.0050008364528183955, 0.00470918871550092, 0.004860810604550961, 0.005491231488379578, 0.004458525824221492, 0.004487129108594977, 0.004461347604197774, 0.004944991393866442, 0.004645265865964446, 0.005278205578886603, 0.005288987103088171, 0.004442253074581224, 0.005115412137902439, 0.005241866860993494, 0.005134560207509987, 0.005909498845175596, 0.00553895104541581, 0.006601999780118012, 0.006528640663368157, 0.008001748777285192, 0.007559976124687698, 0.0081603011495822, 0.008859620656181878, 0.009979542459012202, 0.010428964465759078, 0.012331474168924357, 0.01263191762618067, 0.013708549453076696, 0.015422684987798045, 0.01787782504200051, 0.015091603212718891, 0.015694716481689245, 0.01634880634056843, 0.017792731729451977, 0.017671566484467587, 0.017524268327875455, 0.017584712959716083, 0.01765040762587937, 0.014971818034168477, 0.013028697193750617, 0.012074027158703806, 0.009569037235262657, 0.008359106270347498, 0.006381786570399699, 0.005617816689976413, 0.004896910485467803, 0.0035296245310069093, 0.0024196993720023746, 0.002835300804469136, 0.0023887960715818207, 0.007251834549575388, 0.008434511790455344, 0.007019854552053047, 0.002647381166324439, 0.00036927621861152144, 0.00012309207287050715, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
redBee_static =\
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.608242044861763e-05, 0.000131659217078024, 0.0005443957166921539, 0.000735296231901037, 0.0006771666380131167, 0.0006985314203059851, 0.000573948660461585, 0.00047433661682286357, 0.0003344892382682771, 0.0007103255156953582, 0.0004589365875206802, 0.0006201487483681352, 0.000436324690392876, 0.0008892965249228712, 0.000531219095875848, 0.0005513367633337807, 0.0007054724669476119, 0.000693678371558239, 0.000813751679901898, 0.0013109710150365599, 0.0010079417808216233, 0.0008600871784004453, 0.0010131111777713375, 0.001384570249681077, 0.0015445470826720871, 0.0016269638610854926, 0.0018768742080979208, 0.0022091098055745675, 0.00254454772365747, 0.002199126221083278, 0.0027552133313549555, 0.0025657678205159486, 0.0033648265570625072, 0.0032874197207378576, 0.0032003044039913852, 0.0029271489538273353, 0.0037420094441900213, 0.003753571563632199, 0.0038324566527743373, 0.004830537493765761, 0.00367943608860765, 0.004996265439026288, 0.004570151071440309, 0.0061630095758631875, 0.006195424568471206, 0.0056362407955834045, 0.005437352591675826, 0.005591579116156184, 0.005761407680459302, 0.004940185238633142, 0.006144386771554919, 0.005563818920324729, 0.005554344248942134, 0.005451538963239948, 0.005839664607890523, 0.005799290256248921, 0.005853395632010617, 0.005611838689686993, 0.005802749575249853, 0.005636641261341148, 0.005522814308904455, 0.005753696722785955, 0.005092847295463251, 0.005645026996955113, 0.0048297130595606865, 0.004901381340271584, 0.005687390854433448, 0.004478667162338212, 0.0046303779853438835, 0.004214453502087406, 0.004175554126556307, 0.004456675218367235, 0.004877996604274144, 0.005528906396957707, 0.00487835862055479, 0.0050151369992173555, 0.005287292951932278, 0.00458142552775755, 0.004601010588293374, 0.0052128206285829625, 0.005826558571181361, 0.006141479912193677, 0.007414420865461588, 0.005806679075281362, 0.006178885180186011, 0.006711177098381858, 0.005658403586737095, 0.005854041424819796, 0.00501985171927315, 0.004826026012265815, 0.005049480477883206, 0.0051332556247104194, 0.004904909664101279, 0.004822189379107199, 0.004192507318774514, 0.0038333921536286997, 0.0040674991476894245, 0.004289170639015064, 0.003536760822588381, 0.004233437343428726, 0.0038641505861038046, 0.0036106522943329306, 0.004082575238562651, 0.004019918992745943, 0.003968401542147267, 0.003971291708792437, 0.0035315416900354893, 0.003376700636257421, 0.003960054647283665, 0.0037760334382889154, 0.004688008078643458, 0.00436449857702623, 0.004890859527562113, 0.0056573997686218055, 0.00556846722030311, 0.006854012540308627, 0.0068813995889075415, 0.006786430573965922, 0.006194131597306775, 0.005540027243458623, 0.00634474399813395, 0.006124206492799346, 0.005830426130556257, 0.0071238019421961075, 0.008847064677959345, 0.0066119720903728115, 0.005773386095853216, 0.005253489142653864, 0.0053913537533026535, 0.005056669044002817, 0.005066190519335612, 0.004981362059759876, 0.005204732625799569, 0.004670295643060258, 0.004748177842513721, 0.005354151719632658, 0.004847837024858232, 0.005062058567920973, 0.0063140188878751695, 0.006033588294465538, 0.005334345529208767, 0.006066874488563857, 0.0054639249532172545, 0.007351223894264018, 0.007417720161557405, 0.007915315213433496, 0.007932986106459745, 0.007982477671773581, 0.008678331074071864, 0.008808509677409905, 0.009547318326777729, 0.010659462126687794, 0.01130266466710425, 0.013509667965943472, 0.016260943887932176, 0.017263207449170273, 0.018912138951307153, 0.018756610815702464, 0.019078689170020445, 0.01784149803860353, 0.01860742684761082, 0.017003949749244598, 0.01537710727953835, 0.01620069341865004, 0.01578034821223417, 0.014684610957190439, 0.012916045319269794, 0.01105091868898783, 0.010886445831760997, 0.007886317821823492, 0.005893922496315097, 0.005507956516043509, 0.004446663682491691, 0.0036227355949689927, 0.003743711276984593, 0.003885430748504641, 0.005794888525142775, 0.00942646117028768, 0.004763166549427082, 0.0005173916350031211, 0.0, 8.56677803478112e-05, 2.14169450869528e-05, 2.14169450869528e-05, 2.14169450869528e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

######################################################################################################


class Utilities:

    @staticmethod
    def counter(beesCurrentFrame, beesLastFrame, original, lineHistory):

        beesIn = 0
        beesOut=0


        matchingArray = [-1 for x in range(len(beesLastFrame))]


        distSquare=1e10*np.ones((len(beesLastFrame), len(beesCurrentFrame)))
        for beeLast in range(len(beesLastFrame)):
            for beeCurrent in range(len(beesCurrentFrame)):
                #old frame: row-indices, new frame: col-indices
                distSquare[beeLast, beeCurrent] = (beesCurrentFrame[beeCurrent][0]-beesLastFrame[beeLast][0])**2 + (beesCurrentFrame[beeCurrent][1]-beesLastFrame[beeLast][1])**2


        for beeNumber in range(len(beesLastFrame)):
            if distSquare.shape[0]==0 or distSquare.shape[1]==0:
                break
            row, col = np.unravel_index(distSquare.argmin(), distSquare.shape)



            if distSquare[row, col]>25000:
                break






            # cv2.line(original,(int(beesLastFrame[row][0]),int(beesLastFrame[row][1])),(int(beesCurrentFrame[col][0]),int(beesCurrentFrame[col][1])),(0,0,255),2)
            # lineHistory.append(((int(beesLastFrame[row][0]),int(beesLastFrame[row][1])),(int(beesCurrentFrame[col][0]),int(beesCurrentFrame[col][1]))))


            # cv2.putText(original,str(int(distSquare[row, col])),(int(beesCurrentFrame[col][0]),int(beesCurrentFrame[col][1])),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)


            matchingArray[row]=col
            distSquare[row,:]=1e10
            distSquare[:,col]=1e10




            thresholdY=570

            if beesCurrentFrame[col][1]>thresholdY and beesLastFrame[row][1]<thresholdY:
                beesIn+=1
                # cv2.circle(original,(int(beesCurrentFrame[col][0]),int(beesCurrentFrame[col][1])), 30,(0,0,255),-1)
            elif beesCurrentFrame[col][1]<thresholdY and beesLastFrame[row][1]>thresholdY:
                beesOut+=1
                # cv2.circle(original,(int(beesCurrentFrame[col][0]),int(beesCurrentFrame[col][1])), 30,(0,255,0),-1)

            if True:
                thresholdY_2=1000
                if beesCurrentFrame[col][1]<thresholdY_2 and beesLastFrame[row][1]>thresholdY_2:
                    beesIn+=1
                    # cv2.circle(original,(int(beesCurrentFrame[col][0]),int(beesCurrentFrame[col][1])), 30,(0,0,255),-1)
                elif beesCurrentFrame[col][1]>thresholdY_2 and beesLastFrame[row][1]<thresholdY_2:
                    beesOut+=1
                    # cv2.circle(original,(int(beesCurrentFrame[col][0]),int(beesCurrentFrame[col][1])), 30,(0,255,0),-1)






                thresholdX = 80

                if beesCurrentFrame[col][1]<thresholdY_2 and beesCurrentFrame[col][1]>thresholdY and beesLastFrame[row][1]<thresholdY_2 and beesLastFrame[row][1]>thresholdY:

                    if beesCurrentFrame[col][0]>thresholdX and beesLastFrame[row][0]<thresholdX:
                        beesIn+=1
                        # cv2.circle(original,(int(beesCurrentFrame[col][0]),int(beesCurrentFrame[col][1])), 30,(0,0,255),-1)
                    elif beesCurrentFrame[col][0]<thresholdX and beesLastFrame[row][0]>thresholdX:
                        beesOut+=1
                        # cv2.circle(original,(int(beesCurrentFrame[col][0]),int(beesCurrentFrame[col][1])), 30,(0,255,0),-1)
                    thresholdX_2 = 1840
                    if beesCurrentFrame[col][0]<thresholdX_2 and beesLastFrame[row][0]>thresholdX_2:
                        beesIn+=1
                        # cv2.circle(original,(int(beesCurrentFrame[col][0]),int(beesCurrentFrame[col][1])), 30,(0,0,255),-1)
                    elif beesCurrentFrame[col][0]>thresholdX_2 and beesLastFrame[row][0]<thresholdX_2:
                        beesOut+=1
                        # cv2.circle(original,(int(beesCurrentFrame[col][0]),int(beesCurrentFrame[col][1])), 30,(0,255,0),-1)

            lineHistory.append(((int(beesLastFrame[row][0]),int(beesLastFrame[row][1])),(int(beesCurrentFrame[col][0]),int(beesCurrentFrame[col][1]))))


        for i in range(max(len(lineHistory)-100,0), len(lineHistory)):

            cv2.line(original,(lineHistory[i][0][0],lineHistory[i][0][1]),(lineHistory[i][1][0],lineHistory[i][1][1]),(0,255,0),2)
            thresholdY=570

            if lineHistory[i][1][1]>thresholdY and lineHistory[i][0][1]<thresholdY:
                # beesIn+=1
                cv2.circle(original,(int(lineHistory[i][1][0]),int(lineHistory[i][1][1])), 20,(0,0,255),-1)
            elif lineHistory[i][1][1]<thresholdY and lineHistory[i][0][1]>thresholdY:
                # beesOut+=1
                cv2.circle(original,(int(lineHistory[i][1][0]),int(lineHistory[i][1][1])), 20,(0,255,0),-1)

            if True:
                thresholdY_2=1000
                if lineHistory[i][1][1]<thresholdY_2 and lineHistory[i][0][1]>thresholdY_2:
                    # beesIn+=1
                    cv2.circle(original,(int(lineHistory[i][1][0]),int(lineHistory[i][1][1])), 20,(0,0,255),-1)
                elif lineHistory[i][1][1]>thresholdY_2 and lineHistory[i][0][1]<thresholdY_2:
                    # beesOut+=1
                    cv2.circle(original,(int(lineHistory[i][1][0]),int(lineHistory[i][1][1])), 20,(0,255,0),-1)


                thresholdX = 80

                if lineHistory[i][1][1]<thresholdY_2 and lineHistory[i][1][1]>thresholdY and lineHistory[i][0][1]<thresholdY_2 and lineHistory[i][0][1]>thresholdY:

                    if lineHistory[i][1][0]>thresholdX and lineHistory[i][0][0]<thresholdX:
                        # beesIn+=1
                        cv2.circle(original,(int(lineHistory[i][1][0]),int(lineHistory[i][1][1])), 20,(0,0,255),-1)
                    elif lineHistory[i][1][0]<thresholdX and lineHistory[i][0][0]>thresholdX:
                        # beesOut+=1
                        cv2.circle(original,(int(lineHistory[i][1][0]),int(lineHistory[i][1][1])), 20,(0,255,0),-1)
                    thresholdX_2 = 1840
                    if lineHistory[i][1][0]<thresholdX_2 and lineHistory[i][0][0]>thresholdX_2:
                        # beesIn+=1
                        cv2.circle(original,(int(lineHistory[i][1][0]),int(lineHistory[i][1][1])), 20,(0,0,255),-1)
                    elif lineHistory[i][1][0]>thresholdX_2 and lineHistory[i][0][0]<thresholdX_2:
                        # beesOut+=1
                        cv2.circle(original,(int(lineHistory[i][1][0]),int(lineHistory[i][1][1])), 20,(0,255,0),-1)

        return beesIn, beesOut





    @staticmethod
    def histo(pixelArray):
        histogram=[0 for x in range(256)]
        for i in range(pixelArray.shape[0]):
            histogram[int(pixelArray[i])]+=1
        return histogram




    @staticmethod
    def getHistogram(labelNumber, realOriginal):
        pixelArray = []

        #get the pixels from the considered patches
        for j in range(stats[labelNumber,0],stats[labelNumber,0]+stats[labelNumber,2]):
            for i in range(stats[labelNumber,1], stats[labelNumber,1]+stats[labelNumber,3]):
                if labels[i,j]==labelNumber:
                    pixelArray.append(realOriginal[i,j])
                    notEmpty = True
        pixelArray=np.matrix(pixelArray)


        pixelBlue = pixelArray[:, 0]
        pixelGreen = pixelArray[:, 1]
        pixelRed = pixelArray[:, 2]

        histoBlue=Utilities.histo(pixelBlue)
        histoGreen=Utilities.histo(pixelGreen)
        hirstoRed=Utilities.histo(pixelRed)

            # blueArray += plt.hist(shadowBlue,range=(0,256), density=True, bins=255, stacked=True)[0] #density and stacked together make it a normalized histogram (to 1)
            # greenArray+= plt.hist(shadowGreen,range=(0,256), density=True, bins=255, stacked=True)[0]
            # redArray +=  plt.hist(shadowRed,range=(0,256), density=True, bins=255, stacked=True)[0]
            # plt.savefig('/home/philipp/Desktop/Histograms_shadows/shadwo_frame_'+str(frame)+'_label'+str(label)+'_blue')
            # plt.show()
        return (histoBlue, histoGreen, hirstoRed)




    @staticmethod
    def checkColors(labelNumber, realOriginal):

        localBlue, localGreen, localRed = Utilities.getHistogram(labelNumber, realOriginal)

        sumBee = np.dot(blueBee_static[0:140], localBlue[0:140])+np.dot(greenBee_static[0:140], localGreen[0:140])+np.dot(redBee_static[0:140], localRed[0:140])
        sumShadow = np.dot(blueShadow_static[0:140], localBlue[0:140]) +np.dot(greenShadow_static[0:140], localGreen[0:140])+np.dot(redShadow_static[0:140], localRed[0:140])

        if sumBee>sumShadow:
            return True
        else:
            return False




    @staticmethod
    def connectedComponents(fgmask, original, realOriginal):

        global labels
        global stats


        output = cv2.connectedComponentsWithStats(fgmask, 4, cv2.CV_32S)

        num_labels = output[0]
        labels = output[1]
        stats = output[2]
        centroids = output[3]

        beesCurrentFrame=[]
        for i in range(1, num_labels):  # don't do 0, cause it's just the background
            if stats[i, 4] > 1500:  # threshold to filter out small patches
                tmp=np.array(realOriginal)
                if True: # Utilities.checkColors(i, realOriginal)==True:
                    cv2.ellipse(original, (int(centroids[i, 0]), int(centroids[i, 1])), (stats[i, 2] // 3, stats[i, 3] // 3), 0, 0, 360, (0,255,0), 4)

                    beesCurrentFrame.append(centroids[i])
                else:
                    if showShadows==True:
                        cv2.ellipse(original, (int(centroids[i, 0]), int(centroids[i, 1])), (stats[i, 2] // 4, stats[i, 3] // 4), 0, 0, 360, (0,0,255), 1)

        return labels, beesCurrentFrame
