"""
All util functions using to plot results
"""
from matplotlib.font_manager import FontProperties
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('Agg')

def set_fonts():
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Calibri')
    return font

def smooth(y, window, mode):
    box = np.ones(window)/window
    y_smooth = np.convolve(y, box, mode=mode)
    return y_smooth

def scores_plt(scores):
    fig, ax = plt.subplots(1, 1)
    plt.tight_layout()
    im = ax.imshow(scores, interpolation='lanczos', origin='lower', cmap='RdBu_r',
                   extent=subset.times[[0, -1, 0 , -1]], vmin=0., vmax=1.)
    ax.set_xlabel('Testing Time (s)')
    ax.set_ylabel('Training Time (s)')
    ax.set_title('Temporal generalization')
    ax.axvline(0, color='k')
    ax.axhline(0, color='k')
    ax.xaxis.set_ticks_position('bottom')
    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.show()

def diag_scores_plt(scores_diag, apply_smooth):
    if apply_smooth:
        window=50
        mode='valid'
        scores_diag = smooth(y, window, mode)
        print(subset.times.shape)
        print(y_smooth.shape)
    fig, ax = plt.subplots()
    ax.plot(subset.times, scores_diag, label='score')
    ax.axhline(.5, color='k', linestyle='--', label='chance')
    ax.set_xlabel('Times')
    ax.set_ylabel('AUC')  # Area Under the Curve
    ax.legend()
    ax.axvline(.0, color='k', linestyle='-')
    ax.set_title('Sensor space decoding')
    plt.tight_layout()
    plt.show()

def plot_scores_stat(diag_scores, clusts):
    font=set_fonts();
    [t_obs, clusters, clusters_pv, H0] = clusts
    # binned times
    times=np.asarray([-0.4,-0.3,-0.2,-0.1,0.1,0.2,0.3,0.4])
    extent_times=subset.times[[0, -1, 0, -1]]

    # Plot the diagonal (it's exactly the same as the time-by-time decoding above)
    fig, ax = plt.subplots()
    plt.tight_layout()
    ax.plot(times, diag_scores, label='score')
    ax.axhline(.5, color='k', linestyle='--', label='chance')
    plt.ylim([0.43,0.65])
    ax.axvline(.0, color='k', linestyle='-')

    for i_clu, clu_idx in enumerate(clusters):
        clu_idx=clu_idx[0]
        print(clu_idx)
        # unpack cluster information, get unique indices
        if clusters_pv[i_clu] <= 0.05:
            h = plt.axvspan(times[clu_idx[0]], times[clu_idx[-1] - 1],
                            color='r', alpha=0.3)
            plt.legend((h, ), ('cluster p-value < 0.05', ))
        else:
            plt.axvspan(times[clu_idx[0]], times[clu_idx[-1] - 1], color=(0.3, 0.3, 0.3),
                        alpha=0.3)

    plt.tight_layout()
    plt.xlabel('Times',  fontproperties=font, fontsize=12, fontweight='bold')
    plt.ylabel('AUC', fontproperties=font, fontsize=12, fontweight='bold')#, labelpad=16,)
    plt.title('Decoding over time', fontproperties=font, fontweight='bold', fontsize=16)

    plt.legend(fontsize=11)
    plt.tight_layout()
