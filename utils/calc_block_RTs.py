""""
Extracting RTs for each blocks and each groups of locations
"""

import numpy as np
import mne
from scipy import stats

def calc_block_RTs(data_e, data_l):
    B3  = np.mean(data_e.metadata[data_e.metadata.Block==3].RT)
    B4  = np.mean(data_e.metadata[data_e.metadata.Block==4].RT)
    B5  = np.mean(data_e.metadata[data_e.metadata.Block==5].RT)
    B6  = np.mean(data_e.metadata[data_e.metadata.Block==6].RT)
    B7  = np.mean(data_l.metadata[data_l.metadata.Block==7].RT)
    B8  = np.mean(data_l.metadata[data_l.metadata.Block==8].RT)
    B9  = np.mean(data_l.metadata[data_l.metadata.Block==9].RT)
    B10 = np.mean(data_l.metadata[data_l.metadata.Block==10].RT)

    SE3  = stats.sem(data_e.metadata[data_e.metadata.Block==3].RT)
    SE4  = stats.sem(data_e.metadata[data_e.metadata.Block==4].RT)
    SE5  = stats.sem(data_e.metadata[data_e.metadata.Block==5].RT)
    SE6  = stats.sem(data_e.metadata[data_e.metadata.Block==6].RT)
    SE7  = stats.sem(data_l.metadata[data_l.metadata.Block==7].RT)
    SE8  = stats.sem(data_l.metadata[data_l.metadata.Block==8].RT)
    SE9  = stats.sem(data_l.metadata[data_l.metadata.Block==9].RT)
    SE10 = stats.sem(data_l.metadata[data_l.metadata.Block==10].RT)

    D3 = data_e.metadata[data_e.metadata.Block==3].RT
    D4 = data_e.metadata[data_e.metadata.Block==4].RT
    D5 = data_e.metadata[data_e.metadata.Block==5].RT
    D6 = data_e.metadata[data_e.metadata.Block==6].RT
    D7 = data_l.metadata[data_l.metadata.Block==7].RT
    D8 = data_l.metadata[data_l.metadata.Block==8].RT
    D9 = data_l.metadata[data_l.metadata.Block==9].RT
    D10 = data_l.metadata[data_l.metadata.Block==10].RT

    blocks_mean_RTs = [B3, B4, B5, B6, B7, B8, B9, B10]
    blocks_sem_RTs = [SE3, SE4, SE5, SE6, SE7, SE8, SE9, SE10]
    block_data_RTs = [D3, D4, D5, D6, D7, D8, D9, D10]

    return blocks_mean_RTs, blocks_sem_RTs, block_data_RTs
