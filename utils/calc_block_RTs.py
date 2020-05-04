""""
Extracting RTs for each blocks and each groups of locations
"""

import numpy as np
import mne

def calc_block_RTs(data_e, data_l):
    B3  = np.mean(data_e.metadata[data_e.metadata.Block==3].RT)
    B4  = np.mean(data_e.metadata[data_e.metadata.Block==4].RT)
    B5  = np.mean(data_e.metadata[data_e.metadata.Block==5].RT)
    B6  = np.mean(data_e.metadata[data_e.metadata.Block==6].RT)
    B7  = np.mean(data_l.metadata[data_l.metadata.Block==7].RT)
    B8  = np.mean(data_l.metadata[data_l.metadata.Block==8].RT)
    B9  = np.mean(data_l.metadata[data_l.metadata.Block==9].RT)
    B10 = np.mean(data_l.metadata[data_l.metadata.Block==10].RT)

    blocks_RTs = [B3, B4, B5, B6, B7, B8, B9, B10]

    return blocks_RTs
