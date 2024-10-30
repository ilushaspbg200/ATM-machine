import csv
import datetime

import psycopg2

now_data = datetime.datetime.utcnow().strftime("%H:%M-%d.%m.%Y")
class SQL_atm:

    @staticmethod
    def create_table():
        with psycopg2.connect(database = 'atm', user='postgres', password='17030508', host='localhost') as db:
            cur=db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS users_data(
            userid BIGSERIAL PRIMARY KEY,
            number_card INTEGER NOT NULL,
            pin_code INTEGER NOT NULL,
            balance INTEGER NOT NULL,
            phone_number varchar(12)
            );""")

    @staticmethod
    def insert_users(num_c,pin,bal,phone_number):
        with psycopg2.connect(database = 'atm', user='postgres', password='17030508', host='localhost') as db:
            cur=db.cursor()
            cur.execute(f"""INSERT INTO users_data(number_card,pin_code,balance,phone_number) 
            VALUES({num_c},{pin},{bal},'{phone_number}');""")
            print("Пользователь добавлен")
    @staticmethod
    def input_card(num_card):
        try:
            with psycopg2.connect(database='atm', user='postgres', password='17030508', host='localhost') as db:
                cur = db.cursor()
                cur.execute(f"""SELECT number_card FROM users_data WHERE number_card = {num_card};""")
                res = cur.fetchone()
                if res == None:
                    print("Введен неизвестный номер карты")
                    return False
                else:
                    print(f"""Введен номер карты: {num_card}""")
                    return True
        except:
            print("Введен некорректный номер карты!")

    @staticmethod
    def input_pin(num_card):
        pin_code = input("Введите ваш пин-код: ")
        try:
            with psycopg2.connect(database='atm', user='postgres', password='17030508', host='localhost') as db:
                cur = db.cursor()
                cur.execute(f"""SELECT pin_code FROM users_data WHERE number_card = {num_card};""")
                res = cur.fetchone()[0]
                if int(pin_code) == res:
                    print("Введен верный пин-код")
                    return True
                else:
                    print("Введен неверный пин-код!")
                    return False
        except:
            print("Введен некорректный пин-код!")
            return False

    @staticmethod
    def info_balance(num_card):
        with psycopg2.connect(database='atm', user='postgres', password='17030508', host='localhost') as db:
            cur = db.cursor()
            cur.execute(f"""SELECT balance FROM users_data WHERE number_card = {num_card};""")
            res_inf_bal = cur.fetchone()[0]
            return res_inf_bal

    @staticmethod
    def withdraw_money(num_card):
        amount = input("Введите сумму которую желаете снять: ")
        try:
            with psycopg2.connect(database='atm', user='postgres', password='17030508', host='localhost') as db:
                cur = db.cursor()
                cur.execute(f"""SELECT balance FROM users_data WHERE number_card = {num_card};""")
                res_inf_bal = cur.fetchone()[0]
                if int(amount)>0:
                    if int(amount) > res_inf_bal:
                        print("На балансе недостаточно средств!")
                        return False
                    else:
                        cur.execute(f"""UPDATE users_data SET balance = balance - {amount} WHERE number_card = {num_card};""")
                        db.commit()
                        SQL_atm.info_balance(num_card)
                        SQL_atm.report_operation_1(now_data, num_card, "1", amount, "")
                        return True
                else:
                    print("Сумма должна быть положительной!")
                    return False
        except:
            print("Введена некорректная сумма!")
            return False

    @staticmethod
    def depositing_money(num_card):
        amount = input("Введите сумму которую желаете положить: ")
        with psycopg2.connect(database='atm', user='postgres', password='17030508', host='localhost') as db:
            cur = db.cursor()
            try:
                if int(amount) > 0:
                    cur.execute(f"""UPDATE users_data SET balance = balance + {amount} WHERE number_card = {num_card};""")
                    db.commit()
                    SQL_atm.info_balance(num_card)
                    SQL_atm.report_operation_1(now_data,num_card,"2",amount,"")
                    return True
                else:
                    print("Сумма должна быть положительной!")
                    return False
            except:
                print("Введена некорректная сумма")
                return False

    @staticmethod
    def input_operation(num_card):
        while True:
            operation = input("Введите операцию, которую хотите совершить:\n"
                              "1. Узнать баланс\n"
                              "2. Снять денежные средства\n"
                              "3. Внести денежные средства\n"
                              "4. Завершить работу\n"
                              "5. Перевести денежные средства\n"
                              "6. Показать номер телефона\n"
                              "7. Пополнить баланс телефона\n")
            if operation == "1":
                print(f"""Баланс вашей карты: {SQL_atm.info_balance(num_card)}""")
            elif operation == "2":
                SQL_atm.withdraw_money(num_card)
            elif operation == "3":
                SQL_atm.depositing_money(num_card)
            elif operation == "4":
                print("Спасибо за визит, всего добрейшего")
                return False
            elif operation == "5":
                SQL_atm.transfer_money(num_card)
            elif operation == "6":
                SQL_atm.show_phone_number(num_card)
            elif operation == "7":
                SQL_atm.transfer_to_the_phone_balance(num_card)
            else:
                print("Такой операции не найдено, попробуйте другую")

    @staticmethod
    def transfer_money(num_card):
        trans_num = input("Введите номер карты пользователя для перевода денежных средств: ")
        if trans_num != num_card:
            with psycopg2.connect(database='atm', user='postgres', password='17030508', host='localhost') as db:
                cur = db.cursor()
                try:
                    cur.execute(f"""SELECT number_card FROM users_data WHERE number_card = {trans_num};""")
                    if cur.fetchone():
                        amount = input("Введите сумму, которую желаете перевести: ")
                        cur.execute(f"""SELECT balance FROM users_data WHERE number_card = {num_card}""")
                        res = cur.fetchone()[0]
                        if res > int(amount):
                            if int(amount) > 0:
                                cur.execute(f"""UPDATE users_data SET balance = balance + {amount} WHERE number_card = {trans_num};""")
                                db.commit()
                                cur.execute(f"""UPDATE users_data SET balance = balance - {amount} WHERE number_card = {num_card}; """)
                                db.commit()
                                print("Перевод проведен успешно")
                                SQL_atm.info_balance(num_card)
                                SQL_atm.report_operation_1(now_data, num_card, "3", amount, "")
                                SQL_atm.report_operation_2(now_data,trans_num,"3",amount,num_card)
                                return True
                            else:
                                print("Сумма должна быть положительной!")
                                return False
                        else:
                            print("У вас недостаточно средств на счете!")
                            return False
                    else:
                        print("Пользователь с данной картой не найден!")
                        return False

                except:
                    print("Некорректные данные! Убедитесь, что сумма перевода и номер карты получателя являются числами!")
                    return False
        else:
            print("Нельзя совершать переводы самому себе!")
            return False
    @staticmethod
    def report_operation_1(now_date,number_card,type_operation,amount,payee):
        user_data=[(now_date,number_card,type_operation,amount,payee)]
        with open("report_1.csv",'a',newline='') as file:
            writer = csv.writer(file,delimiter=";")
            writer.writerows(
                user_data
            )
    @staticmethod
    def report_operation_2(now_date,payee,type_operation,amount,number_card):
        user_data= [(now_date,payee,type_operation,amount,number_card)]
        with open("report_2.csv",'a',newline = '') as file:
            writer = csv.writer(file,delimiter=";")
            writer.writerows(
                user_data
            )

    @staticmethod
    def show_phone_number(num_card):
        print("Пожалуйста, введите пин-код еще раз для подтверждения операции ")
        if SQL_atm.input_pin(num_card):
            with psycopg2.connect(database='atm',user='postgres',password='17030508',host='localhost') as db:
                cur = db.cursor()
                cur.execute(f"""SELECT phone_number FROM users_data WHERE number_card = '{num_card}';""")
                res=cur.fetchone()[0]
                print(f"""Номер телефона, к которому привязана карта: {res}""")

    """ЗДЕСЬ РЕАЛИЗУЮ ПОПОЛНЕНИЕ БАЛАНСА ТЕЛЕФОНА В ТАБЛИЦЕ mobile_users"""
    @staticmethod
    def transfer_to_the_phone_balance(num_card):
        number = input("Введите номер телефона, баланс которого желаете пополнить, учитывая, что номер должен начинаться с '+7': ")
        try:
            if number[:2]=='+7' and len(number)==12 and int(number[1:]):
                with psycopg2.connect(database='mobile_calls',user='postgres',password='17030508',host='localhost') as db:
                    cur=db.cursor()
                    cur.execute(f"""SELECT phone_number FROM mobile_users WHERE phone_number = '{number}'; """)
                    res = cur.fetchone()
                    """если такой телефон существует то"""
                    if res:
                        sum_of_transf = input("Введите сумму, которую желаете перевести на баланс выбранного номера: ")
                        try:
                            if int(sum_of_transf) > 0:

                                if int(sum_of_transf) <= SQL_atm.info_balance(num_card):
                                    """Пополняю баланс телефона"""
                                    cur.execute(f"""UPDATE mobile_users 
                                    SET balance=balance+{int(sum_of_transf)}
                                    WHERE phone_number = '{number}';""")

                                    """Списываю деньги со счета в банке"""
                                    with psycopg2.connect(database='atm',user='postgres',password='17030508',host='localhost') as db2:
                                        curs=db2.cursor()
                                        curs.execute(f"""UPDATE users_data 
                                        SET balance = balance - {int(sum_of_transf)}
                                        WHERE number_card= '{num_card}';""")
                                    print("Операция успешно выполнена")



                                else:
                                    print("Сумма перевода не должна превышать вашего баланса.")
                            else:
                                print("Сумма должна быть положительной")
                        except:
                            print("Сумма должна быть числом")
                    else:
                        print("Такой номер не найден, убедитесь, что данные введены верно")


            else:
                print("Неверный формат номера телефона")

        except:
            print("Неверный формат номера телефона")