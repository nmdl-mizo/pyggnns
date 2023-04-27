import torch

# 1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p, 5s, 4d, 5p, 6s, 4f, 5d, 6p
N_ORB = 15

# ref:
# [1] E. Clementi, and D. L. Raimondi, J. Chem. Phys. 38, 2686–2689 (1963).
# [2] E. Clementi, et al., J. Chem. Phys. 47, 1300–1307 (1967).
# fmt: off
EXPONENT_TABLE = torch.tensor(
    [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # dummy
        [1.6875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # using the same value as He # noqa: E501
        [1.6875, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [2.6906, 0.6396, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [3.6848, 0.956, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [4.6795, 1.2881, 1.2107, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [5.6727, 1.6083, 1.5679, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [6.6651, 1.9237, 1.917, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [7.6579, 2.2458, 2.2266, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [8.6501, 2.5638, 2.55, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [9.6421, 2.8792, 2.8792, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [10.6259, 3.2857, 3.4009, 0.8358, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [11.6089, 3.696, 3.9129, 1.1025, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [12.591, 4.1068, 4.4817, 1.3724, 1.3552, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [13.5745, 4.51, 4.9725, 1.6344, 1.4284, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [14.5578, 4.9125, 5.4806, 1.8806, 1.6288, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [15.5409, 5.3144, 5.9885, 2.1223, 1.8273, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [16.5239, 5.7152, 6.4966, 2.3561, 2.0387, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [17.5075, 6.1152, 7.0041, 2.5856, 2.2547, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [18.4895, 6.5031, 7.5136, 2.8933, 2.5752, 0.8738, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [19.473, 6.8882, 8.0207, 3.2005, 2.8861, 1.0995, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [20.4566, 7.2868, 8.5273, 3.4466, 3.1354, 1.1581, 2.3733, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [21.4409, 7.6883, 9.0324, 3.6777, 3.3679, 1.2042, 2.7138, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [22.4256, 8.0907, 9.5364, 3.9031, 3.595, 1.2453, 2.9943, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [23.4138, 8.4919, 10.0376, 4.1226, 3.822, 1.2833, 3.2522, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [24.3957, 8.8969, 10.542, 4.3393, 4.0364, 1.3208, 3.5094, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [25.381, 9.2995, 11.0444, 4.5587, 4.2593, 1.3585, 3.7266, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [26.3668, 9.7025, 11.5462, 4.7741, 4.4782, 1.3941, 3.9518, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [27.3526, 10.1063, 12.0476, 4.987, 4.695, 1.4277, 4.1765, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [28.3386, 10.5099, 12.5485, 5.1981, 4.9102, 1.4606, 4.4002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [29.3245, 10.914, 13.049, 5.4064, 5.1231, 1.4913, 4.6261, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [30.3094, 11.2995, 13.5454, 5.6654, 5.4012, 1.7667, 5.0311, 1.5554, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [31.2937, 11.6824, 14.0411, 5.9299, 5.6712, 2.0109, 5.4171, 1.6951, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [32.2783, 12.0635, 14.5368, 6.1985, 5.9499, 2.236, 5.7928, 1.8623, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [33.2622, 12.4442, 15.0326, 6.4678, 6.235, 2.4394, 6.159, 2.0718, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [34.2471, 12.8217, 15.5282, 6.7395, 6.5236, 2.6382, 6.5197, 2.257, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [35.2316, 13.199, 16.0235, 7.0109, 6.8114, 2.8289, 6.8753, 2.4e423, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [36.2078, 13.5784, 16.5194, 7.2809, 7.1011, 3.097, 7.2264, 2.7202, 0.9969, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [37.1911, 13.9509, 17.0152, 7.5546, 7.3892, 3.3611, 7.5754, 2.983, 1.2141, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [38.1756, 14.3111, 17.5016, 7.8505, 7.6975, 3.5659, 8.4657, 3.1864, 1.2512, 3.9896, 0.0, 0.0, 0.0, 0.0, 0.0],
        [39.159, 14.6869, 17.9964, 8.1205, 7.9485, 3.7254, 8.5223, 3.365, 1.2891, 3.2679, 0.0, 0.0, 0.0, 0.0, 0.0],
        [40.1423, 15.0626, 18.4911, 8.3905, 8.2184, 3.909, 8.7847, 3.5652, 1.3392, 3.0796, 0.0, 0.0, 0.0, 0.0, 0.0],
        [41.1256, 15.4384, 18.9859, 8.6605, 8.503, 4.1037, 9.1097, 3.7622, 1.3952, 3.111, 0.0, 0.0, 0.0, 0.0, 0.0],
        [42.109, 15.8141, 19.4704, 8.9304, 8.7947, 4.2996, 9.451, 3.9528, 1.4453, 3.2205, 0.0, 0.0, 0.0, 0.0, 0.0],
        [43.0923, 16.1899, 19.9754, 9.2004, 9.0844, 4.4876, 9.7981, 4.1291, 1.4905, 3.347, 0.0, 0.0, 0.0, 0.0, 0.0],
        [44.0756, 16.5656, 20.4702, 9.4704, 9.3724, 4.6571, 10.1478, 4.3236, 1.5286, 3.4937, 0.0, 0.0, 0.0, 0.0, 0.0],
        [45.0589, 16.9414, 20.965, 9.7404, 9.6616, 4.8568, 10.4989, 4.501, 1.5675, 3.6476, 0.0, 0.0, 0.0, 0.0, 0.0],
        [46.0423, 17.3171, 21.4597, 10.0104, 9.9476, 5.0398, 10.8503, 4.6777, 1.6057, 3.8064, 0.0, 0.0, 0.0, 0.0, 0.0],
        [47.0256, 17.6929, 21.9545, 10.2804, 10.2305, 5.2173, 11.2023, 4.8528, 1.6384, 3.9692, 0.0, 0.0, 0.0, 0.0, 0.0],
        [48.0097, 18.0618, 22.449, 10.5436, 10.5069, 5.4403, 11.5594, 5.0922, 1.9023, 4.2354, 1.694, 0.0, 0.0, 0.0, 0.0],  # noqa: E501
        [48.992, 18.4297, 22.9427, 10.8066, 10.7844, 5.6645, 11.9139, 5.3163, 2.1257, 4.4925, 1.8204, 0.0, 0.0, 0.0, 0.0],  # noqa: E501
        [49.9744, 18.7977, 23.4363, 11.0697, 11.0613, 5.8859, 12.2666, 5.5453, 2.3222, 4.7436, 1.9989, 0.0, 0.0, 0.0, 0.0],  # noqa: E501
        [50.9568, 19.1656, 23.93, 11.3327, 11.3363, 6.1021, 12.6131, 5.7805, 2.5076, 4.99, 2.1617, 0.0, 0.0, 0.0, 0.0],
        [51.9391, 19.5335, 24.4237, 11.5958, 11.6138, 6.3243, 12.9669, 6.0074, 2.6807, 5.2335, 2.3223, 0.0, 0.0, 0.0, 0.0],  # noqa: E501
        [52.9215, 19.9015, 24.9173, 11.8588, 11.8892, 6.5432, 13.3156, 6.2393, 2.8436, 5.4733, 2.4849, 0.0, 0.0, 0.0, 0.0],  # noqa: E501
        [53.9043, 20.2558, 25.4098, 12.1258, 12.1926, 6.7606, 13.6602, 6.4644, 3.0889, 5.7096, 2.7302, 1.0605, 0.0, 0.0, 0.0],  # noqa: E501
        [54.8861, 20.6234, 25.9048, 12.3852, 12.4388, 6.98, 14.0081, 6.7008, 3.3239, 5.946, 2.9601, 1.2625, 0.0, 0.0, 0.0],  # noqa: E501
        [55.8683, 20.9767, 26.3978, 12.6477, 12.7132, 7.1991, 14.3534, 6.9266, 3.5622, 6.1813, 3.1792, 1.552, 0.34, 0.0, 0.0],  # noqa: E501
        [56.8481, 21.37, 26.8912, 12.8864, 12.9865, 7.42, 14.6951, 7.1516, 3.7827, 6.4152, 3.3931, 1.7994, 0.419, 0.0, 0.0],  # noqa: E501
        [57.8306, 21.731, 27.3847, 13.167, 13.2748, 7.5833, 15.0508, 7.2642, 3.5226, 6.5743, 3.0567, 1.2911, 5.2752, 0.0, 0.0],  # noqa: E501
        [58.8132, 22.1081, 27.8783, 13.4476, 13.563, 7.7466, 15.3856, 7.5035, 3.7485, 6.7023, 3.3922, 1.5511, 5.5665, 0.0, 0.0],  # noqa: E501
        [59.7958, 22.4852, 28.3719, 13.7282, 13.8513, 7.9099, 15.6994, 7.6558, 3.7671, 6.935, 3.2828, 1.5659, 5.7835, 0.0, 0.0],  # noqa: E501
        [60.7783, 22.8674, 28.8655, 14.0088, 14.1395, 8.0731, 16.0763, 7.772, 3.6498, 7.0599, 3.2562, 1.3353, 5.8829, 0.0, 0.0],  # noqa: E501
        [61.7609, 23.2354, 29.359, 14.2894, 14.428, 8.217, 16.4176, 7.9687, 3.718, 7.2352, 3.311, 1.3536, 6.08, 0.0, 0.0],  # noqa: E501
        [62.7435, 23.6085, 29.8527, 14.5699, 14.7164, 8.361, 16.759, 8.1617, 3.7764, 7.4084, 3.3528, 1.3691, 6.2534, 0.0, 0.0],  # noqa: E501
        [63.7261, 23.9861, 30.3462, 14.8505, 15.0049, 8.505, 17.0995, 8.3497, 3.8341, 7.5775, 3.3922, 1.3834, 6.4662, 0.0, 0.0],  # noqa: E501
        [64.7086, 24.3547, 30.8398, 15.1311, 15.2935, 8.648, 17.4433, 8.4565, 3.8608, 7.7545, 3.4254, 1.3906, 6.634, 0.0, 0.0],  # noqa: E501
        [65.6912, 24.7278, 31.3334, 15.4117, 15.5818, 8.828, 17.7823, 8.6407, 3.9152, 7.9179, 3.4678, 1.4065, 6.8674, 0.0, 0.0],  # noqa: E501
        [66.6737, 25.1008, 31.827, 15.6923, 15.8703, 9.058, 18.1201, 8.7773, 3.9436, 8.0678, 3.4944, 1.4127, 6.9946, 0.0, 0.0],  # noqa: E501
        [67.6563, 25.4739, 32.3206, 15.9728, 16.1587, 9.2844, 18.4581, 8.997, 4.0074, 8.236, 3.5456, 1.4307, 7.1585, 0.0, 0.0],  # noqa: E501
        [68.6389, 25.847, 32.8142, 16.2534, 16.4455, 9.3794, 18.7989, 9.1005, 4.03, 8.3974, 3.5663, 1.4322, 7.358, 0.0, 0.0],  # noqa: E501
        [69.6195, 26.2249, 33.3055, 16.5115, 16.7221, 9.5673, 19.1396, 9.2976, 4.191, 8.8223, 3.736, 1.4674, 7.7328, 4.0266, 0.0],  # noqa: E501
        [70.6016, 26.5949, 33.7994, 16.7705, 16.9944, 9.7443, 19.4766, 9.4824, 4.3666, 8.881, 3.917, 1.5274, 8.0524, 3.3239, 0.0],  # noqa: E501
        [71.5837, 26.9649, 34.2932, 17.0305, 17.2668, 9.9397, 19.8137, 9.6837, 4.5387, 9.081, 4.0947, 1.5875, 8.3676, 3.2736, 0.0],  # noqa: E501
        [72.5657, 27.3349, 34.7871, 17.29, 17.5392, 10.1397, 20.1508, 9.8871, 4.7083, 9.2933, 4.2651, 1.6424, 8.6777, 3.3484, 0.0],  # noqa: E501
        [73.5478, 27.7049, 35.281, 17.5495, 17.8115, 10.3391, 20.4849, 10.0933, 4.8714, 9.5136, 4.4288, 1.686, 8.9812, 3.4766, 0.0],  # noqa: E501
        [74.5299, 28.0749, 35.7749, 17.8091, 18.0839, 10.5238, 20.8249, 10.286, 5.019, 9.7145, 4.582, 1.7205, 9.2882, 3.5994, 0.0],  # noqa: E501
        [75.5119, 28.4449, 36.2688, 18.0686, 18.3563, 10.712, 21.162, 10.4785, 5.1691, 9.9343, 4.7322, 1.7611, 9.5862, 3.7392, 0.0],  # noqa: E501
        [76.494, 28.8149, 36.7627, 18.3281, 18.6287, 10.9097, 21.4991, 10.6826, 5.3176, 10.1575, 4.8839, 1.7919, 9.8765, 3.8815, 0.0],  # noqa: E501
        [77.4761, 29.1849, 37.2566, 18.5876, 18.901, 11.1033, 21.8361, 10.8867, 5.4655, 10.382, 5.034, 1.823, 10.1624, 4.0253, 0.0],  # noqa: E501
        [78.4581, 29.5547, 37.7505, 18.8471, 19.1734, 11.3112, 22.1732, 11.1015, 5.6222, 10.617, 5.1934, 1.8589, 10.4402, 4.1712, 0.0],  # noqa: E501
        [79.4409, 29.8421, 38.2431, 19.1397, 19.4555, 11.5197, 22.5114, 11.3042, 5.8244, 10.8472, 5.4177, 2.1366, 10.7169, 4.405, 2.0423],  # noqa: E501
        [80.4195, 30.215, 38.7383, 19.3841, 19.7165, 11.7232, 22.8489, 11.5084, 6.0263, 11.0799, 5.606, 2.35, 10.9922, 4.6304, 2.0655],  # noqa: E501
        [81.3982, 30.588, 39.2335, 19.6285, 19.9774, 11.9268, 23.1805, 11.7126, 6.2058, 11.3098, 5.8042, 2.54, 11.2673, 4.8488, 2.2233],  # noqa: E501
        [82.3768, 30.9609, 39.7286, 19.8729, 20.2383, 12.1304, 23.524, 11.9168, 6.4046, 11.9168, 6.0049, 2.7218, 11.5396, 5.0608, 2.3701],  # noqa: E501
        [83.3554, 31.3338, 40.2238, 20.1173, 20.4992, 12.3339, 23.8615, 12.121, 6.5867, 11.7624, 6.208, 2.8833, 11.8101, 5.2678, 2.5272],  # noqa: E501
        [84.3341, 31.7068, 40.719, 20.3617, 20.7602, 12.5375, 24.1991, 12.3253, 6.7786, 11.9857, 6.3942, 3.054, 12.0828, 5.4706, 2.6793],  # Rn (86) # noqa: E501
    ]
)
# fmt: on
