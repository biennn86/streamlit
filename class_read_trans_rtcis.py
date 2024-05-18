import pandas as pd
import csv
import re
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from control.datatrans import DataTrans

class DataProcessor:
	def __init__(self, path_excel, sheet_name):
		self.path_excel = path_excel
		self.sheet_name = sheet_name
		self.set_static_var()
		self.data_trans = DataTrans()
		self.set_row_data = set()

	def get_data_from_dataframe(self):
		try:
			self.df = pd.read_excel(self.path_excel, self.sheet_name)
		except FileNotFoundError:
			print("File not found. Please provide a valid Excel file.")

		for column in self.df.columns:
			self.COLLUMN_NO += 1
			for i in range(len(self.df[column])-1):
				self.row_data_getform_df = self.df.iloc[i, self.COLLUMN_NO]

				if str(self.row_data_getform_df) == self.ROW_NULL:
					break

				try:
					check_row_get_match = re.match(self.pattern_getrow, self.row_data_getform_df)
				except:
					pass
					# print("-------------------------------------------------------------------------------------------------")
					# print("Data row i: {} , số dòng bị lỗi Match {}, cột: {}: {}".format(i, self.biendem, self.ROW_NULL, self.row_data_getform_df))
					# self.biendem += 1

				if check_row_get_match:
					self.data_row_not_user = check_row_get_match.group()
					self.data_row_user = self.df.iloc[i + 1, self.COLLUMN_NO]
					#Clear row
					self.string_row_cleared = self.get_row_from_data(self.data_row_not_user)
					if self.string_row_cleared is not None:
					# Get T#
						self.user_final = self.get_user_form_data(self.data_row_user)
					# Input results to list
						data_row_final = self.string_row_cleared + ";" + self.user_final + "\n"
						self.set_row_data.add(data_row_final)
						# self.lst_results.append(data_row_final)
						#create dict data
						# dict_data = {}
						# data_row_insert = data_row_final.rstrip().split(";")
						# for i in range(len(self.lst_columns_datatrans)):
						# 	dict_data.setdefault(self.lst_columns_datatrans[i], data_row_insert[i])
						# if dict_data is not None:
						# 	self.data_trans.insert(dict_data)
						
						self.string_row_cleared = None
						data_row_final = None
					else:
						pass
						# print("-" * 150)
						# print("Lỗi:, Data trả về None: {}".format(self.data_row_not_user))
				else:
					pass
					# print("-" * 180)
					# print("No: {}, Data không Match: {}".format(self.biendem, self.row_data_getform_df))
					# self.biendem += 1
		self.lst_results = list(self.set_row_data)
		return self.lst_results


	def get_row_from_data(self, row_data):
		try:
			index_cut = self.get_index_vn07(row_data)[1]
			left_row = row_data[:index_cut]
			right_row = row_data[index_cut:]

			left_row_fianl = self.process_left_row(left_row)
			category = left_row_fianl.split(";")[4]
			right_row_fianl = self.process_right_row(right_row, category)

			row_data_cleared = left_row_fianl + ";" + right_row_fianl
			
			if len(row_data_cleared.split(";")) == 11:
				return row_data_cleared
			else:
				return None
		except Exception:
			# print("Lỗi except hàm get_row: {}".format(row_data))
			return None

	def process_left_row(self, left_row):
		try:
			left_row_clear = self.clear_one_space(left_row, ";")
			left_row_final = left_row_clear[0]

			return left_row_final
		except:
			return ""
		
	def process_right_row(self, right_row, category):
		pattern_check_location = r'^\s*[A-Z]{1}[A-Z0-9/#\\]{1,7}$'
		pattern_check_digit = r'[0-9-.]{1,}'
		FG_CATEROGY = "F"
		PM_CATEGORY = "P"
		global number_row_error
		try:
			right_row_clear = self.clear_tow_space(right_row, ";")
			right_row_clear = self.clear_one_space(right_row_clear[0], "")
			lst_right_row = right_row_clear[0].split(";")
			lst_row_right_clear_none = [x  for x in lst_right_row if len(x) > 0]
			#Check right row
			len_list = len(lst_row_right_clear_none)
			if len_list == 1:
				check_loc = re.match(pattern_check_location, lst_row_right_clear_none[0])
				if check_loc and category == FG_CATEROGY:
					lst_row_right_clear_none.append('9999')
					lst_row_right_clear_none.append('CS')
				elif check_loc and category == PM_CATEGORY:
					lst_row_right_clear_none.append('9999')
					lst_row_right_clear_none.append('EA')
			elif len_list == 2:
				check_digit = re.match(pattern_check_digit, lst_row_right_clear_none[1])
				if check_digit:
					lst_row_right_clear_none.append('EA')
				else:
					lst_row_right_clear_none.insert(-1, '8888')
			elif len_list == 0 or len_list > 3:
				return ""

			left_row_final = ";".join(lst_row_right_clear_none)

			return left_row_final
		except:
			return ""

	def get_user_form_data(self, row_data_user):
		pattern_check_user = r'^[A-Z]{2,4}[0-9]{2,5}$'
		pattern_get_user = r'(?<=(Tech=))[A-Z0-9]{4,8}'
		NOT_FIND_USER = "UNKNOWN"
		try:
			match_user = re.search(pattern_get_user, row_data_user)
			if match_user:
				user = match_user.group()
			else:
				user = NOT_FIND_USER
				# print("."*150)
				# print("Row Number: {}, Data User Error: {}".format(i, row_data_user))
				# print("Row Number: {}, Data User Error: {}".format(i, data_row_not_user))
				# number_row_error += 1
			#check user sau khi clear
			check_user = re.match(pattern_check_user, user)
			if check_user:
				user_final = user
			else:
				user_final = NOT_FIND_USER

			return user_final
		except:
			# print("Row Number: {}, Data User Error: {}".format(number_row_error, row_data_user))
			# number_row_error += 1
			return NOT_FIND_USER

	def clear_one_space(self, string_need_clear, string_replace):
		# Hàm subn trả về 1 tuple bao gồm string sau khi thay thế và số lượng vị trí đã thay
		# Nếu không tìm thấy sẽ trả về là chuỗi ban đầu và số lần thay thế là 0
		pattern_cut_onespace = r'(\s{1,})'
		try:
			string_clear_is_tuple = re.subn(pattern_cut_onespace, string_replace, string_need_clear)
			return string_clear_is_tuple
		except Exception:
			return (string_need_clear, 0)
	
	def clear_tow_space(self, string_need_clear, string_replace):
		# Hàm subn trả về 1 tuple bao gồm string sau khi thay thế và số lượng vị trí đã thay
		# Nếu không tìm thấy sẽ trả về là chuỗi ban đầu và số lần thay thế là 0
		pattern_cut_towspace = r'(\s{2,})'
		try:
			string_clear_is_tuple = re.subn(pattern_cut_towspace, string_replace, string_need_clear)
			return string_clear_is_tuple
		except Exception:
			return (string_need_clear, 0)

	def get_index_vn07(self, data_row):
		pattern_get_vn07 = r'(\bVN07\b)'
		try:
			# phương thức span của re.search trả về tuple
			self.index_vn07_is_tuple = re.search(pattern_get_vn07, data_row).span()
			if self.index_vn07_is_tuple:
				return self.index_vn07_is_tuple
			else:
				return (0, 0)
		except:
			return (0, 0)
		
	def create_df_from_list(self, list_results):
		title_df = ['date', 'time', 'activity', 'ulid', 'category', 'item', 'batch', 'plan', 'location', 'qty', 'unit', 'user']
		self.df_tonghopdata = pd.DataFrame(columns = title_df)
		df_list = []
		for data in list_results:
			data = data.split(";")
			data[-1] = data[-1].rstrip()
			data_tuple = tuple(data)
			series_data = pd.Series(data_tuple, index=title_df)
			df_list.append(series_data)

		self.df_tonghopdata = pd.concat(df_list, axis=1).T.reset_index(drop=True)
		self.df_tonghopdata['batch'] = "'" + self.df_tonghopdata['batch']

		self.data_trans.insert_data_from_df(self.df_tonghopdata)
		df = self.data_trans.get_df_from_db()
		print(df)
		return self.df_tonghopdata
	
	def write_data_to_csv(self):
		try:
			self.df_tonghopdata.to_csv('data_trans_tonghop.csv', index=False, quoting=csv.QUOTE_ALL)
			print('Ghi data ra csv thành công')
		except AttributeError:
			print("DataFrame is not defined. Please read data from Excel first.")

	def write_data_to_txt(self):
		try:
			with open ('cls_data_tonghop_rtcis.txt', 'w') as file:
				file.writelines(self.lst_results)
				print("Đã hoàn thành ghi data ra file.")
		except FileNotFoundError:
			print("File not found. Please provide a valid TXT file.")

	def time_loading(self, start, end):
		time_difference = end - start
		total_seconds = time_difference.total_seconds()
		minutes  = int(total_seconds // 60)
		seconds = round(int(total_seconds % 60),0)
		time_load = str(f'{minutes:02d}') + ":" + str(f'{seconds:02d}')
		return time_load

	def set_static_var(self):
		self.COLLUMN_NO = -1
		self.ROW_NULL = "nan"
		self.lst_results = []
		self.biendem = 1
		self.pattern_getrow = r'^(\w*|\s*)(([0-9]{2}\/){2}[0-9]{2}[\s][0-9:]+[\s][A-Z]+[^\S][0-9]+[-0-9]{2}[\s]+(F|P)[\s][0-9]+[\s][0-9A-Z]+[\s]*VN07[\s]+([0-9A-Z\s/#\\]){2,8}[\s]+[0-9-.]*[\s]*(EA|CS|NA|N\/A|#NA|#N\/A)?)'
		self.lst_columns_datatrans = ['day', 'hour', 'activity', 'ulid', 'category', 'item', 'batch', 'plan', 'location', 'qty', 'unit', 'user']
		#Hàng mẫu: 03/02/24 07:28:41 DEPSUL 0010009772008339531-4  F 80772439 40610395P9    VN07     FF18A         32     CS
		#old: r'\W?\d{2}\/\d{2}\/\d{2}\s+\d+:\d+:\d+\s+[A-Z]+\s+\d+-\d{1}'
		#new_v1: r'\W?\d{2}\/\d{2}\/\d{2}\s+\d+:\d+:\d+\s+[A-Z]+\s+\d+-\d{1}\s+(F|P)\s+\d+\s+\d+\w+\s+(VN07)'
		#new_v2: r'^(\w*|\s*)(([0-9]{2}\/){2}[0-9]{2}[\s][0-9:]+[\s][A-Z]+[^\S][0-9]+[-0-9]{2}[\s]+(F|P)[\s][0-9]+[\s][0-9A-Z]+[\s]*VN07[\s]+([0-9A-Z\s/#\\]){2,8}[\s]+[0-9-.]*[\s]*(EA|CS|NA|N\/A|#NA|#N\/A)?)'


class DataAnalyzer:
	def __init__(self, link_openfile):
		self.link_openfile = link_openfile

	def read_csv_to_dataframe(self):
		self.df = pd.read_csv(self.link_openfile)
		self.df.columns = [re.sub("[ -]", "_", string).lower().strip() for string in self.df.columns]
		return self.df
	def read_excel_to_dataframe(self, sheet_name):
		self.df = pd.read_excel(self.link_openfile, sheet_name)
		self.df.columns = [re.sub("[ -]", "_", string).lower().strip() for string in self.df.columns]
		return self.df
	
	def left_join_df(self, df1, df2, column_df1, column_df2, method_join):
		self.df = pd.merge(df1, df2, left_on = column_df1, right_on = column_df2, how = method_join, suffixes = ('_item', '_loc'))
		return self.df
	
	def time_loading(self, start, end):
		time_difference = end - start
		total_seconds = time_difference.total_seconds()
		minutes  = int(total_seconds // 60)
		seconds = round(int(total_seconds % 60),0)
		time_load = str(f'{minutes:02d}') + ":" + str(f'{seconds:02d}')
		return time_load

class DataframeIterator:
	def __init__(self, df):
		self.df = df
		self.data_by_row = []
	
	def interate(self):
		for index, row in self.df.iterrows():
			row_data = []
			for column in self.df.columns:
				row_data.append(row[column])
			self.data_by_row.append(row_data)
			
	def get_row(self, index):
		return self.data_by_row[index]

def test_df_inter():
	path_open_csv = "D:/DATA/P&G/my_project/file_source/data_trans_tonghop.csv"
	sheet_name = "data_trans_tonghop"
	data_analyzer = DataAnalyzer(path_open_csv)
	df = data_analyzer.read_csv_to_dataframe()
	df = df.drop_duplicates()

	df_iterator  = DataframeIterator(df)
	df_iterator.interate()
	row_2_data = df_iterator.get_row(2)
	print("Dữ liệu của hàng thứ 2:", row_2_data)

# test_df_inter()

class Productivity(DataAnalyzer):
	def __init__(self, link_openfile, link_openfile_excel = None):
		super().__init__(link_openfile)
		self.link_openfile_excel = link_openfile_excel
		self.init_list_var()

		
	def init_df_data_csv(self):
		self.data = DataAnalyzer(self.link_openfile)
		self.df_data_csv = self.data.read_csv_to_dataframe()
		self.df_data_final = self.add_column_process(self.df_data_csv)

		return self.df_data_final
	
	def add_column_process(self, df_data_csv):
		#Hàm nhận vào là một dataframe đọc từ csv
		#1. Chuyển cột date, time qua định dạng datetime, và cột batch sang str
		self.df_data_csv['date'] = pd.to_datetime(self.df_data_csv['date'])
		self.df_data_csv['time'] = pd.to_datetime(self.df_data_csv['time'])
		self.df_data_csv['batch'] = self.df_data_csv['batch'].astype(str)
		#2. Remove những dòng duplicate
		self.df_data_csv = self.df_data_csv.drop_duplicates()
		#3. Filler những dòng có giá trị cột type là DEPSUL, và tạo một bản sao df tách biệt với bản đọc từ csv
		self.df_data_drap = self.df_data_csv[self.df_data_csv['type'] == 'DEPSUL'].copy()
		#4. Tạo cột mới chuyển những dòng có giờ trong cột time >=0 and < 6 trừ lùi 1 ngày, vì đó là ngày làm việc của ca 3
		self.df_data_drap['date_shift'] = self.df_data_drap.apply(lambda row: (row['date'] - pd.Timedelta(days=1))  
															  if 0 <= row['time'].hour < 6 else row['date'], axis=1)
		#5. Moving cột date_shift vừa tạo về cạnh cột date
		self.df_data_drap.insert(1, 'date_shift', self.df_data_drap.pop('date_shift'))
		#6. add column shift làm việc
		#6.1 sort cột date_shift và user từ nhỏ đến lớn
		self.df_data_drap = self.df_data_drap.sort_values(by=['date_shift', 'user', 'time'], ascending=[True, True, True])
		#6.2 Thêm cột time_in, time_out làm cơ sở tính ca làm việc
		# self.df_data_drap['time_in'] = self.df_data_drap.groupby(['date_shift', 'user'])['time'].transform('min')
		# self.df_data_drap['time_out'] = self.df_data_drap.groupby(['date_shift', 'user'])['time'].transform('max')
		def get_top(series):
			time_in = series.iloc[0].hour
			time_reference = series.iloc[0]
			#Lấy giờ của ca 3
			if time_in in [17, 18, 19, 20, 21, 22, 23]:
				if series.max() > time_reference:
					return time_reference
				return series.max()
			return series.min()
    				
		def get_bottom(series):
			time_out = series.iloc[-1].hour
			time_reference = series.iloc[-1]
			#Lấy giờ của ca 3
			if time_out in [3, 4, 5, 6]:
				if series.min() < time_reference:
					return time_reference
				return series.min()
			return series.max()
		
		def get_shift(series):
			try:
				# Series trả về tuple bao gồm các cột trong hàm groupby
				t_in = series.name[2].hour
				t_out = series.name[3].hour
				if 5 <= t_in <= 10 and 10 < t_out <= 14:
					return 'shift_1'
				elif 13 <= t_in <= 15 and 18 < t_out <= 22:
					return 'shift_2'
				elif ((21 <= t_in <= 23) or 0 <= t_in < 2) and 2 < t_out <= 6:
					return 'shift_3'
				elif 5 <= t_in <= 7 and 15 < t_out <= 18:
					return 'shift_1.12'
				elif 5 <= t_in <= 7 and 19 < t_out <= 22:
					return 'shift_1.16'
				elif 17 <= t_in <= 23 and 1 < t_out <= 6:
					return 'shift_2.12'
				elif 13 <= t_in <= 21 and 1 < t_out <= 6:
					return 'shift_2.16'
				elif 7 <= t_in <= 9 and 11 < t_out <= 16:
					return 'shift_hc1'
				elif 8 <= t_in <= 10 and 11 < t_out <= 17:
					return 'shift_hc2'
				elif 9 <= t_in <= 13 and 13 < t_out <= 18:
					return 'shift_mid'
				return 'unknown'
				# print("Time in: {}, Time out: {}".format(t_in, t_out))
			except:
				return 'error'
		
		self.df_data_drap['time_in'] = self.df_data_drap.groupby(['date_shift', 'user'])['time'].transform(get_top)
		self.df_data_drap['time_out'] = self.df_data_drap.groupby(['date_shift', 'user'])['time'].transform(get_bottom)
		self.df_data_drap['shift'] = self.df_data_drap.groupby(['date_shift', 'user', 'time_in', 'time_out'])['time_in'].transform(get_shift)
		#7. Tính số giờ làm việc trong ca dựa vào time_in và time_out
		def get_hour_work(series):
			try:
				hour_in = series.name[2]
				hour_out = series.name[3]
				day_references = (hour_out - hour_in).days
				if day_references == -1:
					diff = timedelta(hours=24) + (hour_out - hour_in)
				else:
					diff = hour_out - hour_in
				total_seconds = abs(diff.total_seconds())
				total_hours = round(total_seconds / 3600, 2)
				if total_hours <= 1:
					return 100
				return total_hours
			except:
				return None

		self.df_data_drap['work_hours'] = self.df_data_drap.groupby(['date_shift', 'user', 'time_in', 'time_out'])['time_in'].transform(get_hour_work)
		#8 Đếm số giao dịch thực hiện trong ngày
		self.df_data_drap['number_trans'] = self.df_data_drap.groupby(['date_shift', 'user'])['location'].transform('count')
		#9 Khoảng thời gian lệch nhau giữa 2 giao dịch
		self.df_data_drap['diff_time_trans'] = self.df_data_drap['time'].diff().dt.total_seconds()
		def corver_hour_minute_seconds(total_seconds):
			if total_seconds > 0:
				total_seconds = int(total_seconds)
				minutes, seconds = divmod(total_seconds, 60)
				hours, minutes = divmod(minutes, 60)
				time_string = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
				return time_string
			else:
				return None
		self.df_data_drap['diff_time_trans'] = self.df_data_drap['diff_time_trans'].apply(corver_hour_minute_seconds)
		#10 Tính prd một giờ làm được bao nhiêu pallet
		def get_prd(series):
			qty_trans = series.name[0]; work_hours = series.name[1]
			if qty_trans > 0 and work_hours > 0:
				prd = round(qty_trans / work_hours,2)
				return prd
			return None
		self.df_data_drap['prd_h'] = self.df_data_drap.groupby(['number_trans', 'work_hours'])['work_hours'].transform(get_prd)

		# print(self.df_data_drap.iloc[850:900, :])
		# print(self.df_data_drap)
		# self.df_data_drap.to_csv('time_in_out.csv', index = False,encoding='utf-8-sig')
		return self.df_data_drap
	
	def init_df_loc_user(self):
		self.df_loc = DataAnalyzer(self.link_openfile_excel).read_excel_to_dataframe(self.sheet_name_loc)
		self.df_user = DataAnalyzer(self.link_openfile_excel).read_excel_to_dataframe(self.sheet_name_user)
		self.df_user = self.df_user[['user', 'group', 'name']]
		self.df_loc = self.df_loc.drop_duplicates()
		self.df_user = self.df_user.drop_duplicates()
		return self.df_loc, self.df_user
	
	def init_data_final(self):
		self.df_data_final = self.init_df_data_csv()
		self.df_loc, self.df_user = self.init_df_loc_user()
		self.df_data_loc = self.data.left_join_df(self.df_data_final, self.df_loc, 'location', 'location', 'left')
		self.df_data_loc_user = self.data.left_join_df(self.df_data_loc, self.df_user, 'user', 'user', 'left')
		return self.df_data_loc_user
	
	def init_list_var(self):
		# column insert to df
		self.columns_need_add = ['receive_wh_b', 'receive_234', 'put_pm_wh1', 'put_pm_wh2', 
						 'put_pm_wh3', 'put_marking', 'put_fg', 'lta', 'fill', 'scaner', 
						 'move_stock', 'cap_pm', 'cap_marking', 'move_fg_to_wh3','move_pm_to_wh2', 'move_pm_to_wh3', 'other']
		# add column summary total
		self.columns_total = self.columns_need_add.copy()
		self.columns_total.append('total_trans')
		# init dict for function groupby.agg
		self.agg_columns = {f'{col}': (col, 'sum') for col in self.columns_total}
		# arguments need function process_row
		self.column_need = ['type_item', 'category_item', 'type_loc', 'category_loc', 'level', 'wh']
		#lst columns report
		self.lst_columns_report = ['date_shift', 'time_in', 'time_out', 'work_hours', 'shift', 'user', 'group', 'name', 'number_trans', 'prd_h']
		# sheetname create df loc, user
		self.sheet_name_loc = "location"
		self.sheet_name_user  = "masteruser"
		# Variable used for productivity statistics
		self.RECEIVE = 'Receive'; self.PUTAWAY = 'Putaway'; self.FINISHGOODS = 'F'; self.RAWMATERIAL = 'P'
		self.WH1 = 'WH1'; self.WH2 = 'WH2'; self.WH3 = 'WH3'; self.MARKING = 'Marking'
		self.HIGHTRACK = 'HR'; self.LEVEL_A = 'PF'; self.LTA = 'LTA'; self.PICK = 'Pick'; self.SCANOUT = 'ScanOut'
		self.SHIPOUT = 'ShipOut'; self.LSL_PM = 'LSLPM'; self.LSL_MK = 'LSLRM'; self.FLOOR = 'Floor';
		self.LABLE = 'LABLE'; self.TYPE_STJP = 'Retail_Returns'

	def process_row(self, row, type_item, category_item, type_loc, category_loc, level, wh, i):
		type_item = row[type_item]
		category_item = row[category_item]
		type_loc = row[type_loc]
		category_loc = row[category_loc]
		level = row[level]
		wh = row[wh]
		#get index row and column
		index_of_row  = row.name
		column_name_of_row = row.index
		i += 1
		dict_lambda = {
			1: category_loc == self.RECEIVE and wh == self.WH1,
			2: category_loc == self.RECEIVE and wh == self.WH2,
			3: category_loc == self.PUTAWAY and category_item == self.RAWMATERIAL and wh == self.WH1,
			4: category_loc == self.PUTAWAY and category_item == self.RAWMATERIAL and wh == self.WH2,
			5: category_loc == self.PUTAWAY and category_item == self.RAWMATERIAL and wh == self.WH3,
			6: category_loc == self.PUTAWAY and type_loc == self.MARKING and category_item == self.RAWMATERIAL,
			7: category_loc == self.PUTAWAY and level == self.HIGHTRACK and category_item == self.FINISHGOODS,
			8: category_loc == self.LTA and level == self.LEVEL_A and category_item == self.FINISHGOODS,
			9: category_loc == self.PICK and category_item == self.FINISHGOODS,
			10: category_loc == self.SCANOUT,
			11: category_loc == self.SHIPOUT,
			12: category_loc == self.LSL_PM,
			13: category_loc == self.LSL_MK,
			14: wh == self.WH3 and level == self.FLOOR and category_item == self.FINISHGOODS,
			15: wh == self.WH2 and (category_loc in [self.PICK, self.LTA]) and category_item == self.RAWMATERIAL,
			16: wh == self.WH3 and level == self.FLOOR and category_item == self.RAWMATERIAL,
			17: (wh in [self.WH2] and type_loc in [self.TYPE_STJP]) or wh == self.LABLE
		}

		if dict_lambda[i]:
			return 1
		return 0

	def process_df(self):
		self.df_data = self.init_data_final()
		# Chưa hiểu vì sao phải đặt ở đây mới chạy được, đặt ở hàm add_columns_process lại chạy ra dataframe empty
		self.df_data['time_in'] = pd.to_datetime(self.df_data['time_in']).dt.time
		self.df_data['time_out'] = pd.to_datetime(self.df_data['time_out']).dt.time
		self.df_data['time'] = pd.to_datetime(self.df_data['time']).dt.time
		# thêm và tính các cột cần tính prd vào
		for i, column in enumerate(self.columns_need_add):
			self.df_data.loc[:, column] = self.df_data.apply(lambda row: self.process_row(row, *self.column_need, i), axis=1)
		self.df_data['total_trans'] = self.df_data[self.columns_need_add].agg('sum', axis=1)
		#tổng hợp các cột vừa thêm
		df_sum = self.df_data.groupby(self.lst_columns_report).agg(**self.agg_columns).reset_index()
		#sắp xếp data từ nhỏ đến lớn
		df_sum = df_sum.sort_values(by=['date_shift', 'total_trans'], ascending=[True, False]).reset_index(drop=True)
		#ghi data ra file
		df_sum.to_csv('prd.csv', index = False, encoding='utf-8-sig')
		self.df_data.to_csv('data_merge.csv', index = False, encoding='utf-8-sig')

		return df_sum
	
	def process_detail(self):
		try:
			path_prd = "file_source/prd.csv"
			analysis = DataAnalyzer(path_prd)
		except:
			path_prd = "D:/DATA/P&G/my_project/file_source/prd.csv"
			analysis = DataAnalyzer(path_prd)

		self.df_sum = analysis.read_csv_to_dataframe()
		#1. tính sản lượng nhập theo ngày
		self.df_sum['total_receive'] = self.df_sum['receive_wh_b'] +  self.df_sum['receive_234']
		#tinh total_mhe
		self.df_sum['total_mhe'] = self.df_sum['total_trans'] - \
			self.df_sum['total_receive'] - self.df_sum['move_stock'] - self.df_sum['scaner']
		df_receive = self.df_sum.groupby(['date_shift']).agg({'total_receive': 'sum',
														'lta': 'sum',
														'scaner': 'sum',
														'total_mhe': 'sum',
														'total_trans': 'sum',
														}).reset_index()
		# df_receive = self.df_sum.groupby(['date_shift']).agg({'receive_wh_b': 'sum', 'receive_234': 'sum'}).reset_index()
		# df_receive['total_receive'] = df_receive.agg(lambda x: x['receive_wh_b'] + x['receive_234'], axis=1)
		#1.1 Tính lượng nhân sự nhập theo ngày
		manpower = self.df_sum.groupby(['date_shift', 'group'])['user'].agg('count').reset_index()
		manpower_inbound = manpower.query("group == 'Inbound'")#.reset_index(drop=True)
		manpower_outbound = manpower.query("group == 'Outbound'")
		manpower_mhe = manpower.query("group == 'MHE'")
		manpower_total = self.df_sum.groupby(['date_shift'])['user'].agg('count').reset_index()
		# manpower_inbound.drop(['group'], axis=1, inplace=True)
		#phải merge lấy date_shift làm chuẩn tránh ca df khác bị thiếu dòng
		df_receive = pd.merge(df_receive, manpower_inbound, left_on='date_shift', right_on='date_shift', how='left')
		df_receive = pd.merge(df_receive, manpower_outbound, left_on='date_shift', right_on='date_shift', how='left', suffixes = ('_in', '_out'))
		df_receive = pd.merge(df_receive, manpower_mhe, left_on='date_shift', right_on='date_shift', how='left')
		df_receive = pd.merge(df_receive, manpower_total, left_on='date_shift', right_on='date_shift', how='left', suffixes = ('_mhe', '_total'))
		#chèn 1 dòng mới vào df do ngày 24 inbound không có nhân sự
		# df_chen = pd.DataFrame({'date_shift': '2024-03-24', 'group': 'Inbound', 'user': 0}, index=[0])
		# manpower_inbound = pd.concat([manpower_inbound, df_chen], ignore_index=True)
		
		manpower_inbound = df_receive['user_in']
		manpower_outbound = df_receive['user_out']
		manpower_mhe = df_receive['user_mhe']
		manpower_total = df_receive['user_total']
		date_receive = df_receive['date_shift']
		total_receive = df_receive['total_receive']
		total_lta = df_receive['lta']
		total_out = df_receive['scaner']
		total_mhe = df_receive['total_mhe']
		total_trans = df_receive['total_trans']
		
		#2 Vẽ biểu đồ
		fig, receive_in_out = plt.subplots()
		fig.set_figure=(14, 6)
		# Đặt chiều rộng của các cột
		bar_width = 0.25
		cot1 = range(0, len(date_receive))
		cot2 = [x + bar_width for x in cot1]
		cot3 = [x + bar_width for x in cot2]

		receive_in_out.bar(cot1, height = total_receive, width=bar_width, align='center', label='Total Receive RPM')
		receive_in_out.bar(cot2, height = total_lta, width=bar_width, align='center', label='Total Receive FG')
		receive_in_out.bar(cot3, height = total_out, width=bar_width, align='center', label='Total Out')
		receive_in_out.set_title('Sản Lượng Nhập Theo Ngày', color='black')
		receive_in_out.set_xlabel('Date', color='red')
		receive_in_out.set_ylabel('Pallet', color='red')
		# Định dạng trục x để hiển thị ngày tháng
		receive_in_out.set_xticks(df_receive.index, df_receive['date_shift'], rotation=90, size=8)
		#_in_outgrid(True, color='gray')
		receive_in_out.legend()
		# receive_in_out = plt.show()

		#2.1 biểu đồ inbound
		fig, receive = plt.subplots()
		# fig.set_figure(14, 6)
		receive_man = receive.twinx()
		receive.bar(x=date_receive, height=total_receive, color='blue')
		receive_man.plot(date_receive, manpower_inbound, marker='.', color='red')
		receive.set_title('Sản Lượng Nhập Theo Ngày Team Inbound')
		receive.set_xlabel('Date')
		receive.set_ylabel('Pallet')
		receive_man.set_ylabel('Man')
		receive.set_xticks(date_receive, date_receive, rotation=90, size=8)
		receive.legend(['Sản Lượng Nhập', 'Nhân Sự Nhập'])
		# receive_man.legend(bbox_to_anchor=(0.987, 0.95))
		# receive = plt.show()

		#2.2 biểu đồ outbound
		fig, outbound = plt.subplots()
		# fig.set_figure(14, 6)
		out_man = outbound.twinx()
		outbound.bar(x=date_receive, height=total_out, label='Sản Lượng Xuất', color='coral')
		out_man.plot(date_receive, manpower_outbound, label='Nhân Sự Xuất', marker='.', color='red')
		outbound.set_title('Sản Lượng Xuất Theo Ngày Team Outbound')
		outbound.set_xlabel('Date')
		outbound.set_ylabel('Pallet')
		out_man.set_ylabel('Man')
		outbound.set_xticks(date_receive, date_receive, rotation=90, size=8)
		outbound.legend()
		out_man.legend(bbox_to_anchor=(0.987, 0.95))
		# outbound = plt.show()
		#2.3 biểu đồ mhe
		fig, mhe = plt.subplots()
		# fig.set_figure(14, 6)
		mhe_man = mhe.twinx()
		mhe.bar(x=date_receive, height=total_mhe, label='Total Pallet In/Out', color='aqua')
		mhe_man.plot(date_receive, manpower_mhe, label='Nhân Sự MHE', marker='.', color='red')
		mhe.set_title('Sản Lượng Xuất Theo Ngày Team MHE')
		mhe.set_xlabel('Date')
		mhe.set_ylabel('Pallet')
		mhe_man.set_ylabel('Man')
		mhe.set_xticks(date_receive, date_receive, rotation=90, size=8)
		mhe.legend()
		mhe_man.legend(bbox_to_anchor=(0.987, 0.95))
		# outbound = plt.show()

		#2.4 total sản lượng total manpower
		fig, total = plt.subplots()
		# fig.set_figure(14, 6)
		man_total = total.twinx()
		total.bar(x=date_receive, height=total_trans, color='olivedrab')
		man_total.plot(date_receive, manpower_total, marker='.', color='red')
		total.set_title('Sản Lượng Xuất Theo Ngày Toàn Team')
		total.set_xlabel('Date')
		total.set_ylabel('Pallet')
		man_total.set_ylabel('Man')
		total.set_xticks(date_receive, date_receive, rotation=90, size=8)
		total.legend(['Total Pallet', 'Total Nhân Sự'])
		# man_total.legend(bbox_to_anchor=(0.987, 0.95))
		# total = plt.show()

		return self.df_sum

def test_prd():
	starttime = datetime.now()
	
	path_open_csv = "D:/DATA/P&G/my_project/file_source/data_trans_tonghop.csv"
	path_open_loc_user = "D:/DATA/P&G/my_project/file_source//loc_user.xlsx"

	# d = Productivity(path_open_csv).init_df_data_csv()
	t = Productivity(path_open_csv, path_open_loc_user)
	# t.init_data_final()
	# t.process_df()
	t.process_detail()
	

	endtime = datetime.now()
	time_diference = t.time_loading(starttime, endtime)
	print("Đã chạy xong, thời gian chạy: {}".format(time_diference))

# test_prd()

def main_cls_read_data_from_excel():

	path = 'D:/DATA/P&G/my_project/file_source/get_transaction_rtcis_070424 GuiMinh.xlsm'
	name_sh = 'DataFormRTCIS'
	# path = 'D:/DATA/P&G/my_project/file_source/data_rtcis_test.xlsx'
	# name_sh = 'Sheet1'
	data = DataProcessor(path, name_sh)
	result = data.get_data_from_dataframe()
	print("Tổng Dòng Tổng Hợp Được: {}".format(len(result)))
	starttime = datetime.now()
	data.write_data_to_txt()

	df_tonghop = data.create_df_from_list(result)
	data.write_data_to_csv()
	# print(df_tonghop.head(20))
	
	endtime = datetime.now()
	time_diference = data.time_loading(starttime, endtime)
	print("Đã chạy xong, thời gian chạy: {}".format(time_diference))

	#------------------------------------------------------------------------------
	

main_cls_read_data_from_excel()

