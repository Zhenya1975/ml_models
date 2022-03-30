import pandas as pd

def sap_counter_data_cleanup():
  """обработка таблицы с данными о наработке из сап"""
  raw_motohours_data = pd.read_csv('data/sap_counters_data.csv', decimal = ',')
  # определяем уникальные номера документов, чтобы убрать дубликаты
  docs_list = list(set(raw_motohours_data['Документ измерений']))
  motohours_data = raw_motohours_data.loc[raw_motohours_data['Документ измерений'].isin(docs_list)]

  # выбираем строки, в которых указан МТЧ
  motohours_data = raw_motohours_data.loc[raw_motohours_data['ЕдиницаИзмерПризнака'].isin(['МТЧ'])]

  motohours_data = motohours_data.copy()
  # читаем даты3/30/2022
  try:
    motohours_data['datetime'] = pd.to_datetime(motohours_data['Дата'], format='%m/%d/%Y')
  except:
    print("не получилось конвертировать даты")

  # поле Показания счетчика - во float
  motohours_data['Показания счетчика'] = motohours_data['Показания счетчика'].astype(float)
  motohours_data['Единица оборудования'] = motohours_data['Показания счетчика'].astype(str)

  # переименовываем колонки 
  rename_columns_dict = {"Показания счетчика": "motohours", "Единица оборудования": "eo_code"}

  motohours_data.rename(columns=rename_columns_dict, inplace=True)
  # выбираем колонки
  motohours_data = motohours_data.loc[:, ["datetime", "eo_code", "motohours"]]

  # получаем полный список ео
  full_eo_list_actual = pd.read_csv("https://drive.google.com/uc?export=download&id=1GDB2rVwdquDQlI7qrVAlwwiaK2L86nzw", dtype=str)

  eo_data = full_eo_list_actual.loc[:, ['eo_code', 'operation_start_date']]
  # конвертируем operation_start_date в дату
  eo_data['operation_start_date'] = pd.to_datetime(eo_data['operation_start_date'], format='%Y-%m-%d')
  print(eo_data.info())
  print(eo_data)
  # print(motohours_data.info())
  # print(motohours_data)
  
sap_counter_data_cleanup()


