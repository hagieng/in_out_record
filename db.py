'''
入退記録 DBアクセス関連Def

'''

from optparse import Values
import psycopg2
import psycopg2.extras


#conn = psycopg2.connect(host='192.168.8.102', dbname='inout_record', user='postgres', password='raspberry')

"""
table="reader_id"
inout="in"
def select(table):
    sql="select * from "+table+" where in_out='"+inout+"'"
    print(sql)
    cur=conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    print(rows)
    conn.close()
"""
def store_record(val={}):
    conn = psycopg2.connect(host='192.168.8.102', dbname='inout_record', user='postgres', password='raspberry')
 
    values="'"+str(val["record_id"])+"','"+str(val["unix_time"])+"','"+str(val["reader_id"])+"'"
    print(values)
    sql="INSERT INTO in_out_record(record_id,unix_time,reader_id) VALUES("+values+");"
    cur=conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()
    return True

def read_record(top="*"):
    conn = psycopg2.connect(host='192.168.8.102', dbname='inout_record', user='postgres', password='raspberry')
    table="in_out_record"
    #sql="select "+top+" from "+table+"ORDER BY unix_time DESC"
    sql="select "+top+" from "+table+";"
    #print(sql)
    rows={}
    cur=conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    #print(rows)
    conn.close()
    key=["record_id","unix_time","reader_id","id"]
    records=rows
    mydata = []
    for item in records:
        mydata.append(dict(zip(key,item)))
    return mydata

#入退ログ用にテーブルを結合して取得 limitは取得する直近のログの行数。1以上の整数。指定無ければALL
def get_logs_inout(limit="all"):
    conn = psycopg2.connect(host='192.168.8.102', dbname='inout_record', user='postgres', password='raspberry')
    table1="in_out_record"
    table2="reader_id"
    table3="employee_id"
    #sql="select "+top+" from "+table+"ORDER BY unix_time DESC"
    sql="SELECT * from "+table1+" LEFT JOIN "+table2+" ON "+table1+".reader_id = "+table2+".reader_id LEFT JOIN "+table3+" ON "+table1+".record_id="+table3+".rfid ORDER BY unix_time DESC LIMIT "+str(limit)+";"
    #sql="select last_name, first_name, unix_time, location, room "+top+" from "+table1+" LEFT OUTER JOIN "+table2+" LEFT OUTER JOIN "+table3+" ON table1.reader_id = table2.reader_id AND table1.record_id=table3.rfid ORDER BY unix_time DESC;"
    #print(sql)
    rows={}
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(sql)
    rows = cur.fetchall()
    #print(rows)
    dict_result = []
    for row in rows:
        dict_result.append(dict(row))
    
    conn.close()
    return dict_result
    
from datetime import datetime,timezone,timedelta

#UNIX時間でのタイムスタンプ取得
#reader_id= 社員証を読み取るカードリーダーのID
#record_id=社員証のID（RFIDタグの識別子等）
def inout_record(reader_id,record_id):
    rec_time=int(time.time())
    record_data={"record_id":record_id,"unix_time":rec_time,"reader_id":reader_id}

    return record_data

#UNIXタイムから、表示可能なフォーマットへの変換
def inout_record_view(unix_time,time_zone=timezone(timedelta(hours=+9), 'JST')):
    utc=datetime.fromtimestamp(unix_time)
    dt=utc.replace(tzinfo=timezone.utc).astimezone(tz=time_zone)
    date=dt.date()
    tzone=dt.tzinfo
    time=dt.time()
    time_view={"date":date,"time":time,"time_zone":tzone}

    return time_view

#リストに含まれるUNIX時間を変換して、リストに辞書型で日時とタイムゾーンを追加
def datetime_add(mydata=[]):
    for mydata_item in mydata:
        dt=inout_record_view(mydata_item["unix_time"])
        mydata_item["date"]=dt["date"]
        mydata_item["time"]=dt["time"]
        mydata_item["time_zone"]=dt["time_zone"]
    return mydata