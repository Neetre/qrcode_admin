from data_manager import DataManager

datamanager = DataManager("../data/qr_codes.db")
data = datamanager.get_codes()
print(data[0])

# datamanager.cursor.execute('''UPDATE codes SET used = 0 WHERE data = ?''', (data[0][1],))
# datamanager.conn.commit()
# 
# data = datamanager.get_codes()
# print(data[0])
