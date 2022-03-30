import pandas as pd
from sklearn import linear_model


def sap_counter_data_cleanup():
  """обработка таблицы с данными о наработке из сап"""
  raw_motohours_data = pd.read_csv('data/sap_counters_data.csv', decimal=',')
  # print(len(raw_motohours_data))
  # определяем уникальные номера документов, чтобы убрать дубликаты
  raw_motohours_data.drop_duplicates(subset=['Документ измерений'])
  # print(raw_motohours_data.info())

  # выбираем строки, в которых указан МТЧ
  motohours_data = raw_motohours_data.loc[raw_motohours_data['ЕдиницаИзмерПризнака'].isin(['МТЧ'])]
  
  motohours_data = motohours_data.copy()
  # читаем даты3/30/2022
  try:
    motohours_data['datetime'] = pd.to_datetime(motohours_data['Дата'], format='%m/%d/%Y')
  except:
    print("не получилось конвертировать даты")

  
  
  # поле Показания счетчика - во float
  # motohours_data['Показания счетчика'] = (motohours_data['Показания счетчика'].str.split()).apply(lambda x: float(x[0].replace(',', '')))
  motohours_data['Показания счетчика'] = motohours_data['Показания счетчика'].astype(float)
  motohours_data['Единица оборудования'] = motohours_data['Единица оборудования'].astype(str)
  
  
  # переименовываем колонки 
  rename_columns_dict = {"Показания счетчика": "motohours", "Единица оборудования": "eo_code"}

  motohours_data.rename(columns=rename_columns_dict, inplace=True)
  # выбираем колонки
  motohours_data = motohours_data.loc[:, ["datetime", "eo_code", "motohours"]]
  # print("motohours_data.info()", motohours_data.info())
  # motohours_data.to_csv('data/motohours_data.csv')
  
  # получаем полный список ео
  full_eo_list_actual = pd.read_csv("https://drive.google.com/uc?export=download&id=1GDB2rVwdquDQlI7qrVAlwwiaK2L86nzw", low_memory=False)

  eo_data = full_eo_list_actual.loc[:, ['eo_code',"eo_model_name",	"eo_model_id", "eo_description", "level_1_description", 'operation_start_date']]
  # конвертируем operation_start_date в дату
  eo_data['operation_start_date'] = pd.to_datetime(eo_data['operation_start_date'], format='%Y-%m-%d')
  
  # объединяем данные о наработке с данными о машинах
  motohours_data_eo = pd.merge(motohours_data, eo_data, on = 'eo_code', how = 'left')
  
  # Вычисляем ts для даты начала эксплуатации и для даты показания счетчика
  motohours_data_eo['operation_start_date_ts'] = (motohours_data_eo['operation_start_date'].astype(int) / 10**9).astype(int)
  motohours_data_eo['motohours_date_ts'] = (motohours_data_eo['datetime'].astype(int) / 10**9).astype(int)
  # точка относительно даты начала эксплуатации, в которой измерена наработка
  motohours_data_eo['motohours_measure_ts'] = motohours_data_eo['motohours_date_ts'] - motohours_data_eo['operation_start_date_ts']
  motohours_data_eo.to_csv("data/motohours_data_eo.csv")
  

  
# sap_counter_data_cleanup()

def ml_model():
  data_df = pd.read_csv("data/motohours_data_eo.csv")
  # print(data_df.info())
  # print(len(data_df))
  # на графике получившихся точек видны выбросы. убираем их
  data_df = data_df.loc[data_df['motohours_measure_ts'] > 50000000]
  # print(len(data_df))
  data_df = data_df.loc[:, ['motohours_measure_ts', 'motohours']]
  data_df.sort_values(['motohours_measure_ts'], inplace = True)

  model = linear_model.LinearRegression()
  model.fit(data_df[['motohours_measure_ts']].values, data_df.motohours)

  prediction = model.predict([[1641427200], [1668124800]])
  print(prediction)
  print("model.coef: ", model.coef_)
  print("model.intercept: ", model.intercept_)
  
  
ml_model()
