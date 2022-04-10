import sys
import json
import moni
import mysql.connector
from datetime import date

connectiondb = mysql.connector.connect(host="host", user="user",
                                       password="password", database="database", port=3306)
cursordb = connectiondb.cursor()
print(connectiondb)

json_object = json.loads(sys.argv[1])

e_id = json_object["e_id"]
o_id = json_object["o_id"]

for w, t in moni.show_activity():
    today = date.today()
    sql = "INSERT INTO MonitoringDetails (md_title, md_total_time_seconds, md_date, e_id_id, o_id_id) VALUES (%s, %s, %s, %s, %s)" 
    val = (w,t, today, e_id, o_id)
    cursordb.execute(sql, val)
    connectiondb.commit()
    print(cursordb.rowcount, "record inserted.")

