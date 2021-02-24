from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_mentors(cursor: RealDictCursor) -> list:
    query = """
        SELECT first_name, last_name, city
        FROM mentor
        ORDER BY first_name"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_mentors_by_last_name(cursor: RealDictCursor, last_name: str) -> list:
    query = """
        SELECT first_name, last_name, city
        FROM mentor
        WHERE lower(last_name) = lower(%(last_name)s)"""
    value = {'last_name': last_name}
    cursor.execute(query, value)
    return cursor.fetchall()


@database_common.connection_handler
def get_city(cursor: RealDictCursor, city) -> list:
    query = """
        SELECT first_name, last_name, city
        FROM mentor
        WHERE city = (%(city)s);"""
    value = {'city': city}
    cursor.execute(query, value)
    return cursor.fetchall()


@database_common.connection_handler
def get_applicant_data_by_name(cursor: RealDictCursor, first_name, last_name) -> list:
    query = """
        SELECT first_name, last_name, phone_number
        FROM applicant
        WHERE lower(first_name) = lower(%(first_name)s) OR lower(last_name) = lower(%(last_name)s)"""
    value = {'first_name': first_name, 'last_name': last_name}
    cursor.execute(query, value)
    return cursor.fetchall()


@database_common.connection_handler
def get_applicant_data_by_email(cursor: RealDictCursor, email) -> list:
    email = f"%{email}%"
    query = """
        SELECT first_name, last_name, phone_number
        FROM applicant
        WHERE email LIKE (%(email)s);"""
    value_email = {'email': email}
    cursor.execute(query, value_email)
    return cursor.fetchall()


@database_common.connection_handler
def get_applicants(cursor: RealDictCursor) -> list:
    query = """
        SELECT first_name, last_name, phone_number, email, application_code
        FROM applicant"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def update_phone_number(cursor: RealDictCursor, phone_number: str, application_code: str) -> list:
    cursor.execute("""UPDATE applicant SET phone_number = %s  WHERE application_code = %s""",
                   (phone_number, application_code))


@database_common.connection_handler
def adding_new_applicant(cursor, first_name, last_name, phone_number, email, application_code) -> list:
    query = f"""
            INSERT INTO applicant (first_name, last_name, phone_number, email, application_code)
            VALUES('{first_name}', '{last_name}', '{phone_number}', '{email}', '{application_code}');
            """
    cursor.execute(query)
