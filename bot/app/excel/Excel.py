import os
import pandas as pd

class Excel:
    def create_empty_excel(self, columns: list, filename: str, sheet_name: str = 'Sheet1'):
        df = pd.DataFrame(columns=columns)

        if not os.path.exists('excel_files'):
            os.makedirs('excel_files')

        filepath = os.path.join('excel_files', filename)
        excel_writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
        df.to_excel(excel_writer, index=False, sheet_name=sheet_name, freeze_panes=(1, 0))
        excel_writer._save()

        return filepath
    
    def create_tabel_users(self):
        filepath = self.create_empty_excel(columns=['Имя', 'Адрес', 'Email', 'Телефон'],
            filename='users.xlsx')