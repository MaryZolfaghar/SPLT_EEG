"""
Apply Temporal Generalization approch from MNE

https://mne.tools/stable/auto_tutorials/machine-learning\
/plot_sensors_decoding.html#temporal-generalization
"""
import numpy as np

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from mne.decoding import cross_val_multiscore, LinearModel, \
                         GeneralizingEstimator, Scaler, Vectorizer

def apply_temp_gen(args, Grp_data, cv):
    le = LabelEncoder()
    clf_SVC  = make_pipeline(
                          StandardScaler(),
                          LinearModel(LinearSVC(random_state=args.random_state,
                                                max_iter=args.max_iter)))
    X=Grp_data.copy()._data
    y=le.fit_transform(Grp_data.copy().metadata.Trgt_Loc_main)

    time_gen = GeneralizingEstimator(clf_SVC, scoring=args.scoring,
                                     n_jobs=args.n_jobs, verbose=True)
    #print('In ApplyTempGen the size of y and X data is\n')
    #print(np.unique(y))
    #print(np.unique(Grp_data.copy().metadata.Trgt_Loc_main))

    scores = cross_val_multiscore(time_gen, X, y, cv=cv, n_jobs=args.n_jobs)
    scores = np.mean(scores, axis=0) #scores with cv
    scores_diag = np.diag(scores)
    scores_pck = (scores.copy(), scores_diag.copy())

    # Without using cv, train and test on the same data
    X = Grp_data.copy()._data
    y = le.fit_transform(Grp_data.copy().metadata.Trgt_Loc_main)
    time_gen.fit(X=X ,y=y)
    scores = time_gen.score(X=X, y=y) #scores without cv
    scores_diag = np.diag(scores)
    scores_pck_fit = (scores.copy(), scores_diag.copy())

    return scores_pck, scores_pck_fit
