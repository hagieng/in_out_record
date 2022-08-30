'''
入退記録コマンド

'''

import time
from datetime import datetime,timezone,timedelta

#UNIX時間でのタイムスタンプ取得
#reader_id= 社員証を読み取るカードリーダーのID
#record_id=社員証のID（RFIDタグの識別子等）
def inout_record(reader_id,record_id):
    rec_time=int(time.time())
    record_data={"record_id":record_id,"unix_time":rec_time,"reader_id":reader_id}

    return record_data

#UNIXタイムから、表示可能なフォーマットへの変換
def inout_record_view(unix_time,time_zone):
    utc=datetime.fromtimestamp(unix_time)
    dt=utc.replace(tzinfo=timezone.utc).astimezone(tz=time_zone)
    date=dt.date()
    tzone=dt.tzinfo
    time=dt.time()
    time_view={"date":date,"time":time,"time_zone":tzone}

    return time_view