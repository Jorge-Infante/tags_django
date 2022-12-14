# Django
from django.http import HttpResponse
from django.shortcuts import render

# Python
import datetime
from datetime import timedelta
import json
import requests
import shutil
import csv
import os

def download_tags(request):
    template_name = 'download_tags.html'
    if request.method == 'POST':
        response = HttpResponse(content_type='text/csv')
        tag=request.POST.get('tag')
        date01=request.POST.get('initDate')
        date02=request.POST.get('finishDate')
        
        if tag!='':
            values_lis = []

            init_date=date01+'T'+'00:00:00'+'Z'
            start_date = datetime.datetime.strptime(init_date, "%Y-%m-%dT%H:%M:%SZ")

            finish_date=date02+'T'+'23:59:59'+'Z'
            end_date = datetime.datetime.strptime(finish_date, "%Y-%m-%dT%H:%M:%SZ")
            
            payload={}
            headers = {
                'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFlM2Y4ZDRhLWVjNTMtNDhkZC1hNGYwLTAwYTBiZTViNjVlOCJ9.eyJ0eXBlIjoic2VydmljZSIsInZlcnNpb24iOiIyLjAiLCJ0ZW5hbnRpZCI6IjAyODlkZGZmLTRkZWQtNDFjMi1hZmY0LWI2MjYzNmQ2Y2JhZiIsInNpaWQiOiIxNjZhMmI0OC03ZDNmLTRlYmMtOTQzNi0zYzllZGNjNTU5NjQiLCJqdGkiOiIwNWQzNTMwZS05ZjFlLTRiYTEtOGIwZi1kODFkNTg1ZWY0MmMiLCJpc3MiOiJwcm9vZm9maWRlbnRpdHlzZXJ2aWNlIn0.lQtqTWgN6IA28PXmOFEm_C9xO5-8CGraDu0y9TDac5SQ2ufzWz_lj_hSZwQTd94y5brzLd4QyTOT18Rfcr8s2_zmQUjurR4hbdWOuRkPEP1cDQfHI1qhXVzB4-Zhf-D8y2kdD-IvoKr0917WtqkiasN8blCdxn4qMoizbJSUFqmsRJ4EedWHOdrcdcnj-po2g0Myb4OhJYay6zqVRYmRl5OxOAk2OQMGh0fgDmwZjqorqXsRP8stBDzwpueLr_5TymcUR3ezBRJcjR5jCy3tiQl9V-6XN3yskCiUtHnkKUE3JWuKB5o0pTyF-jPWNqwY_qG62vbFnuJdowZRQjwPxg'
            }
            print('Iniciando tag: {}'.format(tag))

            delta = timedelta(hours=12) 
            while start_date <= end_date: 
                delta_parcial=timedelta(hours=12)
                end_parcial_date=start_date+delta_parcial
                    

                url = "https://online.wonderware.com/apis/Historian/v2/AnalogSummary ?$filter=FQN+eq+'Vasconia_OPC.{}' and StartDateTime ge {} +and+EndDateTime+le+ {}&Resolution=10000&$select=FQN,Last,LastDateTime,StartDateTime,EndDateTime".format(tag,start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),end_parcial_date.strftime("%Y-%m-%dT%H:%M:%SZ"))
                resp = requests.request("GET", url, headers=headers, data=payload)
                
                try:
                    res =json.loads(resp.text) 
                    print(res['value'])   
                    if('value' in res.keys()):
                        values_lis=values_lis+res['value']
                    else:
                        pass
                except:
                    print("Error en el dato")

                
                print('Iniciando desde: ',start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),' Hasta: ',end_parcial_date)
                start_date += delta

            name_file=tag+'.csv'
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(name_file)
           
            writer = csv.DictWriter(response,delimiter=';',fieldnames=['FQN','StartDateTime','EndDateTime','Last','LastDateTime'])
            writer.writeheader()
            writer.writerows(values_lis)
            
            return response
        else:
            response = HttpResponse(content_type='text/zip')
            os.remove('static/out.zip')
            with open ("config.json") as archivo:
                datos=json.load(archivo)
                print(datos)

            for tag in datos['tags']:
                values_lis = []
                init_date=date01+'T'+'00:00:00'+'Z'
                start_date = datetime.datetime.strptime(init_date, "%Y-%m-%dT%H:%M:%SZ")

                finish_date=date02+'T'+'23:59:59'+'Z'
                end_date = datetime.datetime.strptime(finish_date, "%Y-%m-%dT%H:%M:%SZ")
                payload={}
                headers = {
                    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFlM2Y4ZDRhLWVjNTMtNDhkZC1hNGYwLTAwYTBiZTViNjVlOCJ9.eyJ0eXBlIjoic2VydmljZSIsInZlcnNpb24iOiIyLjAiLCJ0ZW5hbnRpZCI6IjAyODlkZGZmLTRkZWQtNDFjMi1hZmY0LWI2MjYzNmQ2Y2JhZiIsInNpaWQiOiIxNjZhMmI0OC03ZDNmLTRlYmMtOTQzNi0zYzllZGNjNTU5NjQiLCJqdGkiOiIwNWQzNTMwZS05ZjFlLTRiYTEtOGIwZi1kODFkNTg1ZWY0MmMiLCJpc3MiOiJwcm9vZm9maWRlbnRpdHlzZXJ2aWNlIn0.lQtqTWgN6IA28PXmOFEm_C9xO5-8CGraDu0y9TDac5SQ2ufzWz_lj_hSZwQTd94y5brzLd4QyTOT18Rfcr8s2_zmQUjurR4hbdWOuRkPEP1cDQfHI1qhXVzB4-Zhf-D8y2kdD-IvoKr0917WtqkiasN8blCdxn4qMoizbJSUFqmsRJ4EedWHOdrcdcnj-po2g0Myb4OhJYay6zqVRYmRl5OxOAk2OQMGh0fgDmwZjqorqXsRP8stBDzwpueLr_5TymcUR3ezBRJcjR5jCy3tiQl9V-6XN3yskCiUtHnkKUE3JWuKB5o0pTyF-jPWNqwY_qG62vbFnuJdowZRQjwPxg'
                }

                print('Iniciando tag: {}'.format(tag))

                delta = timedelta(hours=12) 
                while start_date <= end_date: 
                    delta_parcial=timedelta(hours=12)
                    end_parcial_date=start_date+delta_parcial
                        

                    url = "https://online.wonderware.com/apis/Historian/v2/AnalogSummary ?$filter=FQN+eq+'Vasconia_OPC.{}' and StartDateTime ge {} +and+EndDateTime+le+ {}&Resolution=10000&$select=FQN,Last,LastDateTime,StartDateTime,EndDateTime".format(tag,start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),end_parcial_date.strftime("%Y-%m-%dT%H:%M:%SZ"))
                    respon = requests.request("GET", url, headers=headers, data=payload)
                    
                    try:
                        res =json.loads(respon.text)    
                        if('value' in res.keys()):
                            values_lis=values_lis+res['value']
                        else:
                            pass
                    except:
                        print("Error en el dato")

                    
                    print('Iniciando desde: ',start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),' Hasta: ',end_parcial_date)
                    start_date += delta

                name_file=tag+'.csv'
                mtn_path = r'static/out/'
                txt_file_csv_path = os.path.join(mtn_path, name_file)
                with open(txt_file_csv_path, 'w', newline='') as csvfile:
                    fieldnames = ['FQN','StartDateTime','EndDateTime','Last','LastDateTime']
                    writer = csv.DictWriter(csvfile,delimiter=';', fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(values_lis)

                    print('\n Sale dato ----> \n')

            shutil.make_archive('static/out/', 'zip', root_dir='static')
            for i in datos['tags']:
                os.remove('static/out/'+i+'.csv')

            response=HttpResponse(open('static/out.zip', 'rb').read())   
            response['Content-Disposition'] = 'attachment; filename="{}"'.format('out.zip')
            
        
        return response
    else:
        return render(request,template_name)