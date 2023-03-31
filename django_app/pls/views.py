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
        'message': '※縦はデータ、横は説明変数となるように、<br>エクセルからコピペして貼り付けてください',
    }
    if (request.method == 'POST'):
        try:
            y = np.array(request.POST['目的変数'].split()).astype('float')
            li = [i.split() for i in request.POST['説明変数'].split('\n')]
            if li[-1] == []:
                li.remove([])
            X = np.array(li).astype('float')
            n_components = int(request.POST['n_components'])

            if X.shape[1] < n_components:
                params = {
                    'range1': range(1, 11),
                    'message': '説明変数の数より主成分の数が多いです！'
                }
                return render(request, 'pls/index.html', params)

            PCR_model = make_pipeline(StandardScaler(), 
                            PCA(n_components=n_components), 
                            LinearRegression())
            
            PCR_model.fit(X, y)
            components = PCR_model.named_steps["pca"].components_
            variance_ratio = PCR_model.named_steps["pca"].explained_variance_ratio_
            predict = PCR_model.predict(X)
            R2 = round(PCR_model.score(X, y), 4)
            params = {
                'range1': range(1, 11),
                'components1': 'components:<br>',
                'components2': components,
                'variance_ratio': 'variance_ratio:<br>' + str(variance_ratio),
                'predict': 'predict:<br>' + str(predict),
                'R2': 'R2: ' + str(R2),
            }
            return render(request, 'pls/index.html', params)
        except Exception as e:
            params = {
                'range1': range(1, 11),
                'message': e,
            }

    return render(request, 'pls/index.html', params)