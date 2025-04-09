import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sql_query import SQL_atm
"""Создание базы данных (если требуется)"""
# db = psycopg2.connect(user='login',password='pass',host='localhost')
# db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# curs = db.cursor()
# curs.execute("""CREATE DATABASE atm;""")
class ATM:
    SQL_atm.create_table()
    number_card = input("Введите номер карты: ")
    while True:
        if SQL_atm.input_card(number_card):
            if SQL_atm.input_pin(number_card):

                SQL_atm.input_operation(number_card)
                break
            else:
                break

        else:
            break

