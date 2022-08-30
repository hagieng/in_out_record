'''
入退記録メインファイル
'''

import inout_record as io_r
from datetime import datetime,timezone,timedelta

reader_id="reader10001" #読み取りリーダーのID
#print("社員証のIDを入力下さい")
#record_id=input()#社員のRFIDタグのID
record_id=[]
####################################################################################

import RPi.GPIO as GPIO
import MFRC522
import signal

import time
import db

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome!! Please scan your employee tag.")
print("Press Ctrl-C to stop.")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print("Card read UID: {},{},{},{}".format(uid[0], uid[1], uid[2], uid[3]))
        record_id=uid
        record_data=io_r.inout_record(reader_id,record_id)
        print(record_data)
        db.store_record(record_data)    
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
            time.sleep(1.5)
            print("waiting")
        else:
            print("Authentication error")
    


#################################################################################

"""
record_data=io_r.inout_record(reader_id,record_id)
print(record_data)
#なぜかローカル時間が取得されてしまう。　？？？？
"""

'''
#record_dataを記録する to csv file
from csv import DictWriter
# First, open the old CSV file in append mode, hence mentioned as 'a'
# Then, for the CSV file, create a file object
with open('in_out_record.csv', 'a', newline='') as f_object:
    # Pass the CSV  file object to the Dictwriter() function
    # Result - a DictWriter object
    headersCSV = ['record_id','unix_time','reader_id']  
    dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
    # Pass the data in the dictionary as an argument into the writerow() function
    dictwriter_object.writerow(record_data)
    # Close the file object
    f_object.close()
'''
"""
##record_dataを記録する to  DB
import db
db.store_record(record_data)

unix_time=record_data["unix_time"]
#print(unix_time)
JST=timezone(timedelta(hours=+9), 'JST')
dt=io_r.inout_record_view(unix_time,JST)
#print(dt)

lastname="hagiwara"
inout="In"
print(lastname+"さん "+str(dt["date"])+" "+str(dt["time"])+" "+str(dt["time_zone"])+" "+inout+"完了")
"""