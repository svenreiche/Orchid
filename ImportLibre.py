import pandas as pd
import json

def importCVS(file):
    imp = pd.read_csv(file)
    ndata=imp['Name'].size

    dborchid={}
    for i in range(ndata):
        dborchid[str(imp['Name'][i])]={'ID':int(imp['ID'][i]),'Anzahl':int(imp['Anzahl'][i]),'Gattung':imp['Gattung'][i]}


    with open('OrchidDB_import.json','w') as out:
        json.dump(dborchid,out,indent=4,sort_keys=True)

importCVS('FromBase_Orchid.csv')