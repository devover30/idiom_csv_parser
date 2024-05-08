import csv
import psycopg
import math
import os
import base64

def secure_random_alphanumeric(str_len: int) -> str:
  ret = ''
  while len(ret) < str_len:
    rand_len = 3 * (math.ceil((str_len - len(ret)) / 3) + 2)
    ret += base64.b64encode(os.urandom(rand_len)).decode('ascii').replace('+', '').replace('/', '').replace('=', '')
  return ret[:str_len]


csvRow = []

with open('idioms.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        csvRow.append(row)

#print(len(csvRow))
#print(csvRow[198])
with psycopg.connect("dbname=idiom_v1 user=db_user port=5440 host=localhost password=User_2024") as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no SQL injections!)
        index = 0
        for row in csvRow:
            index = index + 1
            uuid = secure_random_alphanumeric(16)
            cur.execute(
                "INSERT INTO idioms_tbl (id, idiom_eng, idiom_hin, is_read) VALUES (%s, %s, %s, %s)",
                (uuid, row[1], row[2], "false"))
            print("inserted row with uuid: ", uuid, " having row no.: ", index, " with csv id: ", row[0])


        # Make the changes to the database persistent
        conn.commit()
