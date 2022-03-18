import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()


def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS t_empoyeetable(Employee_Name TEXT,Position TEXT,Email_Address TEXT,Entry_date DATE)')


def add_data(Name,Positions,Email,Entry_date):
	c.execute('INSERT INTO t_empoyeetable(Employee_Name,Position,Email_Address,Entry_date) VALUES (?,?,?,?)',(Name,Positions,Email,Entry_date))
	conn.commit()


def view_all_data():
	c.execute('SELECT * FROM  t_empoyeetable')
	data = c.fetchall()
	return data

def view_all_employee_info():
	c.execute('SELECT DISTINCT Employee_Name FROM t_empoyeetable')
	data = c.fetchall()
	return data

def get_name(name):
	c.execute('SELECT * FROM t_empoyeetable WHERE Employee_Name="{}"'.format(name))
	data = c.fetchall()
	return data


def edit_info_data(new_name,new_position_status,new_email,new_entry_date,Name,Position,Email,Entry_date):
	c.execute("UPDATE t_empoyeetable SET Employee_Name =?,Position=?,Email_Address=?,Entry_date=? WHERE Employee_Name =? and Position=?and Email_Address=? and Entry_date=? ",(new_name,new_position_status,new_email,new_entry_date,Name,Position,Email,Entry_date))
	conn.commit()
	data = c.fetchall()
	return data

def delete_data(name1):
	c.execute('DELETE FROM t_empoyeetable WHERE Employee_Name="{}"'.format(name1))
	conn.commit()


def view_s_position():
	c.execute("SELECT * FROM t_empoyeetable WHERE Position='Senior'")
	data = c.fetchall()
	return data

def view_m_position():
	c.execute("SELECT * FROM t_empoyeetable WHERE Position='Middle'")
	data = c.fetchall()
	return data

def view_j_position():
	c.execute("SELECT * FROM t_empoyeetable WHERE Position='Junior'")
	data = c.fetchall()
	return data