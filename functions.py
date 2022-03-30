import pandas as pd

def sap_counter_data_cleanup():
  """обработка таблицы с данными о наработке из сап"""
  raw_motohours_data = pd.read_csv('data/sap_counters_data.csv', decimal = ',')
  # определяем уникальные номера документов, чтобы убрать дубликаты
  docs_list = list(set(raw_motohours_data['Документ измерений']))
  motohours_data = raw_motohours_data.loc[raw_motohours_data['Документ измерений'].isin(docs_list)]

  # выбираем строки, в которых указан МТЧ
  motohours_data = raw_motohours_data.loc[raw_motohours_data['ЕдиницаИзмерПризнака'].isin(['МТЧ'])]

  # читаем даты3/30/2022
  try:
    motohours_data['datetime'] = pd.to_datetime(motohours_data['Дата'], format='%m/%d/%Y')
  except:
    print("не получилось конвертировать даты")

  # поле Показания счетчика - во float
  motohours_data['Показания счетчика'] = motohours_data['Показания счетчика'].astype(float)

  # переименовываем колонки 
  rename_columns_dict = {"Показания счетчика": "motohours", "Единица оборудования": "eo_code"}

  motohours_data.rename(columns=rename_columns_dict, inplace=True)
  # выбираем колонки
  motohours_data = motohours_data.loc[:, ["datetime", "eo_code", "motohours"]]
  
  print(motohours_data.info())
  print(motohours_data)
  

sap_counter_data_cleanup()