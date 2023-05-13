from django.shortcuts import render
from django.http import FileResponse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import PLSRegression
import re
import os
import time
import shutil
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import selenium
import pandas as pd
from googletrans import Translator
import random
import openpyxl
import openpyxl as xl
from openpyxl.styles import Alignment
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter


def index(request):
    return render(request, 'pls/index.html')

def outline(request):
    return render(request, 'pls/outline.html')

def pls(request):
    params = {
        'range1': range(1, 11),
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
                return render(request, 'pls/pls.html', params)

            PLS_model = PLSRegression(n_components=n_components)
            PLS_model.fit(X, y)
            predict = PLS_model.predict(X)
            R2 = round(PLS_model.score(X, y), 4)
            params = {
                'range1': range(1, 11),
                'coef_': 'coef_:<br>' + str(PLS_model.coef_),
                'intercept_': 'intercept_:<br>' + str(PLS_model.intercept_),
                'predict': 'predict:<br>' + str(predict),
                'R2': 'R2: ' + str(R2),
            }
            return render(request, 'pls/pls.html', params)
        except Exception as e:
            params = {
                'range1': range(1, 11),
                'message': e,
            }

    return render(request, 'pls/pls.html', params)

def pcr(request):
    params = {
        'range1': range(1, 11),
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
                return render(request, 'pls/pcr.html', params)

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
            return render(request, 'pls/pcr.html', params)
        except Exception as e:
            params = {
                'range1': range(1, 11),
                'message': e,
            }

    return render(request, 'pls/pcr.html', params)

def scraping(request):
    if (request.method == 'POST'):
        def discriminate_jp_en(string):
            if re.search(r'[ぁ-ん]+|[ァ-ヴー]+|[一-龠]+', string):
                return False
            else:
                return True

        options = webdriver.ChromeOptions()
        user_agent = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36']

        UA = user_agent[random.randrange(0, len(user_agent), 1)]
        options.add_argument('--user-agent=' + UA)

        #pluginfile = 'proxy_auth_plugin.zip'
        #options.add_extension(pluginfile)
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument("--disable-gpu")

        with webdriver.Chrome(options=options) as driver:
            i = 0
            result = []
            keyword = '+'.join(request.POST['keyword'].split())
            num = int(request.POST['num'])
            url = 'https://www.jstage.jst.go.jp/result/global/-char/ja?globalSearchKey=' + keyword
            driver.get(url)

            while True:
                url = driver.current_url
                time.sleep(1)
                html = driver.page_source.encode('utf-8')
                soup = BeautifulSoup(html, 'html.parser')
                elems = soup.find('ul', class_='search-resultslisting').find_all('li')
                tr = Translator()
                for elem in elems:
                    print(f'{i+1:03d}. {elem.find("a").text}')
                    line = pd.Series(index=['タイトル', 'URL', '学会誌', '出版年', '巻・ページ', '発行日', '公開日', '要約'], dtype=object)
                    line.name = f'{i+1:03d}'
                    anchor = elem.find('a').text
                    if discriminate_jp_en(anchor):
                        anchor = tr.translate(anchor.strip(), src="en", dest="ja").text
                    line[0] = anchor
                    link = elem.find('a')['href']
                    line[1] = link
                    detail = re.split(r'[\n\t]+', elem.find('div', class_='searchlist-additional-info').text)
                    line[2:4] = detail[1:3]
                    line[-3:-1] = detail[-3:-1]
                    line[4] = ', '.join(detail[3:-3])
                    driver.get(link)
                    time.sleep(1)
                    html = driver.page_source.encode('utf-8')
                    soup = BeautifulSoup(html, 'html.parser')
                    abstract = soup.find('p', class_='global-para-14')
                    if not abstract:
                        line[-1] = ('要約なし')
                    elif abstract.text == '\n':
                        if not abstract.next_sibling:
                            line[-1] = ('要約なし')
                        elif abstract.next_sibling.text == '\n':
                            line[-1] = ('要約なし')
                        else:
                            sibling = abstract.next_sibling
                            if discriminate_jp_en(sibling.text):
                                sibling = tr.translate(sibling.text.strip(), src="en", dest="ja")
                            line[-1] = sibling.text.strip()            
                    else:
                        if discriminate_jp_en(abstract.text):
                            abstract = tr.translate(abstract.text.strip(), src="en", dest="ja")
                        line[-1] = abstract.text.strip()
                    result.append(line)
                    i += 1
                    if i == num:
                        break
                if i == num:
                    break
                driver.get(url)
                ul = driver.find_element(By.XPATH, '//*[@id="search-pagination-wrap-top"]/div/div[1]/ul')
                button = ul.find_elements(By.TAG_NAME, 'li')[-2]
                if button.get_attribute('class') == 'inactive-page':
                    print('\n検索結果を全て出力しました。')
                    break
                button.click()
            
            temp_dir = 'temp'
            shutil.rmtree(temp_dir)
            os.makedirs(temp_dir, exist_ok=True)
            df = pd.concat(result, axis=1).T
            df.to_excel(f'temp/{keyword}.xlsx')

        wb = openpyxl.load_workbook(f"temp/{keyword}.xlsx")
        ws = wb.active

        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 25
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 15
        ws.column_dimensions['F'].width = 15
        ws.column_dimensions['G'].width = 15
        ws.column_dimensions['H'].width = 15
        ws.column_dimensions['I'].width = 50
        wrap_text = xl.styles.Alignment(wrapText=True, vertical='center')

        for row in range(2, ws.max_row+1):
            ws.row_dimensions[row].height = 100

        for row in ws.iter_rows():
            for cell in row:
                cell.alignment = wrap_text
                
        for cell in ws[f'I2:I{ws.max_row}']:
            cell[0].alignment = xl.styles.Alignment(wrapText=True, vertical='top')
            
        for cell in ws['A']:
            cell.alignment = xl.styles.Alignment(wrapText=True, horizontal='center', vertical='center')
            
        for cell in ws[f'C2:C{ws.max_row}']:
            cell[0].hyperlink = cell[0].value
            cell[0].font = Font(color="0000FF", underline="single")

        wb.save(f'temp/{keyword}.xlsx')

        filename, filepath = f'{keyword}.xlsx', f'temp/{keyword}.xlsx'
        return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)
    
    return render(request, 'pls/scraping.html')