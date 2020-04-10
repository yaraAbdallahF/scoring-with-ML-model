import sqlalchemy as db
import pandas as pd
import numpy as np 
import h5py as h5

import json
from keras.models import model_from_json
import pandas as pd




conn = db.create_engine('postgresql://iti:iti@localhost/datamanagement')
conn.table_names()

q = Diabtes_batch = """SELECT pregnancies,glucose,bloodpressure ,skinthickness ,insulin ,bmi,diabetespedigreefunction ,age FROM Public."diabetes_unscored"
						EXCEPT  
						SELECT pregnancies,glucose,bloodpressure ,skinthickness ,insulin ,bmi,diabetespedigreefunction ,age FROM Public."diabetes_scored";"""
result = pd.read_sql(q,conn)

jsonFile = open('model.json', 'r')
jsonPredictionModel = jsonFile.read()
jsonFile.close()
Model = model_from_json(jsonPredictionModel)

Model.load_weights("model.h5")
predictedData = pd.DataFrame(result)
predictedData = predictedData.iloc[: , :].values
arrValues = np.array(predictedData)

predictions = Model.predict(arrValues)
result['outcome'] = predictions
result['outcome'] = result['outcome'].apply(lambda x : 1 if x >= 0.5 else 0 ) 
result.to_sql(name = 'diabetes_scored', 
                con=conn,                                           
                schema = 'public',                                  
                if_exists='append', index=False)
print('DOne')