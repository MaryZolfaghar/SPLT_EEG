"""
Generate random data for creating a null distribution for temporal-
generalization/decoding results
"""

import numpy as np
import datetime

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from mne.decoding import cross_val_multiscore, LinearModel, \
                         GeneralizingEstimator, Scaler, Vectorizer

def gen_null_data(args, Grp_data, cv):
    le = LabelEncoder()
    clf_SVC  = make_pipeline(
                          StandardScaler(),
                          LinearModel(LinearSVC(random_state=args.random_state,
                                                max_iter=args.null_max_iter)))

    X = Grp_data.copy()._data
    y = le.fit_transform(Grp_data.copy().metadata.Trgt_Loc_main)

    rand_scores = []
    rand_diag = []

    rand_scores_fit = []
    rand_diag_fit = []
    print('**************************************************************')
    print('Start of the rand loop:\n')
    print(str(datetime.datetime.now()))
    print('**************************************************************')

    for nitr in range(args.loop_null_iter):
        print('**************************************************************')
        print('**************************************************************')
        print('Iteration:\n')
        print(str(datetime.datetime.now()))
        print(nitr)
        print('**************************************************************')
        print('**************************************************************')
        true_Y = y.copy();
        indx = np.random.permutation(true_Y.shape[0]);
        shuffled_Y = true_Y.copy()[indx];
        shuffled_Y = le.fit_transform(shuffled_Y.copy());

        time_gen = GeneralizingEstimator(clf_SVC, scoring=args.scoring,
                                         n_jobs=args.n_jobs, verbose=True)


        scores = cross_val_multiscore(time_gen, X, shuffled_Y, cv=cv, n_jobs=args.n_jobs)
        scores = np.mean(scores, axis=0) #scores with cv
        scores_diag = np.diag(scores)

        rand_scores.append(scores)
        rand_diag.append(scores_diag)

        # Without using cv, train and test on the same data
        X = Grp_data.copy()._data
        y = le.fit_transform(Grp_data.copy().metadata.Trgt_Loc_main)
        time_gen.fit(X=X ,y=y)
        scores = time_gen.score(X=X, y=y) #scores without cv
        scores_diag = np.diag(scores)

        rand_scores_fit.append(scores)
        rand_diag_fit.append(scores_diag)

        if (nitr>0 and nitr%30==0):
             
    print('**************************************************************')
    print('End of the rand loop:\n')
    print(str(datetime.datetime.now()))
    print('**************************************************************')
    rand_scores_pck = (rand_scores.copy(), rand_diag.copy())
    rand_scores_pck_fit = (rand_scores_fit.copy(), rand_diag_fit.copy())

    return rand_scores_pck, rand_scores_pck_fit
