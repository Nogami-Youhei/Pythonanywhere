from django.shortcuts import render
import numpy as np
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import PLSRegression


def index(request):
    params = {
        'range': range(1, 11),
        'n': 0,
    }

    if (request.POST.get('目的変数')):
        n = request.POST['n']

        X = []
        y = np.array(request.POST['目的変数'].split()).astype('float')

        for i in eval(n):
            X.append(np.array(request.POST['説明変数' + str(i)].split()).astype('float'))

        PCR_model = make_pipeline(StandardScaler(), 
                        PCA(n_components=3), 
                        LinearRegression())
        
        X = np.array(X).T
        print(X)
        print(y)
        PCR_model.fit(X, y)
        components = PCR_model.named_steps["pca"].components_
        variance_ratio = PCR_model.named_steps["pca"].explained_variance_ratio_
        predict = PCR_model.predict(X)
        R2 = round(PCR_model.score(X, y), 2)

        params = {
            'range': range(1, 11),
            'n': 0,
            'components': 'components:<br>' + str(components),
            'variance_ratio': 'variance_ratio:<br>' + str(variance_ratio),
            'predict': 'predict:<br>' + str(predict),
            'R2': 'R2:<br>' + str(R2),
        }
        return render(request, 'pls/index.html', params)

    if (request.method == 'POST'):
        n = range(1, int(request.POST['n']) + 1)

        params = {
            'range': range(1, 11),
            'n': n,
        }
    
    return render(request, 'pls/index.html', params)