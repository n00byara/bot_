import os
from collections import defaultdict

import pandas as pd
from xlsxwriter import Workbook

from text import Message

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
columns = [
    "id",
    "Тренер",
    "Тип мероприятия",
    "Название мероприятия",
    "Дата проведения мероприятия",
    "Имя Пользователя",
    "Телеграм username",
    Message.QUIZ_QUESTION_2.value,
    Message.QUIZ_QUESTION_3.value,
    Message.QUIZ_QUESTION_4.value,
    Message.QUIZ_QUESTION_7.value,
    Message.QUIZ_QUESTION_5.value,
    Message.QUIZ_QUESTION_6.value,
]


def group_by_student(rows):
    grouped = defaultdict(list)

    for row in rows:
        grouped[row["student_id"]].append(row)

    result = []
    for student_id, records in grouped.items():
        first = records[0]
        result.append({
            "student_id": student_id,
            "student_username": first["student_username"],
            "teacher_id": first["teacher_id"],
            "quiz_type": first["quiz_type"],
            "quiz_date": first["quiz_date"],
            "quiz_name": first["quiz_name"],
            "answers": [
                {
                    "answer": r["answer"],
                    "answer_id": r["answer_id"]
                }
                for r in records
            ]
        })

    return result

def create_excel_from_dict_list(answers: list, output_filename: str = "template.xlsx", sheet_name=""):
    tmp_folder = f"{BASE_DIR}/tmp"

    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    data = group_by_student(answers)

    filepath = os.path.join(tmp_folder, output_filename)
    workbook = Workbook(f"{tmp_folder}/{output_filename}")
    worksheet = workbook.add_worksheet("Data")

    for col_idx, column_name in enumerate(columns):
        worksheet.write(0, col_idx, column_name)

    # Запись данных
    for row_idx, entry in enumerate(data, start=1):
        answers_by_id = {a["answer_id"]: a["answer"] for a in entry["answers"]}

        row = [
            entry["student_id"],
            entry["teacher_id"],
            entry["quiz_type"].strip(),
            entry["quiz_name"].strip(),
            entry["quiz_date"].strftime("%d.%m.%Y"),
            answers_by_id.get(1, ""),
            entry["student_username"].strip(),
            answers_by_id.get(2, ""),
            answers_by_id.get(3, ""),
            answers_by_id.get(4, ""),
            answers_by_id.get(5, ""),
            answers_by_id.get(6, ""),
            answers_by_id.get(7, ""),
        ]

    for col_idx, value in enumerate(row):
        worksheet.write(row_idx, col_idx, value)

    worksheet.set_column(0, len(columns) - 1, 20)
    workbook.close()

    return filepath

def remove_file(file_path = None):
    if file_path:
        os.remove(file_path)