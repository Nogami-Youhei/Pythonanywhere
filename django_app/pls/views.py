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
        'range1': range(1, 11),
        'n': 0,
        'message': '※説明変数の数を選択してください'
    }

    if request.POST.get('目的変数'):
        if (int(request.POST['n']) - 1) < int(request.POST['n_components']):
            params = {
                'range1': range(1, 11),
                'n': 0,
                'message': '説明変数の数より主成分の数が多いです！'
            }

            return render(request, 'pls/index.html', params)

        X = []
        y = np.array(request.POST['目的変数'].split()).astype('float')

        for i in eval(request.POST['range2']):
            X.append(np.array(request.POST['説明変数' + str(i)].split()).astype('float'))

        PCR_model = make_pipeline(StandardScaler(), 
                        PCA(n_components=int(request.POST['n_components'])), 
                        LinearRegression())
        
        X = np.array(X).T
        print(X)
        print(y)
        PCR_model.fit(X, y)
        components = PCR_model.named_steps["pca"].components_
        variance_ratio = PCR_model.named_steps["pca"].explained_variance_ratio_
        predict = PCR_model.predict(X)
        R2 = round(PCR_model.score(X, y), 4)

        params = {
            'range1': range(1, 11),
            'n': 0,
            'components1': 'components:<br>',
            'components2': components,
            'variance_ratio': 'variance_ratio:<br>' + str(variance_ratio),
            'predict': 'predict:<br>' + str(predict),
            'R2': 'R2: ' + str(R2),
        }
        return render(request, 'pls/index.html', params)

    if (request.method == 'POST'):

        params = {
            'range1': range(1, 11),
            'range2': range(1, int(request.POST['n']) + 1),
            'n': int(request.POST['n']) + 1,
            'message': '※値を入力してください',
        }
    
    return render(request, 'pls/index.html', params)