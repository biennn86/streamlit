# import matplotlib.pyplot as plt


# # Tạo dữ liệu mẫu
# x = [1, 2, 3, 4, 5]
# y = [10, 20, 15, 25, 30]

# # Vẽ biểu đồ
# plt.plot(x, y)

# # Đặt số lượng điểm chia và nhãn cho trục x
# plt.xticks(range(1, 6), ['Label 1', 'Label 2', 'Label 3', 'Label 4', 'Label 5'])

# # Hiển thị biểu đồ
# plt.show()

from database.conect_db import ConnectDB

t = ConnectDB().getConection()