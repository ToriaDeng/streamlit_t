from unicodedata import name
import streamlit as st
import pandas as pd 
from xt_todolist_attached import * 
import streamlit.components.v1 as stc
import streamlit as st
import smtplib as s 




# Data Viz Pkgs
import plotly.express as px 


menu = ["Add Employee Info","Update Info","Delete Info","Send Email"]
choice = st.sidebar.selectbox("Selected Activity",menu)

create_table()
if choice == "Add Employee Info":
	st.subheader("Add Employee Info")
	col1,col2 = st.columns(2)
	
	with col1:
		Name = st.text_input("Name")
		Email = st.text_input('Email Address')

	with col2:
		Position = st.selectbox("Position Level",["Senior","Midedle","Junior"])
		Entry_date = st.date_input("Date of Entry")

	if st.button("Add Employee"):
		add_data(Name,Position,Email,Entry_date)
		st.success("Added ::{} ::To List".format(Name))


	with st.expander("View Employee Table"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result,columns=['Employee_Name','Position','Email_Address','Entry_date'])
		st.dataframe(clean_df)

	with st.expander("Position Chart"):
		position_df = clean_df['Position'].value_counts().to_frame()
		# st.dataframe(task_df)
		position_df= position_df.reset_index()
		st.dataframe(position_df)

		p1 = px.pie(position_df,names='index',values='Position')
		st.plotly_chart(p1,use_container_width=True)

elif choice == "Update Info":
	st.subheader("Edit Items")

	with st.expander("Current Data"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result,columns=['Employee_Name','Position','Email_Address','Entry_date'])
		st.dataframe(clean_df)

	list_of_employee = [i[0] for i in view_all_employee_info()]
	selected_name = st.selectbox("Select Employee",list_of_employee)
	name_result = get_name(selected_name)
	# st.write(task_result)

	if name_result:
		Name = name_result[0][0]
		Position = name_result[0][1]
		Email = name_result[0][2]
		Entry_date = name_result[0][3]


		col1,col2 = st.columns(2)
		
		with col1:
			new_name = st.text_input("Edit Name")
			new_email = st.text_input('Edit Email')

		with col2:
			new_position_status = st.selectbox(Position,["Senior","Middle","Junior"])
			new_entry_date = st.date_input(Entry_date)

		if st.button("Update Employee Info"):
			edit_info_data(new_name,new_position_status,new_email,new_entry_date,Name,Position,Email,Entry_date)
			st.success("Updated ::{}'s info".format(Name))

		with st.expander("View Updated Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=['Employee_Name','Position','Email_Address','Entry_date'])
			st.dataframe(clean_df)


elif choice == "Delete Info" :
		st.subheader("Delete")
		with st.expander("View Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=['Employee_Name','Position','Email_Address','Entry_date'])
			st.dataframe(clean_df)

		employee_list = [i[0] for i in view_all_employee_info()]
		delete_employee_name =  st.selectbox("Select Employee",employee_list)
		if st.button("Delete"):
			delete_data(delete_employee_name)
			st.warning("Deleted: '{}'".format(delete_employee_name))

		with st.expander("Updated Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=['Employee_Name','Position','Email_Address','Entry_date'])
			st.dataframe(clean_df)


elif choice == "Send Email":
		st.subheader('Email Sender Web App')
		email_sender= st.text_input('Enter User Email :')
		password=st.text_input ('Enter User Password : ', type='password')
		group=['Send to Employee','Send by Job Title']
		group_reviever = st.selectbox('Where to send :',group )
		

		if group_reviever == 'Send to Employee':
			list_of_employee = [i[0] for i in view_all_employee_info()]
			selected_name = st.selectbox("Select Employee",list_of_employee)
			name_result = get_name(selected_name)
			if name_result:
				email_reciever = name_result[0][2]
				st.write(selected_name,email_reciever)

		elif group_reviever == 'Send by Job Title':
				title_send = st.selectbox("Selected Job Title",["Senior","Middle","Junior"])
				if title_send=='Senior':
					email_reciever_list = [i[2] for i in view_s_position()]
					st.write(email_reciever_list)
					email_reciever =(email_reciever_list)

				elif title_send=='Middle':
					email_reciever_list = [i[2] for i in view_m_position()]
					st.write(email_reciever_list)
					email_reciever =(email_reciever_list)

				else: 
					title_send=='Junior'
					email_reciever_list = [i[2] for i in view_j_position()]
					st.write(email_reciever_list)
					email_reciever =(email_reciever_list)
					

		subject = st.text_input('Your Email Subject :')
		body = st.text_area('Your Email')
					
		if st.button('Send Email'):
			if email_sender=='':
				st.error('Please Fill User Email Field')

			elif password=='':
				st.error ('Please Fill User Password Filed')

			elif email_reciever == '':
				st.error('Please Fill Reciecer Email Filed')
				
			try:
				connection = s.SMTP('smtp.gmail.com', 587)
				connection.starttls()
				connection.login(email_sender,password)
				message = 'Subject:{}\n\n{}'.format(subject,body)
				connection.sendmail(email_sender,email_reciever,message)
				st.success('Email Send Successfully.')

			
			except Exception as e:
				st.error('Please connect your Internet or check your email and password!')
				
			finally:
				connection.quit()



