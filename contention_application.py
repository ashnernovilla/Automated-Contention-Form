# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:16:58 2024

@author: I024605
"""
import time
import streamlit as st
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import hashlib
from streamlit_navigation_bar import st_navbar
import numpy as np
st.set_page_config(layout="wide")
from datetime import datetime, timedelta
from PIL import Image 
import io
import random
import base64
import win32com.client as win32
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval
from streamlit_free_text_select import st_free_text_select
import hydralit_components as hc
import plotly.graph_objects as go
import plotly
import plotly.io as pio
import kaleido
fig = go.Figure()

from incentive_test import pref_incentives_main

pd.set_option('display.max_columns', None)  


server = 'PPBWDLC0SG7A1'
database = 'db_Contention'
username = 'admin'
password = 'Openlab@123'

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(connection_string))

def sql_connection(sql_query, dbase):
    # Replace with your actual SQL Server connection details
    server = 'PPBWDLC0SG7A1'
    database = dbase
    username = 'admin'
    password = 'Openlab@123'

    # Define the connection string
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )


    try:
        # Establish the connection
        conn = pyodbc.connect(connection_string)

        # Define the SELECT query
        query = sql_query

        # Execute the query and fetch data into a DataFrame
        df = pd.read_sql(query, conn)

        # Execute Trims 

        # Print the data
        print(df)


    except pyodbc.Error as e:
        print("Error connecting to SQL Server:", e)
    finally:
        # Close the connection
        conn.close()

    return df

@st.cache_data
def incetives_test(passcode):
    bse_incetive_data, bse_incetive_info, pref_incentives_group = pref_incentives_main(passcode)
    return bse_incetive_data, bse_incetive_info, pref_incentives_group


# Security
#passlib,hashlib,bcrypt,scrypt
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

def login_user(username, password, position):
    #c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    #data = c.fetchall()
    
    if position == 'BSE Login':
        query = f''' 
                        SELECT 
                        BSE24.[BSE FULL NAME]
                        , BSE24.[SURNAME]
                        , BSE24.[BSE CODE]
    					, BSE24.BAM
    					, BSE24.[BAM CODE]
    					, BSE24.BDM
    					, BSE24.[BDM CODE]
                        , BSE24.[TSH]
                        , BSE24.[TSH CODE]
                        , BSE24.[SEGMENT]
    					, MONTH(CAST(BSE24.[WWDate] AS DATE)) AS MONTH_WWDate
                        FROM db_MasterFile_2024.dbo.tbl_BSEMasterFile_2024 AS BSE24
                        WHERE MONTH(CAST(BSE24.[WWDate] AS DATE)) = (SELECT Top 1 MAX(MONTH(CAST([WWDate] AS DATE))) AS MONTH_WWDate FROM db_MasterFile_2024.dbo.tbl_BSEMasterFile_2024 )
                        AND [SURNAME] = '{username}' AND [BSE CODE] = '{password}' 
                  '''
        
        data = sql_connection(query, 'master')
        
        return data
    
    if position == 'BAM Login':
        query = f''' 
                   SELECT 
                    BAM24.[BAM FULL NAME]
                    , BAM24.[SURNAME]
					, BAM24.[BAM CODE]
					, BAM24.BDM
					, BAM24.[BDM CODE]
					, MONTH(CAST(BAM24.[WWDate] AS DATE)) AS MONTH_WWDate
                    FROM db_MasterFile_2024.dbo.tbl_BAMMasterFile_2024 AS BAM24
                    WHERE MONTH(CAST(BAM24.[WWDate] AS DATE)) = (SELECT Top 1 MAX(MONTH(CAST([WWDate] AS DATE))) AS MONTH_WWDate FROM db_MasterFile_2024.dbo.tbl_BAMMasterFile_2024 )
                    AND [SURNAME] = '{username}' AND [BAM CODE] = '{password}'
                  '''
        
        data = sql_connection(query, 'master')
        
        return data
    
    if position == 'BDM Login':
        query = f''' 
                   SELECT 
                      BDM24.[BDM FULL NAME]
                    , BDM24.[SURNAME]
					, BDM24.[BDM CODE]
					, MONTH(CAST(BDM24.[WWDate] AS DATE)) AS MONTH_WWDate
                    FROM db_MasterFile_2024.dbo.tbl_BDMMasterFile_2024 AS BDM24
                    WHERE MONTH(CAST(BDM24.[WWDate] AS DATE)) = (SELECT Top 1 MAX(MONTH(CAST([WWDate] AS DATE))) AS MONTH_WWDate FROM db_MasterFile_2024.dbo.tbl_BDMMasterFile_2024)
                    AND [SURNAME] = '{username}' AND [BDM CODE] = '{password}'
                  '''
        
        data = sql_connection(query, 'master')
        
        return data
        
    if position == 'TSH Login':
        query = f''' 
                  	  SELECT 
                      TSH24.[SURNAME] +', '+ TSH24.[FIRST NAME] AS [TSH FULL NAME]
                    , TSH24.[SURNAME]
					, TSH24.[TSH CODE]
					, MONTH(CAST(TSH24.[WWDate] AS DATE)) AS MONTH_WWDate
                    FROM db_MasterFile_2024.dbo.tbl_TSHMasterFile_2024 AS TSH24
                    WHERE MONTH(CAST(TSH24.[WWDate] AS DATE)) = (SELECT Top 1 MAX(MONTH(CAST([WWDate] AS DATE))) AS MONTH_WWDate FROM db_MasterFile_2024.dbo.tbl_TSHMasterFile_2024)
                    AND [SURNAME] = '{username}' AND [TSH CODE] = '{password}'
                  '''
        
        data = sql_connection(query, 'master')
    
        return data

def T1_POLNUM(bsecode):
    #c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    #data = c.fetchall()
    query = f''' 
                SELECT DISTINCT(POLNUM) AS POLNUM FROM [db_MegaReportIV].[dbo].[Mega_2024] WHERE [BSE CODE] = '{bsecode}' OR [BSE CODE 2] = '{bsecode}' OR [BSE CODE 3] = '{bsecode}'
              '''
    data = sql_connection(query, 'master')
    
    return data

def email_sent(bsecode, bsename, body, sender, receiver):
    now = datetime.now().strftime("%m-%d-%Y")
    olApp = win32.Dispatch('Outlook.Application')
    olNS = olApp.GetNamespace("MAPI")
    mailItem = olApp.CreateItem(0)
    mailItem.Subject = f"Alpha Convention {now} Update"
    mailItem.BodyFormat = 1
    
   # Convert the DataFrame to an HTML table with width styling
    #html_table = body.to_html(classes='data', header=True, index=False, table_id='example', justify='center', border=0, max_rows=10, max_cols=5, col_space=25, notebook=True)
    
    # Wrap the table in a <div> with inline styling to center and adjust width
    
    
    num_rows = len(body['POLICY NUMBER'])
    
    mailItem.HTMLBody = '''
        <html>
            <head>
            
            <!-- Required meta tags -->
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">

                <!-- Bootstrap CSS -->
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

                <style>
                    table { 
                        margin-left: auto;
                        margin-right: auto;
                    }
                </style>

                <title>Email Format</title>

            </head>
        '''
    
    mailItem.HTMLBody += f'''
        <body>

            <h1 class='h1-name'> Good day, {bsename.title()}!  </h1>
            
            <p class='p1'> Please find your contention summary as of {now}. <br> </br>
                This report is system-generated and should be used for tracking purposes only. <br></br>
            </p>
            
            <p class='p1'>
                For questions and corrections, you may reach out to <a href="philippines.bplac.bas.incentive-prod@aia.com">philippines.bplac.bas.incentive-prod@aia.com</a>. 
            </p>
            
            <div> <br> </br>  </div>
            
            '''
    #mailItem.HTMLBody += f'<div style="text-align: center; max-width: 80%;">{html_table}</div>'
    
    mailItem.HTMLBody+= '''
               <h2 style="text-align:center;"> Contention Summary  </h2>
                <div class="table-responsive">
                    <table class="table">
                    <thead style = "background: #510400; color: white;">
                        <tr>
                        <th>POLICY NUMBER</th>
                        <th>TYPE OF CONTENTION</th>
                        <th>CONTENTION DETAILS</th>
                        <th>Date Submit</th>
                        <th>BAM STATUS</th>
                        <th>BAM COMMENTS</th>
                        <th>BAM APPRV DATE</th>
                        <th>BDM STATUS</th>
                        <th>BDM COMMENTS</th>
                        <th>BDM APPRV DATE</th>
                        <th>TSH STATUS</th>
                        <th>TSH COMMENTS</th>
                        <th>TSH APPRV DATE</th>
                        <th>BCA STATUS</th>
                        <th>BCA COMMENTS</th>
                        <th>BCA APPRV DATE</th>
                        <th>BAM NAME</th>
                        <th>BDM NAME</th>
                        <th>TSH NAME</th>
                        <th>CURRENT FINAL STATUS</th>
                        </tr>
                    </thead>
                    <tbody>
                    '''
    
    for i in range(num_rows):
        
        
        mailItem.HTMLBody += f'''
                    <tr>
                    <td style = "vertical-align: middle; text-align: center;" >{body.loc[i, 'POLICY NUMBER']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'TYPE OF CONTENTION']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'CONTENTION DETAILS']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'Date Submit']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'BAM Approval']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'BAM Comments']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'BAM Approved Dates']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'BDM Approval']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'BDM Comments']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'BDM Approved Dates']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'TSH Approval']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'TSH Comments']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'TSH Approved Dates']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'BCA Approval']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'BCA Comments']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'BCA Approved Dates']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'BAM']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'BDM']}</td>
                    <td style = "vertical-align: middle; text-align: center;">{body.loc[i, 'TSH']}</td>
                    <td style = "vertical-align: middle; text-align: center;">"PENDING"</td>
                    </tr>
                    '''
    
    mailItem.HTMLBody += f'''
        </tbody>
        </table>
        </div>
        
        <div> 
            <br>
            <p style = "font-size:15px;"> <b> Best Regards, </b></p>
        </div>
        </body>

    </html>
    '''
    
    mailItem.To = f"{sender};{receiver}"
    mailItem.SentOnBehalfOfName = "philippines.bplac.bas.incentive-prod@aia.com"
    #mailItem.Display()
    mailItem.Save()

def email_matching(bsecode):
    query = f'''
        WITH BSE1 AS
    		(
    			SELECT DISTINCT([BSE CODE]) AS [BSE CODE], [BSE FULL NAME], [BAM CODE], [BDM CODE], [TSH CODE], [EMAILADD] AS BSEEMAIL FROM tbl_BSEMasterFile_2024 Where [WWDate] = (SELECT MAX(CAST([WWDate] AS date)) AS [WWDate] FROM tbl_BSEMasterFile_2024)
    		),
    	BAM1 AS
    		(
    			SELECT DISTINCT([BAM CODE]) AS [BAM CODE], [BAM FULL NAME], [EMAIL ADD] FROM tbl_BAMMasterFile_2024 Where [WWDate] = (SELECT MAX(CAST([WWDate] AS date)) AS [WWDate] FROM tbl_BAMMasterFile_2024)
    		),
    	BDM1 AS
    		(
    			SELECT DISTINCT([BDM CODE]) AS [BDM CODE], [BDM FULL NAME], [EMAIL ADD] FROM tbl_BDMMasterFile_2024 Where [WWDate] = (SELECT MAX(CAST([WWDate] AS date)) AS [WWDate] FROM tbl_BDMMasterFile_2024)
    		),
    	TSH1 AS
    		(
    			SELECT DISTINCT([TSH CODE]) AS [TSH CODE], ([FIRST NAME]+[SURNAME]) AS [TSH FULL NAME], [EMAIL ADD] FROM tbl_TSHMasterFile_2024 Where [WWDate] = (SELECT MAX(CAST([WWDate] AS date)) AS [WWDate] FROM tbl_TSHMasterFile_2024)
    		),
    	COMBINEDT1 AS
    		(
    			SELECT BSE1.*, BAM1.[EMAIL ADD] AS BAMEMAIL, BAM1.[BAM FULL NAME], BDM1.[EMAIL ADD] AS BDMEMAIL, BDM1.[BDM FULL NAME], TSH1.[EMAIL ADD] AS TSHEMAIL, TSH1.[TSH FULL NAME] FROM BSE1 LEFT JOIN BAM1 ON BSE1.[BAM CODE] = BAM1.[BAM CODE]
    			LEFT JOIN BDM1 ON BSE1.[BDM CODE] = BDM1.[BDM CODE]
    			LEFT JOIN TSH1 ON BSE1.[TSH CODE] = TSH1.[TSH CODE]
    		)
    	SELECT * FROM COMBINEDT1 WHERE [BSE CODE] = '{bsecode}'
    '''
    
    df_email_addr = sql_connection(query, 'db_MasterFile_2024')
    
    return df_email_addr 
    
def add_dfForm():
    
    # uploaded_files = st.session_state.input_upload
    # df_image = pd.DataFrame({'FILE_UPLOAD': [0]})
    
    # if uploaded_files and len(uploaded_files) <= 4:

    #     combined_image = load_image(uploaded_files)
    #     #st.image(combined_image, caption='Combined Image')
    #     #st.write(', '.join([file.name for file in st.session_state.input_upload]))    

    #     combined_image_data = io.BytesIO()
    #     combined_image.save(combined_image_data, format='PNG')
    #     combined_image_data = combined_image_data.getvalue()

    #     df_image = pd.DataFrame({'FILE_UPLOAD': [combined_image_data]})
    #     # df_image.to_sql("test_export_combined_image", engine, if_exists='replace', index=False)
                                        
    #     #result_images = 1
                                        
        
    # elif uploaded_files:
    #     st.error('Please upload a maximum of 4 images.')
    
    uploaded_files = st.session_state.input_upload
    df_image = pd.DataFrame({'FILE_UPLOAD': [0]})
    
    # Check if no image is uploaded
    if not uploaded_files:
        st.warning('Please upload an image.')
        return  # Exit the function if no image is uploaded
    
    
    if len(uploaded_files) <= 4:
        combined_image = load_image(uploaded_files) 
    
        combined_image_data = io.BytesIO()
        combined_image.save(combined_image_data, format='PNG')
        combined_image_data = combined_image_data.getvalue()
    
        df_image = pd.DataFrame({'FILE_UPLOAD': [combined_image_data]})                                        

    else:
        st.error('Please upload a maximum of 4 images.')
        return  # Exit the function if more than 4 images are uploaded
                        
    
    file_names = [file.name for file in st.session_state.input_upload]
    file_names_str = ', '.join(file_names) 
    
    print("Session State After Add: ",st.session_state.input_upload)
    
    if st.session_state.input_colA is None or st.session_state.input_colB is None or st.session_state.input_colC is None:
        st.warning('Please fill in all fields (POLICY NUMBER, TYPE OF CONTENTION, CONTENTION DETAILS) before proceeding.')
        return  # Exit the function if any of the fields are empty
    
    row = pd.DataFrame({'POLICY NUMBER':[st.session_state.input_colA],
            'TYPE OF CONTENTION':[st.session_state.input_colB],
            'CONTENTION DETAILS':[st.session_state.input_colC],
            'ATTACHMENT':[file_names_str]})
    
    row['FILE_UPLOAD'] = df_image['FILE_UPLOAD']
    row['contention_key'] =  st.session_state.bsecode+datetime.now().strftime('%Y%m%d%H%M%S')
        
    st.session_state.data = pd.concat([st.session_state.data, row]).reset_index(drop=True)
    
    st.session_state.input_colA = None
    st.session_state.input_colB = None
    st.session_state.input_colC = None    


def remove_dfForm(df_edited, bsecode, bsename, bam, bamcode, bdm, bdmcode, tsh, tshcode):
    submit_data = df_edited
    submit_data['BSE NAME'] = bsename
    submit_data['BSE CODE'] = bsecode
    
    submit_data['BAM'] = bam
    submit_data['BAM CODE'] = bamcode
    submit_data['BAM Approval'] = np.where((submit_data['TYPE OF CONTENTION'].str.lower().str.contains('vpay recomputation (target for bam)'.lower())), 
                                           "NOT REQUIRED", "PENDING")
    submit_data['BAM Approved Dates'] = ''
    submit_data['BAM Comments'] = ''
    
    submit_data['BDM'] = bdm
    submit_data['BDM CODE'] = bdmcode
    submit_data['BDM Approval'] = np.where((submit_data['TYPE OF CONTENTION'].str.lower().str.contains('reinstatement (change status)'.lower())) |
                                           (submit_data['TYPE OF CONTENTION'].str.lower().str.contains('vpay recomputation (target for bse)'.lower())), 
                                           "NOT REQUIRED", "NO ACTION NEEDED YET")
    submit_data['BDM Approved Dates'] = ''
    submit_data['BDM Comments'] = ''
    
    submit_data['TSH'] = tsh
    submit_data['TSH CODE'] = tshcode
    submit_data['TSH Approval'] = np.where((submit_data['TYPE OF CONTENTION'].str.contains('Retag Branch, Area, Division, or Territory')), 
                                           "NO ACTION NEEDED YET", "NOT REQUIRED")
    submit_data['TSH Approved Dates'] = ''
    submit_data['TSH Comments'] = ''
    
    submit_data['BCA Approval'] =  "NO ACTION NEEDED YET"
    submit_data['BCA Approved Dates'] = ''
    submit_data['BCA Comments'] = ''
    
    submit_data['Date Submit'] = datetime.now().strftime('%Y-%m-%d')
    
    
    submit_data['BAS Comment'] = ''
    
    submit_data['TYPE OF CONTENTION'] = np.where(submit_data['TYPE OF CONTENTION'].isna(), '', submit_data['TYPE OF CONTENTION'])
    
    #submit_data['Status'] = 'Pending'
    submit_data.to_sql('tbl_contention_logs', engine, if_exists='append', index=False, chunksize=1000)
    
    
    #df_emaildet = email_matching(bsecode)
    
    #email_sent(password, df_emaildet.loc[0, "BSE FULL NAME"], submit_data, df_emaildet.loc[0, "BSEEMAIL"], df_emaildet.loc[0, "BAMEMAIL"])
    
    time.sleep(1)
    
    st.session_state.data = pd.DataFrame({'POLICY NUMBER':[],'TYPE OF CONTENTION':[],'CONTENTION DETAILS':[],'ATTACHMENT':[], 'FILE_UPLOAD':[]}).reset_index(drop=True)
    
    
def load_image(image_files):
    images = [Image.open(image_file) for image_file in image_files]
    
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)
    
    combined_image = Image.new('RGB', (total_width, max_height))
    
    x_offset = 0
    for img in images:
        combined_image.paste(img, (x_offset, 0))
        x_offset += img.width
    
    return combined_image


# def color_status(val):
#     colors = {
#         'PENDING': 'pink',
#         'APPROVED': 'green',
#         'NOT REQUIRED': 'gray',
#         'REJECTED':'red'
#     }
#     return f'background-color: {colors.get(val, "yellow")}'

def color_status(val):
    colors = {
        'PENDING': {'background-color': '#FFBF00', 'color': 'white'},
        'APPROVED': {'background-color': 'green', 'color': 'white'},
        'NOT REQUIRED': {'background-color': 'gray', 'color': 'white'},
        'REJECTED': {'background-color': 'red', 'color': 'white'}
    }
    style = colors.get(val, {'background-color': 'yellow', 'color': 'black'})
    return f'background-color: {style["background-color"]}; color: {style["color"]}'


def contention_history(bsecode, startdate, enddate, pol, bsetypeselection):
    query = f''' 
       SELECT  [POLICY NUMBER]
              ,[TYPE OF CONTENTION]
              ,[CONTENTION DETAILS]
              ,[Date Submit] 
              ,[BAM]
              ,[BAM Approval] AS [BAM STATUS]
              ,[BAM Comments] AS [BAM COMMENTS]
              ,[BAM Approved Dates] AS [BAM APPRV DATE]
              ,[BDM]
              ,[BDM Approval] AS [BDM STATUS]
              ,[BDM Comments] AS [BDM COMMENTS]
              ,[BDM Approved Dates] AS [BDM APPRV DATE]
              ,[TSH]
              ,[TSH Approval] AS [TSH STATUS]
              ,[TSH Comments] AS [TSH COMMENTS]
              ,[TSH Approved Dates] AS [TSH APPRV DATE]
              ,[BCA Approval] AS [BCA STATUS]
              ,[BCA Comments] AS [BCA COMMENTS]
              ,[BCA Approved Dates] AS [BCA APPRV DATE]
              ,[BAS Comment] AS [EFFECTIVE DATE OF CONTENTION]
      FROM [db_Contention].[dbo].[tbl_contention_logs]
      WHERE [BSE CODE] = {bsecode} AND ([Date Submit] BETWEEN '{startdate}' AND '{enddate}') AND [POLICY NUMBER] LIKE '{pol}%' 
      AND ([TYPE OF CONTENTION] LIKE '{bsetypeselection}%') ORDER BY [contention_key] DESC
  '''
    data = sql_connection(query, 'master')
    
    data['FINAL STATUS'] = np.where((data['BAM STATUS'] == 'PENDING') | (data['BDM STATUS'] == 'PENDING') | 
                                    (data['TSH STATUS'] == 'PENDING') | (data['BCA STATUS'] == 'PENDING'), 'PENDING', 'APPROVED')
    
    data['FINAL STATUS'] = np.where((data['BAM STATUS'] == 'REJECTED') | (data['BDM STATUS'] == 'REJECTED') | 
                                    (data['TSH STATUS'] == 'REJECTED') | (data['BCA STATUS'] == 'REJECTED'), 'REJECTED', data['FINAL STATUS'])
    
    
    return data


def contention_for_BAMApproval(bamcode):
    query = f''' 
       SELECT  [POLICY NUMBER]
              ,[TYPE OF CONTENTION]
              ,[CONTENTION DETAILS]
              ,[BAM Approval] AS [BAM STATUS]
              ,CAST([FILE_UPLOAD] AS varbinary(max)) AS [FILE_UPLOAD]
              ,[BAM Comments]
              ,[Date Submit] 
              ,contention_key
      FROM [db_Contention].[dbo].[tbl_contention_logs]
      WHERE [BAM CODE] = {bamcode} AND [BAM Approval] = 'PENDING'
  '''
    data = sql_connection(query, 'master') 
        
    return data

def Select_BAMApproved(bamcode, begdate, enddate, policy, bsename, typecontention):
    query = f''' 
       SELECT  [POLICY NUMBER]
              ,[BSE NAME]
              ,[TYPE OF CONTENTION]
              ,[CONTENTION DETAILS]
              ,[BAM Approval] AS [BAM STATUS]
              ,[BAM Comments]
              ,[BAM Approved Dates]
      FROM [db_Contention].[dbo].[tbl_contention_logs]
      WHERE [BAM CODE] = {bamcode} AND [BAM Approval] = 'APPROVED' AND ([BAM Approved Dates] BETWEEN '{begdate}' AND '{enddate}') AND [POLICY NUMBER] LIKE '{policy}%'
      AND [BSE NAME] LIKE '%{bsename}%' AND [TYPE OF CONTENTION] LIKE '{typecontention}%'
      ORDER BY [BAM Approved Dates] DESC, [contention_key] DESC
  '''
    data = sql_connection(query, 'master') 
        
    return data

def Clear_BAMFilter():
    # st.write(st.session_state['bse_date_col'])
    # st.session_state['bse_date_col'] = '', ''
    st.session_state['input_pol_col'] = ''
    st.session_state['input_bsename_col'] = ''
    st.session_state['input_contype_col'] = ''
    
def Clear_BSEFilter():
    st.session_state['input_pol_col'] = ''
    st.session_state['input_contype_col'] = ''
    st.session_state['con_status_col'] = 'PENDING|APPROVED|REJECTED'


def Select_BDMApproved(bdmcode,begdate, enddate, policy, bsename, typecontention):
    query = f''' 
       SELECT  [POLICY NUMBER]
              ,[BSE NAME]
              ,[TYPE OF CONTENTION]
              ,[CONTENTION DETAILS]
              ,[BDM Approval] AS [BDM STATUS]
              ,[BDM Comments]
              ,[BDM Approved Dates]
      FROM [db_Contention].[dbo].[tbl_contention_logs]
      WHERE [BDM CODE] = {bdmcode} AND [BDM Approval] = 'APPROVED' AND ([BDM Approved Dates] BETWEEN '{begdate}' AND '{enddate}') AND [POLICY NUMBER] LIKE '{policy}%'
      AND [BSE NAME] LIKE '%{bsename}%' AND [TYPE OF CONTENTION] LIKE '{typecontention}%'
      ORDER BY [BAM Approved Dates] DESC, [contention_key] DESC
  '''
    data = sql_connection(query, 'master') 
        
    return data

def contention_for_BDMApproval(bdmcode):
    query = f''' 
       SELECT  [POLICY NUMBER]
              ,[TYPE OF CONTENTION]
              ,[CONTENTION DETAILS]
              ,[BDM Approval] AS [BDM STATUS]
              ,CAST([FILE_UPLOAD] AS varbinary(max)) AS [FILE_UPLOAD]
              ,[BDM Comments]
              ,[Date Submit] 
              ,contention_key
      FROM [db_Contention].[dbo].[tbl_contention_logs]
      WHERE [BDM CODE] = {bdmcode} AND [BDM Approval] = 'PENDING'
  '''
    data = sql_connection(query, 'master') 
        
    return data

def Select_TSHApproved(tshcode, begdate, enddate, policy, bsename, typecontention):
    query = f''' 
       SELECT  [POLICY NUMBER]
              ,[BSE NAME]
              ,[TYPE OF CONTENTION]
              ,[CONTENTION DETAILS]
              ,[TSH Approval] AS [TSH STATUS]
              ,[TSH Comments]
              ,[TSH Approved Dates]
      FROM [db_Contention].[dbo].[tbl_contention_logs]
      WHERE [TSH CODE] = {tshcode} AND [TSH Approval] = 'APPROVED' AND ([TSH Approved Dates] BETWEEN '{begdate}' AND '{enddate}') AND [POLICY NUMBER] LIKE '{policy}%'
      AND [BSE NAME] LIKE '%{bsename}%' AND [TYPE OF CONTENTION] LIKE '{typecontention}%'
      ORDER BY [BAM Approved Dates] DESC, [contention_key] DESC
  '''
    data = sql_connection(query, 'master') 
        
    return data

def contention_for_TSHApproval(tshcode):
    query = f''' 
       SELECT  [POLICY NUMBER]
              ,[TYPE OF CONTENTION]
              ,[CONTENTION DETAILS]
              ,[BDM Approval] AS [BDM STATUS]
              ,CAST([FILE_UPLOAD] AS varbinary(max)) AS [FILE_UPLOAD]
              ,[BDM Comments]
              ,[Date Submit] 
              ,contention_key
      FROM [db_Contention].[dbo].[tbl_contention_logs]
      WHERE [TSH CODE] = {tshcode} AND [TSH Approval] = 'PENDING'
  '''
    data = sql_connection(query, 'master') 
        
    return data

def Select_BCAApproved(begdate, enddate, policy, bsename='', typecontention=''):
    query = f''' 
       SELECT  [POLICY NUMBER]
              ,[BSE NAME]
              ,[TYPE OF CONTENTION]
              ,[CONTENTION DETAILS]
              ,[BCA Approval] AS [BCA STATUS]
              ,[BCA Comments]
              ,[BCA Approved Dates]
      FROM [db_Contention].[dbo].[tbl_contention_logs]
      WHERE  ([BCA Approval] = 'APPROVED') AND ([BCA Approved Dates] BETWEEN '{begdate}' AND '{enddate}') AND [POLICY NUMBER] LIKE '{policy}%'
      AND [BSE NAME] LIKE '%{bsename}%' AND [TYPE OF CONTENTION] LIKE '{typecontention}%'
      ORDER BY [BCA Approved Dates] DESC, [contention_key] DESC
  '''
    data = sql_connection(query, 'master') 
        
    return data

def contention_for_BCAApproval():
    query = f''' 
       SELECT  [POLICY NUMBER]
              ,[TYPE OF CONTENTION]
              ,[CONTENTION DETAILS]
              ,[BCA Approval] AS [BCA STATUS]
              ,CAST([FILE_UPLOAD] AS varbinary(max)) AS [FILE_UPLOAD]
              ,[BCA Comments]
              ,[Date Submit] 
              ,contention_key
      FROM [db_Contention].[dbo].[tbl_contention_logs]
      WHERE [BCA Approval] = 'PENDING'
  '''
    data = sql_connection(query, 'master') 
        
    return data

def contention_for_BASApproval(begdate, enddate, policy):
    query = f''' 
       SELECT  [POLICY NUMBER]
              ,[TYPE OF CONTENTION]
              ,[CONTENTION DETAILS]
              ,[BCA Approval] AS [BCA STATUS]
              ,CAST([FILE_UPLOAD] AS varbinary(max)) AS [FILE_UPLOAD]
              ,[BAS Comment]
              ,[Date Submit] 
              ,[BCA Approved Dates]
              ,contention_key
      FROM [db_Contention].[dbo].[tbl_contention_logs]
      WHERE  ([BCA Approval] = 'APPROVED') AND ([BCA Approved Dates] BETWEEN '{begdate}' AND '{enddate}') AND [POLICY NUMBER] LIKE '{policy}%' AND ([BAS Comment] IS NULL OR [BAS Comment] ='' OR [BAS Comment] =' ')
  '''
    data = sql_connection(query, 'master') 
        
    return data


def Select_BASApproved(begdate, enddate, policy, bsename='', typecontention=''):
    query = f''' 
       SELECT  [POLICY NUMBER]
              ,[TYPE OF CONTENTION]
              ,[BSE NAME]
              ,[CONTENTION DETAILS]
              ,[BCA Approval] AS [BCA STATUS]
              ,CAST([FILE_UPLOAD] AS varbinary(max)) AS [FILE_UPLOAD]
              ,[BCA Comments]
              ,[BCA Approved Dates]
              ,[BAS Comment] AS [EFFECTIVE DATE]
              ,[Date Submit]
      FROM [db_Contention].[dbo].[tbl_contention_logs]
      -- WHERE  ([BCA Approval] = 'APPROVED') AND ([BCA Approved Dates] BETWEEN '{begdate}' AND '{enddate}') AND [POLICY NUMBER] LIKE '{policy}%'
      WHERE  ([BCA Approval] = 'APPROVED') AND ([BCA Approved Dates] BETWEEN '{begdate}' AND '{enddate}') AND [POLICY NUMBER] LIKE '{policy}%' AND ([BAS Comment] IS NOT NULL AND [BAS Comment]  !='' )
      AND [BSE NAME] LIKE '%{bsename}%' AND [TYPE OF CONTENTION] LIKE '{typecontention}%'
      ORDER BY [BCA Approved Dates] DESC, [contention_key] DESC
  '''
    data = sql_connection(query, 'master') 
    
    return data
    
def bytes_to_base64(bytes_data):
    return base64.b64encode(bytes_data).decode()

def display_image_bas(image_data):
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    return image

def click_button():
    st.session_state.button = True
    
def click_logout():
    st.session_state.button = False

def sql_update(sql_query, dbase):
    # Replace with your actual SQL Server connection details
    server = 'PPBWDLC0SG7A1'
    database = dbase
    username = 'admin'
    password = 'Openlab@123'

    # Define the connection string
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )

    try:
        # Establish the connection
        conn = pyodbc.connect(connection_string)

        # Define the UPDATE query
        query = sql_query

        # Execute the UPDATE query
        conn.execute(query)
        conn.commit()

        print("Update successful")

    except pyodbc.Error as e:
        print("Error updating data in SQL Server:", e)
    finally:
        # Close the connection
        conn.close()

def main():
    menu = ["Home","BSE Login", "BAM Login", "BDM Login", "TSH Login", "BCA Login", "BAS Login"]
    
    choice = st.sidebar.selectbox("Menu",menu)
    
    if choice == "Home":
        st.markdown(f"<h2 style='text-align: center; color: black;'> CONTENTION FORM </h2> <br>", unsafe_allow_html=True)
        
        components.html('''
                        
                        <!doctype html>
                                <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1">
                                <title>Carousel Template · Bootstrap v5.0</title>
                                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                                <style>
                            
                                    .marketing .col-lg-4 {
                                      margin-bottom: 1.5rem;
                                      text-align: center;
                                    }
                                    .marketing h2 {
                                      font-weight: 400;
                                    }
                                    .marketing .col-lg-4 p {
                                      margin-right: .75rem;
                                      margin-left: .75rem;
                                    }
                            
                            
                                    .featurette-divider {
                                      margin: 5rem 0; 
                                    }
                            
                                    .featurette-heading {
                                      font-weight: 300;
                                      line-height: 1;
                                      letter-spacing: -.05rem;
                                    }
                                    
                                    * {box-sizing: border-box;}
                                        body {font-family: Verdana, sans-serif;}
                                        .mySlides {display: none;}
                                        img {vertical-align: middle;}
                                        
                                        /* Slideshow container */
                                        .slideshow-container {
                                          max-width: 1000px;
                                          position: relative;
                                          margin: auto;
                                        }
                                        
                                        /* Caption text */
                                        .text {
                                          color: #f2f2f2;
                                          font-size: 15px;
                                          padding: 8px 12px;
                                          position: absolute;
                                          bottom: 8px;
                                          width: 100%;
                                          text-align: center;
                                        }
                                        
                                        /* Number text (1/3 etc) */
                                        .numbertext {
                                          color: #f2f2f2;
                                          font-size: 12px;
                                          padding: 8px 12px;
                                          position: absolute;
                                          top: 0;
                                        }
                                        
                                        /* The dots/bullets/indicators */
                                        .dot {
                                          height: 15px;
                                          width: 15px;
                                          margin: 0 2px;
                                          background-color: #bbb;
                                          border-radius: 50%;
                                          display: inline-block;
                                          transition: background-color 0.6s ease;
                                        }
                                        
                                        .active {
                                          background-color: #717171;
                                        }
                                        
                                        /* Fading animation */
                                        .fade {
                                          animation-name: fade;
                                          animation-duration: 4s;
                                        }
                                        
                                        @keyframes fade {
                                          from {opacity: .4} 
                                          to {opacity: 1}
                                        }
                                        
                                        /* On smaller screens, decrease text size */
                                        @media only screen and (max-width: 300px) {
                                          .text {font-size: 11px}
                                        }
  
                                </style>
                                
                                <!-- Custom styles for this template -->
                              </head>
                              <body>
                                
                            <br> </br>
                            
                              <div class="container marketing">
                            
                                <!-- Three columns of text below the carousel -->
                                <div class="row">
                                  <div class="col-lg-4">
                                    <svg class="bd-placeholder-img rounded-circle" width="140" height="140" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder: 140x140" preserveAspectRatio="xMidYMid slice" focusable="false"><title>Placeholder</title><rect width="100%" height="100%" fill="#777"/><text x="50%" y="50%" fill="#777" dy=".3em">140x140</text></svg>
                            
                                    <h2>Heading</h2>
                                    <p>Some representative placeholder content for the three columns of text below the carousel. This is the first column.</p>
                                  </div><!-- /.col-lg-4 -->
                                  <div class="col-lg-4">
                                    <svg class="bd-placeholder-img rounded-circle" width="140" height="140" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder: 140x140" preserveAspectRatio="xMidYMid slice" focusable="false"><title>Placeholder</title><rect width="100%" height="100%" fill="#777"/><text x="50%" y="50%" fill="#777" dy=".3em">140x140</text></svg>
                            
                                    <h2>Heading</h2>
                                    <p>Another exciting bit of representative placeholder content. This time, we've moved on to the second column.</p>
                                  </div><!-- /.col-lg-4 -->
                                  <div class="col-lg-4">
                                    <svg class="bd-placeholder-img rounded-circle" width="140" height="140" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder: 140x140" preserveAspectRatio="xMidYMid slice" focusable="false"><title>Placeholder</title><rect width="100%" height="100%" fill="#777"/><text x="50%" y="50%" fill="#777" dy=".3em">140x140</text></svg>
                            
                                    <h2>Heading</h2>
                                    <p>And lastly this, the third column of representative placeholder content.</p>
                                  </div><!-- /.col-lg-4 -->
                                </div><!-- /.row -->
                            
                            
                              </div><!-- /.container -->
                              
                              <!-- <h2 style='text-align: center; color: black;'>Automatic Slideshow</h2> -->
                                
                                <div class="slideshow-container">
                                
                                <div class="mySlides fade">
                                  <div class="numbertext">1 / 3</div>
                                  <img src="https://www.bpi-aia.com.ph/content/dam/bplac/en/photos/press-release/bpi-aia-pamilya-protect-kv.png?force=true&w=1920" style="width:100%; max-height: 350px;">
                                  <div class="text"></div>
                                </div>
                                
                                <div class="mySlides fade">
                                  <div class="numbertext">2 / 3</div>
                                  <img src="https://tse3.mm.bing.net/th/id/OIP.EnjwKVyP7iou9dP2JO0zSQAAAA?w=474&h=215&rs=1&pid=ImgDetMain?force=true&w=1920" style="width:100%; max-height: 350px;">
                                  <div class="text"></div>
                                </div>
                                
                                <div class="mySlides fade">
                                  <div class="numbertext">3 / 3</div>
                                  <img src="https://tse4.mm.bing.net/th/id/OIP.6azoq1Hwk-AuCBf54c8IZgHaEK?rs=1&pid=ImgDetMain?force=true&w=1920" style="width:100%; max-height: 350px;">
                                  <div class="text"></div>
                                </div>
                                
                                </div>
                                <br>
                                
                                <div style="text-align:center">
                                  <span class="dot"></span> 
                                  <span class="dot"></span> 
                                  <span class="dot"></span> 
                                </div>
                                
                                <script>
                                let slideIndex = 0;
                                showSlides();
                                
                                function showSlides() {
                                  let i;
                                  let slides = document.getElementsByClassName("mySlides");
                                  let dots = document.getElementsByClassName("dot");
                                  for (i = 0; i < slides.length; i++) {
                                    slides[i].style.display = "none";  
                                  }
                                  slideIndex++;
                                  if (slideIndex > slides.length) {slideIndex = 1}    
                                  for (i = 0; i < dots.length; i++) {
                                    dots[i].className = dots[i].className.replace(" active", "");
                                  }
                                  slides[slideIndex-1].style.display = "block";  
                                  dots[slideIndex-1].className += " active";
                                  setTimeout(showSlides, 2000); // Change image every 2 seconds
                                }
                                </script>
                            
                            <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
                                  
                              </body>
                            </html>
                                                                                                
                        ''', height=1200,
            )
        
    
    
    elif choice == "BSE Login":
        username = st.sidebar.text_input("User Surname")
        password = st.sidebar.text_input("BSE CODE",type='password')
        st.session_state.bsecode = password
        css = '''
                <style>
                    [data-testid='stFileUploader'] section {
                        padding: 0;
                        float: center;A
                    }
                    [data-testid='stFileUploader'] section > input + div {
                        display: none;
                    }
                    [data-testid='stFileUploader'] section + div {
                        float: center;
                        padding-top: 0;
                    }
                
                </style>
                '''
        
        if 'button' not in st.session_state:
            st.session_state.button = False
        
        scol1, scol2 = st.sidebar.columns([1,0.5])
        
        scol1.button('Login', type="primary", on_click=click_button)
        
        scol2.button('Logout', on_click=click_logout)
        
        #if st.sidebar.toggle("Login"):
        if st.session_state.button:
            # if password == '12345':
            #hashed_pswd = make_hashes(password)
            result = login_user(username, password, choice)
            if len(result) >=1:
                
                option_data = [
                                   {'icon': "bi bi-hand-thumbs-up", 'label':"Contention Form"},
                                   {'icon':"fa fa-question-circle",'label':"Contention History"},
                                   {'icon':"fa fa-solid fa-coffee", 'label':"Dashboard"},
                                ]
                
                # override the theme, else it will use the Streamlit applied theme
                over_theme = {'txc_inactive': 'white','menu_background':'grey','txc_active':'white','option_active':'black'}
                font_fmt = {'font-class':'h2','font-size':'150%'}    

                task = hc.option_bar(option_definition=option_data,title=' ',key='PrimaryOption',override_theme=over_theme,font_styling=font_fmt,horizontal_orientation=True)

                                            
                # task = st_navbar(["Contention Form", "Contention History", "Profiles"])
                #st.success("Logged In as {}".format(result['BSE FULL NAME'].loc[0]))
                    
                if task == "Contention Form":
                    
                    #st.markdown(f"<h2 style='text-align: center; color: black;'>CONTENTION FORM FOR BSE {result['BSE FULL NAME'].loc[0]} </h2> <br>", unsafe_allow_html=True)
                    
                    if 'data' not in st.session_state:
                        data = pd.DataFrame({'POLICY NUMBER':[],'TYPE OF CONTENTION':[],'CONTENTION DETAILS':[],'ATTACHMENT':[], 'FILE_UPLOAD':[]})
                        st.session_state.data = data
                                                
                    df_edited = st.data_editor(st.session_state.data, num_rows= "dynamic", hide_index = 1, disabled=(["POLICY NUMBER", "TYPE OF CONTENTION", "ATTACHMENT"]), column_order=(["POLICY NUMBER", "TYPE OF CONTENTION", "CONTENTION DETAILS", "ATTACHMENT"]), use_container_width=True, key='df_editedA')
                    #df_edited = st.data_editor(st.session_state.data, num_rows= "dynamic", hide_index = 1, use_container_width=True, key='df_editedA')
                    st.session_state.data = df_edited
                    
                    dfForm = st.form(key='dfForm', clear_on_submit=True)
                    with dfForm:
                        #dfColumns = st.columns([1.25,1.25,1.25,1.1])
                        dfColumns = st.columns([1,1,1,0.85])
                        with dfColumns[0]:
                            # st.selectbox('POLICY NUMBER',tuple(T1_POLNUM(password)['POLNUM']), index=None, placeholder="Select Policy Number...", key='input_colA')
                            
                            value = st_free_text_select(
                                label="POLICY NUMBER",
                                options=tuple(T1_POLNUM(password)['POLNUM']),
                                format_func=lambda x: x.lower(),
                                placeholder="Select Policy Number...",
                                disabled=False,
                                delay=300, key='input_colA'
                            )
                            
                        with dfColumns[1]:
                            st.selectbox('TYPE OF CONTENTION',(
                              'Retag BSE, BAM, BDM',
                              'Retag Branch, Area, Division, or Territory',
                              'Retag Referrer Name or Referrer Category',
                              'Change BSE Segment',
                              'Change Credit Month',
                              'Change ANP / FYP Amount',
                              'Change Production Splitting',
                              'Update Policy Status',
                              'Add Missing Policy',
                              'Remove Policy'), index=None, placeholder="Select Type of Contention...", key='input_colB')
                        with dfColumns[2]:
                            st.text_input('CONTENTION DETAILS',  key='input_colC')
                        with dfColumns[3]:   
                            #CHOOSE PICTURE FILES FOR REQUIREMENTS (REQUIRED)
                            st.file_uploader("IMAGE FILES PROOF (REQUIRED)", accept_multiple_files=True, key='input_upload')
                            st.markdown(css, unsafe_allow_html=True)
                        
                        st.form_submit_button(label='Add', on_click=add_dfForm)
                         
                    columns = st.columns((1,1,1,1))

                    with columns[0]:
                        st.write('')
                    with columns[1]:
                        st.write('')
                    # No usage of 3rd position on the columns.
                    with columns[3]:
                        st.button("Submit", on_click=remove_dfForm, args=(df_edited, 
                                                                          password, 
                                                                          result['BSE FULL NAME'].loc[0],
                                                                          result['BAM'].loc[0], 
                                                                          result['BAM CODE'].loc[0], result['BDM'].loc[0], 
                                                                          result['BDM CODE'].loc[0], result['TSH'].loc[0], result['TSH CODE'].loc[0]), use_container_width=True, type="primary") 
                                            
                
                    #st.dataframe(email_matching(password), hide_index=True)
                    #st.write(email_matching(password).loc[0, 'BSEEMAIL'])
                    
                
                elif task == "Contention History":
                    #st.write('Add Analytics Here')
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"<h5 style= color: black;'> Select Contention Dates </h5>", unsafe_allow_html=True)
                        date_input = st.date_input(
                            "submit date",
                            ((datetime.now() -  timedelta(days=7)) , datetime.now()),label_visibility = 'hidden', key='bse_date_col'
                            )
                        
                    with col2:
                        st.markdown(f"<h5 style= color: black;'> Input Policy Number</h5>", unsafe_allow_html=True)
                        pol = st.text_input("inputpolnum", placeholder = 'Input Policy Number . . .', label_visibility = 'hidden', key = 'input_pol_col')  
                        

                    with col3:
                        st.markdown(f"<h5 style= color: black;'> Select Contention Status </h5>", unsafe_allow_html=True)
                        option = st.selectbox(
                            "contention_option",
                            ('PENDING|APPROVED|REJECTED',"PENDING", "APPROVED", "REJECTED"), label_visibility = 'hidden', key='con_status_col')

                    with col4:
                        st.markdown(f"<h5 style= color: black;'> Type of Contention </h5>", unsafe_allow_html=True)
                        bse_typeselection = st.selectbox('TYPE OF CONTENTION',(
                            '',
                          'Retag BSE, BAM, BDM',
                          'Retag Branch, Area, Division, or Territory',
                          'Retag Referrer Name or Referrer Category',
                          'Change BSE Segment',
                          'Change Credit Month',
                          'Change ANP / FYP Amount',
                          'Change Production Splitting',
                          'Update Policy Status',
                          'Add Missing Policy',
                          'Remove Policy'), placeholder="Select Type of Contention...",label_visibility ='hidden', key='input_contype_col')
                        
                    bcol1, bcol2, bcol3, bcol4 = st.columns(4)
                    with bcol1:
                        ''
                    with bcol2:
                        ''
                    with bcol3:
                        ''
                    with bcol4:
                        clear_button = st.button("Clear Inputs", type="primary", use_container_width=True, on_click=Clear_BSEFilter)
                    
                    st.markdown(f"<h4 style= color: black;'> Contention Report </h4>", unsafe_allow_html=True)
                    df_contention = contention_history(password, date_input[0], date_input[1], pol, bse_typeselection).copy()
                    
                    # df_contention = contention_history(password).copy()
                    
                    # df_contention = df_contention.loc[df_contention['POLICY NUMBER'].str.contains(pol, na=False)]
                    
                    # #df_contention = df_contention.loc[df_contention['Date Submit'].astype(str) == str(date_input[1])]
                    # df_contention = df_contention.loc[(df_contention['Date Submit'] >= str(date_input[0])) & (df_contention['Date Submit'] <= str(date_input[1]))]
                    
                    df_contention = df_contention.loc[df_contention['FINAL STATUS'].str.contains(option, na=False)]
                  
                    st.dataframe(df_contention.style.map(color_status, subset =['BAM STATUS', 'BDM STATUS', 'TSH STATUS', 'BCA STATUS', 'FINAL STATUS']), use_container_width=True, height=700 , hide_index=True)
                    #st.write(date_input[0], (date_input[1]))
                
                elif task == "Dashboard":
                    
                    st.markdown(f"<h4 style = 'text-align: center; color: black;'>TOTTENHAM HOTSPURS INCENTIVES</h4> <br>", unsafe_allow_html=True)

                    segment_result = result.at[0, 'SEGMENT']
                    
                    
                   
            else:
                st.error("Account does not Exist")
        else:
            st.warning("Please enter username and password")
            
    
    elif choice == "BAM Login":
        username = st.sidebar.text_input("User Surname")
        password = st.sidebar.text_input("BAM CODE",type='password')
        if 'button' not in st.session_state:
            st.session_state.button = False
        
        scol1, scol2 = st.sidebar.columns([1,0.5])
        
        scol1.button('Login', type="primary", on_click=click_button)
        
        scol2.button('Logout', on_click=click_logout)
        
        if st.session_state.button:
        # if st.sidebar.toggle("Login"):
            # if password == '12345':
            #hashed_pswd = make_hashes(password)
            
            result = login_user(username, password, choice)
            if len(result) >=1:
                
                option_data = [
                                   {'icon': "bi bi-hand-thumbs-up", 'label':"Contention For Approval"},
                                   {'icon':"fa fa-question-circle",'label':"Approved Contention"},
                                   {'icon':"fa fa-solid fa-coffee", 'label':"Placeholder"},
                                ]
                
                # override the theme, else it will use the Streamlit applied theme
                over_theme = {'txc_inactive': 'white','menu_background':'grey','txc_active':'white','option_active':'black'}
                font_fmt = {'font-class':'h2','font-size':'150%'}   

                task = hc.option_bar(option_definition=option_data,title=' ',key='PrimaryOption',override_theme=over_theme,font_styling=font_fmt,horizontal_orientation=True)

                # task = st_navbar(["Contention For Approval", "Approved Contention", "Profiles"])
                # st.success("Logged In as {}".format(result['BAM FULL NAME'].loc[0]))
                    
                if task == "Contention For Approval":
                    #st.markdown(f"<h2 style='text-align: center; color: black;'>CONTENTION FORM FOR APPROVAL FOR {result['BAM FULL NAME'].loc[0]} </h2> <br>", unsafe_allow_html=True)
                    bam_approval = contention_for_BAMApproval(password)
                    bam_approval['IMAGE_DATA'] = bam_approval['FILE_UPLOAD'].apply(bytes_to_base64)
                    
                    
                    # ucol1, ucol2, ucol3, ucol4, ucol5, ucol6 = st.columns([1,1.5,2.5,1,1,1])

                    # with ucol1:
                    #  ''
                    # with ucol2:
                    #  ''
                    # with ucol3:
                    #  ''
                    # with ucol4:
                    #  ''
                    # with ucol5:
                    #  ''
                    # with ucol6:
                    #  check_all = st.checkbox("Check All", help='Tick for Approve All')
                    
                    
                    col1, col2, col3, col4, col5, col6 = st.columns([1,1.25,1.5,1.5,.75,1])
                    
                    loop_space = 3
                    with col1:

                        st.markdown(f"<h4 style= color: black;'>POLICY NUMBER </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bam_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bam_approval.loc[i, "POLICY NUMBER"])
                            for _ in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                        
                    with col2:
                        st.markdown(f"<h4 style= color: black;'>TYPE OF CONTENTION </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bam_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bam_approval.loc[i, "TYPE OF CONTENTION"])
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
    
                    with col3:
                        st.markdown(f"<h4 style= color: black;'>CONTENTION DETAILS</h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bam_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bam_approval.loc[i, "CONTENTION DETAILS"])
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                            
                    with col4:
                        st.markdown(f"<h4 style= color: black;'>FILE UPLOAD </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bam_approval)):
                            container = st.container(border=True, height=150)
                            try:
                                container.image(Image.open(io.BytesIO(base64.b64decode(bam_approval['IMAGE_DATA'][i]))), caption='Image', use_column_width=True)
                            except:
                                pass
                                
                    # with col5:
                    #     st.markdown(f"<h4 style=color: black;'>ENDORSEMENT </h4> <br>", unsafe_allow_html=True)
                    #     approval_values = [] # To store checkbox values
                    #     for i in range(len(bam_approval)):
                    #         container = st.container(border=True, height=150)
                    #         if check_all:
                    #             checkbox_value = container.checkbox(f"Approve", value=True, key=f"{i}_checkboxkey", help='Tick for Approve Untick for Reject')
                    #             for i in range(loop_space):
                    #                 container.markdown("<br>", unsafe_allow_html=True)
                                
                    #         else:
                    #             checkbox_value = container.checkbox(f"Approve", key=f"{i}_checkboxkey",help='Tick for Approve Untick for Reject')
                    #             for i in range(loop_space):
                    #                 container.markdown("<br>", unsafe_allow_html=True)
                                    
                    #         approval_values.append(checkbox_value)
                    
                    with col5:
                        st.markdown(f"<h4 style=color: black;'>ENDORSEMENT </h4> <br>", unsafe_allow_html=True)
                        approval_values = [] # To store radio button values
                        for i in range(len(bam_approval)):
                            container = st.container(border=True, height=150)
                            # if check_all:
                            #     radio_value = container.radio("Approve or Reject", options=["Approve", "Reject"], index=0, key=f"{i}_radiokey", help='Select Approve or Reject')
                            #     for i in range(loop_space):
                            #         container.markdown("<br>", unsafe_allow_html=True)
                            # else:
                            #     radio_value = container.radio("Approve or Reject", options=["Approve", "Reject"], index=0, key=f"{i}_radiokey", help='Select Approve or Reject')
                            #     for i in range(loop_space):
                            #         container.markdown("<br>", unsafe_allow_html=True)
                            
                            radio_value = container.radio("Approve or Reject", options=["Approve", "Reject"], index=0, key=f"{i}_radiokey", help='Select Approve or Reject')
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                                    
                                   # Append the selected value as "Approve" or "Reject"
                            if radio_value == "Approve":
                                approval_values.append(True)
                            else:
                                approval_values.append(False)
                
                    with col6:
                        comment_values = []
                        st.markdown(f"<h4 style= color: black;'> COMMENTS </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bam_approval)):
                            container = st.container(border=True, height=150)
                            comments_apprvr = container.text_input('Comments',placeholder="Comments", label_visibility="collapsed", key=f"{i}_container")
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                            comment_values.append(comments_apprvr)
                        
                    
                    # Add a "Submit" button
                    if st.button("Submit",):
                        # Update DataFrame with checkbox values
                        bam_approval['BAM NEW STATUS'] = approval_values
                        bam_approval['BAM NEW STATUS'] = np.where(bam_approval['BAM NEW STATUS'] == True, "APPROVED", "REJECTED")
                        bam_approval['BAM COMMENTS'] = comment_values
                        bam_approval['BDM NEW STATUS'] = np.where(bam_approval['BAM NEW STATUS'] == 'APPROVED', 'PENDING', 'NO ACTION NEEDED YET')
                        bam_approval = bam_approval[['BAM NEW STATUS', 'contention_key', 'BAM COMMENTS', 'BDM NEW STATUS']]
                        #st.write("DataFrame updated successfully!")
                        #st.write(bam_approval)
                        
                        for i in range(len(bam_approval)):
                            bamnewstat = bam_approval.loc[i, "BAM NEW STATUS"]
                            bdmnewstat = bam_approval.loc[i, "BDM NEW STATUS"]
                            contention_key = bam_approval.loc[i, "contention_key"]
                            bamcommt = bam_approval.loc[i, "BAM COMMENTS"]
                            bamapprvdate = datetime.now().strftime('%Y-%m-%d')
                            #st.write(bamnewstat)
                            
                            sql_query = f'''
                                        UPDATE [db_Contention].[dbo].[tbl_contention_logs]
                                        SET [BAM Approval] = '{bamnewstat}', 
                                            [BAM Comments] = '{bamcommt}', 
                                            [BAM Approved Dates] = '{bamapprvdate}',
                                            [BDM Approval] = '{bdmnewstat}'
                                        WHERE [contention_key] = {contention_key}
                                    '''
                            
                            sql_update(sql_query, 'db_Contention')
                        
                        time.sleep(1)
                        try:
                            st.session_state.clear()
                            st.write("Updated Successfully!")

                        except:
                            st.write("Updated Successfully!")
                            st.write("Refresh the Page")
                            pass
                        #st.experimental_rerun()
                        #streamlit_js_eval(js_expressions="parent.window.location.reload()")
                        
                    
                elif task == "Approved Contention":
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"<h4 style= color: black;'> Select Contention Dates </h4>", unsafe_allow_html=True)
                        date_input = st.date_input(
                            "",
                            ((datetime.now() -  timedelta(days=7)) , datetime.now()), label_visibility= 'hidden', key='bse_date_col'
                            )
                        
                    with col2:
                        st.markdown(f"<h4 style= color: black;'> Input Policy Number</h4>", unsafe_allow_html=True)
                        pol = st.text_input("", placeholder = 'Input Policy Number . . .', key='input_pol_col')  
                        

                    with col3:
                        st.markdown(f"<h4 style= color: black;'> Input BSE Name </h4>", unsafe_allow_html=True)
                        bse_name = st.text_input("", placeholder = 'Input BSE Name Number . . .', key='input_bsename_col')

                    with col4:
                        st.markdown(f"<h4 style= color: black;'> Type of Contention </h4>", unsafe_allow_html=True)
                        bse_typeselection = st.selectbox('TYPE OF CONTENTION',(
                            '',
                          'Retag BSE, BAM, BDM',
                          'Retag Branch, Area, Division, or Territory',
                          'Retag Referrer Name or Referrer Category',
                          'Change BSE Segment',
                          'Change Credit Month',
                          'Change ANP / FYP Amount',
                          'Change Production Splitting',
                          'Update Policy Status',
                          'Add Missing Policy',
                          'Remove Policy'), placeholder="Select Type of Contention...",label_visibility ='hidden', key='input_contype_col')
                    
                    
                    bcol1, bcol2, bcol3, bcol4 = st.columns(4)
                    with bcol1:
                        ''
                    with bcol2:
                        ''
                    with bcol3:
                        ''
                    with bcol4:
                        clear_button = st.button("Clear Inputs", type="primary", use_container_width=True, on_click=Clear_BAMFilter)
                    
                    st.markdown(f"<h4 style= color: black;'> Contention Report </h4>", unsafe_allow_html=True)
                    df_apprv_cont = Select_BAMApproved(password, date_input[0], date_input[1], pol, bse_name, bse_typeselection).copy()
                   
                    st.dataframe(df_apprv_cont, use_container_width = True)                    
                
                                        
                elif task == "Profiles":
                    st.write("Profile Here")
            else:
                st.error("Account does not Exist")
        else:
            st.warning("Please enter username and password")


    elif choice == "BDM Login":
        username = st.sidebar.text_input("User Surname")
        password = st.sidebar.text_input("BDM CODE",type='password')
        
        if 'button' not in st.session_state:
            st.session_state.button = False
        
        scol1, scol2 = st.sidebar.columns([1,0.5])
        
        scol1.button('Login', type="primary", on_click=click_button)
        
        scol2.button('Logout', on_click=click_logout)
        
        #if st.sidebar.toggle("Login"):
        if st.session_state.button:
            # if password == '12345':
            #hashed_pswd = make_hashes(password)
            result = login_user(username, password, choice)
            if len(result) >=1:
                
                option_data = [
                                   {'icon': "bi bi-hand-thumbs-up", 'label':"Contention For Approval"},
                                   {'icon':"fa fa-question-circle",'label':"Approved Contention"},
                                   {'icon':"fa fa-solid fa-coffee", 'label':"Placeholder"},
                                ]
                
                # override the theme, else it will use the Streamlit applied theme
                over_theme = {'txc_inactive': 'white','menu_background':'grey','txc_active':'white','option_active':'black'}
                font_fmt = {'font-class':'h2','font-size':'150%'}     

                task = hc.option_bar(option_definition=option_data,title=' ',key='PrimaryOption',override_theme=over_theme,font_styling=font_fmt,horizontal_orientation=True)

                #task = st_navbar(["Contention For Approval", "Approved Contention", "Profiles"])
                # st.success("Logged In as {}".format(result['BAM FULL NAME'].loc[0]))
                    
                if task == "Contention For Approval":
                    #st.markdown(f"<h2 style='text-align: center; color: black;'>CONTENTION FORM FOR APPROVAL FOR {result['BDM FULL NAME'].loc[0]} </h2> <br>", unsafe_allow_html=True)
                    bdm_approval = contention_for_BDMApproval(password)
                    bdm_approval['IMAGE_DATA'] = bdm_approval['FILE_UPLOAD'].apply(bytes_to_base64)
                    
                    
                    # ucol1, ucol2, ucol3, ucol4, ucol5, ucol6 = st.columns([1,1.5,2.5,1,1,1])
    
                    # with ucol1:
                    #  ''
                    # with ucol2:
                    #  ''
                    # with ucol3:
                    #  ''
                    # with ucol4:
                    #  ''
                    # with ucol5:
                    #  ''
                    # with ucol6:
                    #  check_all = st.checkbox("Check All", help='Tick for Approve All')
                    
                    
                    col1, col2, col3, col4, col5, col6 = st.columns([1,1.25,1.5,1.5,.75,1])
                    
                    loop_space = 3
                    with col1:
    
                        st.markdown(f"<h4 style= color: black;'>POLICY NUMBER </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bdm_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bdm_approval.loc[i, "POLICY NUMBER"])
                            for _ in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                        
                    with col2:
                        st.markdown(f"<h4 style= color: black;'>TYPE OF CONTENTION </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bdm_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bdm_approval.loc[i, "TYPE OF CONTENTION"])
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
    
                    with col3:
                        st.markdown(f"<h4 style= color: black;'>CONTENTION DETAILS</h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bdm_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bdm_approval.loc[i, "CONTENTION DETAILS"])
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                            
                    with col4:
                        st.markdown(f"<h4 style= color: black;'>FILE UPLOAD </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bdm_approval)):
                            container = st.container(border=True, height=150)
                            try:
                                container.image(Image.open(io.BytesIO(base64.b64decode(bdm_approval['IMAGE_DATA'][i]))), caption='Image', use_column_width=True)
                            except:
                                pass
                                
                    with col5:
                        st.markdown(f"<h4 style=color: black;'>ENDORSEMENT </h4> <br>", unsafe_allow_html=True)
                        approval_values = [] # To store checkbox values
                        for i in range(len(bdm_approval)):
                            container = st.container(border=True, height=150)
                            # if check_all:
                            #     radio_value = container.radio("Approve or Reject", options=["Approve", "Reject"], index=0, key=f"{i}_radiokey", help='Select Approve or Reject')
                            #     for i in range(loop_space):
                            #         container.markdown("<br>", unsafe_allow_html=True)
                            # else:
                            #     radio_value = container.radio("Approve or Reject", options=["Approve", "Reject"], index=0, key=f"{i}_radiokey", help='Select Approve or Reject')
                            #     for i in range(loop_space):
                            #         container.markdown("<br>", unsafe_allow_html=True)
                            
                            radio_value = container.radio("Approve or Reject", options=["Approve", "Reject"], index=0, key=f"{i}_radiokey", help='Select Approve or Reject')
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)

                          
                                   # Append the selected value as "Approve" or "Reject"
                            if radio_value == "Approve":
                                approval_values.append(True)
                            else:
                                approval_values.append(False)
                    
                    with col6:
                        comment_values = []
                        st.markdown(f"<h4 style= color: black;'> COMMENTS </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bdm_approval)):
                            container = st.container(border=True, height=150)
                            comments_apprvr = container.text_input('Comments',placeholder="Comments", label_visibility="collapsed", key=f"{i}_container")
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                            comment_values.append(comments_apprvr)
                        
                    
                    # Add a "Submit" button
                    if st.button("Submit",):
                        # Update DataFrame with checkbox values
                        bdm_approval['BDM NEW STATUS'] = approval_values
                        bdm_approval['BDM NEW STATUS'] = np.where(bdm_approval['BDM NEW STATUS'] == True, "APPROVED", "REJECTED")
                        bdm_approval['BDM COMMENTS'] = comment_values
                        bdm_approval['TSH NEW STATUS'] = np.where(bdm_approval['BDM NEW STATUS'] == 'APPROVED', 'PENDING', 'NO ACTION NEEDED YET')
                        bdm_approval = bdm_approval[['BDM NEW STATUS', 'contention_key', 'BDM COMMENTS', 'TSH NEW STATUS']]

                        
                        for i in range(len(bdm_approval)):
                            bdmnewstat = bdm_approval.loc[i, "BDM NEW STATUS"]
                            tshnewstat = bdm_approval.loc[i, "TSH NEW STATUS"]
                            contention_key = bdm_approval.loc[i, "contention_key"]
                            bdmcommt = bdm_approval.loc[i, "BDM COMMENTS"]
                            bdmapprvdate = datetime.now().strftime('%Y-%m-%d')
                            #st.write(bamnewstat)
                            
                            sql_query = f'''
                                        UPDATE [db_Contention].[dbo].[tbl_contention_logs]
                                        SET [BDM Approval] = '{bdmnewstat}', 
                                            [BDM Comments] = '{bdmcommt}', 
                                            [BDM Approved Dates] = '{bdmapprvdate}',
                                            [TSH Approval] = '{tshnewstat}'
                                        WHERE [contention_key] = {contention_key} AND [TSH Approval] != 'NOT REQUIRED'
                                    '''
                            
                            sql_update(sql_query, 'db_Contention')
                        
                        
                            sql_query = f'''
                                        UPDATE [db_Contention].[dbo].[tbl_contention_logs]
                                        SET [BDM Approval] = '{bdmnewstat}', 
                                            [BDM Comments] = '{bdmcommt}', 
                                            [BDM Approved Dates] = '{bdmapprvdate}',
                                            [BCA Approval] = '{tshnewstat}'
                                        WHERE [contention_key] = {contention_key} AND [TSH Approval] = 'NOT REQUIRED'
                                    '''
                            
                            sql_update(sql_query, 'db_Contention')
                        
                        time.sleep(1)
                        
                        try:
                            st.rerun()
                            st.write("Updated Successfully!")
    
                        except:
                            st.write("Updated Successfully!")
                            st.write("Refresh the Page")
                            pass
                        #st.experimental_rerun()
                        #streamlit_js_eval(js_expressions="parent.window.location.reload()")
                        
                    
                elif task == "Approved Contention":
                    #st.write('Add Analytics Here')
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"<h4 style= color: black;'> Select Contention Dates </h4>", unsafe_allow_html=True)
                        date_input = st.date_input(
                            "",
                            ((datetime.now() -  timedelta(days=7)) , datetime.now()), label_visibility ='hidden', key='bse_date_col'
                            )
                        
                    with col2:
                        st.markdown(f"<h4 style= color: black;'> Input Policy Number</h4>", unsafe_allow_html=True)
                        pol = st.text_input("", placeholder = 'Input Policy Number . . .',label_visibility ='hidden', key='input_pol_col')  
                        

                    with col3:
                        st.markdown(f"<h4 style= color: black;'> Input BSE Name </h4>", unsafe_allow_html=True)
                        bse_name = st.text_input("", placeholder = 'Input BSE Name Number . . .', label_visibility ='hidden', key = 'input_bsename_col')

                    with col4:
                        st.markdown(f"<h4 style= color: black;'> Type of Contention </h4>", unsafe_allow_html=True)
                        bse_typeselection = st.selectbox('TYPE OF CONTENTION',(
                            '',
                          'Retag BSE, BAM, BDM',
                          'Retag Branch, Area, Division, or Territory',
                          'Retag Referrer Name or Referrer Category',
                          'Change BSE Segment',
                          'Change Credit Month',
                          'Change ANP / FYP Amount',
                          'Change Production Splitting',
                          'Update Policy Status',
                          'Add Missing Policy',
                          'Remove Policy'), placeholder="Select Type of Contention...",label_visibility ='hidden', key = 'input_contype_col')
                    
                    bcol1, bcol2, bcol3, bcol4 = st.columns(4)
                    with bcol1:
                       ''
                    with bcol2:
                       ''
                    with bcol3:
                       ''
                    with bcol4:
                       clear_button = st.button("Clear Inputs", type="primary", use_container_width=True, on_click=Clear_BAMFilter)
                    
                    st.markdown(f"<h4 style= color: black;'> Contention Report </h4>", unsafe_allow_html=True)
                    df_apprv_cont = Select_BDMApproved(password, date_input[0], date_input[1], pol, bse_name, bse_typeselection).copy()
                   
                    st.dataframe(df_apprv_cont, use_container_width = True)    
                                        
                elif task == "Profiles":
                    st.write("Profile Here")
            else:
                st.error("Account does not Exist")
        else:
            st.warning("Please enter username and password")      
    
    elif choice == "TSH Login":
        username = st.sidebar.text_input("User Surname")
        password = st.sidebar.text_input("TSH CODE",type='password')
        
        if 'button' not in st.session_state:
            st.session_state.button = False
        
        scol1, scol2 = st.sidebar.columns([1,0.5])
        
        scol1.button('Login', type="primary", on_click=click_button)
        
        scol2.button('Logout', on_click=click_logout)
        
        #if st.sidebar.toggle("Login"):
        if st.session_state.button:
            # if password == '12345':
            #hashed_pswd = make_hashes(password)
            
            result = login_user(username, password, choice)
            if len(result) >=1:
                
                option_data = [
                                   {'icon': "bi bi-hand-thumbs-up", 'label':"Contention For Approval"},
                                   {'icon':"fa fa-question-circle",'label':"Approved Contention"},
                                   {'icon':"fa fa-solid fa-coffee", 'label':"Placeholder"},
                                ]
                
                # override the theme, else it will use the Streamlit applied theme
                over_theme = {'txc_inactive': 'white','menu_background':'grey','txc_active':'white','option_active':'black'}
                font_fmt = {'font-class':'h2','font-size':'150%'}     

                task = hc.option_bar(option_definition=option_data,title=' ',key='PrimaryOption',override_theme=over_theme,font_styling=font_fmt,horizontal_orientation=True)
                
                #task = st_navbar(["Contention For Approval", "Approved Contention", "Profiles"])
                # st.success("Logged In as {}".format(result['BAM FULL NAME'].loc[0]))
                    
                if task == "Contention For Approval":
                    #st.markdown(f"<h2 style='text-align: center; color: black;'>CONTENTION FORM FOR APPROVAL FOR {result['TSH FULL NAME'].loc[0]} </h2> <br>", unsafe_allow_html=True)
                    tsh_approval = contention_for_TSHApproval(password)
                    tsh_approval['IMAGE_DATA'] = tsh_approval['FILE_UPLOAD'].apply(bytes_to_base64)
                    
                    
                    # ucol1, ucol2, ucol3, ucol4, ucol5, ucol6 = st.columns([1,1.5,2.5,1,1,1])
    
                    # with ucol1:
                    #  ''
                    # with ucol2:
                    #  ''
                    # with ucol3:
                    #  ''
                    # with ucol4:
                    #  ''
                    # with ucol5:
                    #  ''
                    # with ucol6:
                    #  check_all = st.checkbox("Check All", help='Tick for Approve All')
                    
                    
                    col1, col2, col3, col4, col5, col6 = st.columns([1,1.25,1.5,1.5,.75,1])
                    
                    loop_space = 3
                    with col1:
    
                        st.markdown(f"<h4 style= color: black;'>POLICY NUMBER </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(tsh_approval)):
                            container = st.container(border=True, height=150)
                            container.write(tsh_approval.loc[i, "POLICY NUMBER"])
                            for _ in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                        
                    with col2:
                        st.markdown(f"<h4 style= color: black;'>TYPE OF CONTENTION </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(tsh_approval)):
                            container = st.container(border=True, height=150)
                            container.write(tsh_approval.loc[i, "TYPE OF CONTENTION"])
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
    
                    with col3:
                        st.markdown(f"<h4 style= color: black;'>CONTENTION DETAILS</h4> <br>", unsafe_allow_html=True)
                        for i in range(len(tsh_approval)):
                            container = st.container(border=True, height=150)
                            container.write(tsh_approval.loc[i, "CONTENTION DETAILS"])
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                            
                    with col4:
                        st.markdown(f"<h4 style= color: black;'>FILE UPLOAD </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(tsh_approval)):
                            container = st.container(border=True, height=150)
                            try:
                                container.image(Image.open(io.BytesIO(base64.b64decode(tsh_approval['IMAGE_DATA'][i]))), caption='Image', use_column_width=True)
                            except:
                                pass
                                
                    with col5:
                        st.markdown(f"<h4 style=color: black;'>ENDORSEMENT </h4> <br>", unsafe_allow_html=True)
                        approval_values = [] # To store checkbox values
                        for i in range(len(tsh_approval)):
                            container = st.container(border=True, height=150)
                            # if check_all:
                            #     radio_value = container.radio("Approve or Reject", options=["Approve", "Reject"], index=0, key=f"{i}_radiokey", help='Select Approve or Reject')
                            #     for i in range(loop_space):
                            #         container.markdown("<br>", unsafe_allow_html=True)
                            # else:
                            #     radio_value = container.radio("Approve or Reject", options=["Approve", "Reject"], index=0, key=f"{i}_radiokey", help='Select Approve or Reject')
                            #     for i in range(loop_space):
                            #         container.markdown("<br>", unsafe_allow_html=True)
                            
                            radio_value = container.radio("Approve or Reject", options=["Approve", "Reject"], index=0, key=f"{i}_radiokey", help='Select Approve or Reject')
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                            
                                   # Append the selected value as "Approve" or "Reject"
                            if radio_value == "Approve":
                                approval_values.append(True)
                            else:
                                approval_values.append(False)
                                
                    with col6:
                        comment_values = []
                        st.markdown(f"<h4 style= color: black;'> COMMENTS </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(tsh_approval)):
                            container = st.container(border=True, height=150)
                            comments_apprvr = container.text_input('Comments',placeholder="Comments", label_visibility="collapsed", key=f"{i}_container")
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                            comment_values.append(comments_apprvr)
                        
                    
                    # Add a "Submit" button
                    if st.button("Submit",):
                        # Update DataFrame with checkbox values
                        tsh_approval['TSH NEW STATUS'] = approval_values
                        tsh_approval['TSH NEW STATUS'] = np.where(tsh_approval['TSH NEW STATUS'] == True, "APPROVED", "REJECTED")
                        tsh_approval['TSH COMMENTS'] = comment_values
                        tsh_approval['BCA NEW STATUS'] = np.where(tsh_approval['TSH NEW STATUS'] == 'APPROVED', 'PENDING', 'NO ACTION NEEDED YET')
                        tsh_approval = tsh_approval[['TSH NEW STATUS', 'contention_key', 'TSH COMMENTS', 'BCA NEW STATUS']]

                        
                        for i in range(len(tsh_approval)):
                            tshnewstat = tsh_approval.loc[i, "TSH NEW STATUS"]
                            bcanewstat = tsh_approval.loc[i, "BCA NEW STATUS"]
                            contention_key = tsh_approval.loc[i, "contention_key"]
                            tshcommt = tsh_approval.loc[i, "TSH COMMENTS"]
                            tshapprvdate = datetime.now().strftime('%Y-%m-%d')
                            #st.write(bamnewstat)
                            
                            sql_query = f'''
                                        UPDATE [db_Contention].[dbo].[tbl_contention_logs]
                                        SET [TSH Approval] = '{tshnewstat}', 
                                            [TSH Comments] = '{tshcommt}', 
                                            [TSH Approved Dates] = '{tshapprvdate}',
                                            [BCA Approval] = '{bcanewstat}'
                                        WHERE [contention_key] = {contention_key}
                                    '''
                            
                            sql_update(sql_query, 'db_Contention')
                        
                        
                        time.sleep(1)
                        
                        try:
                            st.rerun()
                            st.write("Updated Successfully!")
    
                        except:
                            st.write("Updated Successfully!")
                            st.write("Refresh the Page")
                            pass
                        #st.experimental_rerun()
                        #streamlit_js_eval(js_expressions="parent.window.location.reload()")
                        
                    
                elif task == "Approved Contention":
                    #st.write('Add Analytics Here')
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"<h4 style= color: black;'> Select Contention Dates </h4>", unsafe_allow_html=True)
                        date_input = st.date_input(
                            "",
                            ((datetime.now() -  timedelta(days=7)) , datetime.now()), key = 'bse_date_col', label_visibility ='hidden'
                            )
                        
                    with col2:
                        st.markdown(f"<h4 style= color: black;'> Input Policy Number</h4>", unsafe_allow_html=True)
                        pol = st.text_input("", placeholder = 'Input Policy Number . . .', key = 'input_pol_col', label_visibility ='hidden')  
                        

                    with col3:
                        st.markdown(f"<h4 style= color: black;'> Input BSE Name </h4>", unsafe_allow_html=True)
                        bse_name = st.text_input("", placeholder = 'Input BSE Name Number . . .', key = 'input_bsename_col', label_visibility ='hidden')

                    with col4:
                        st.markdown(f"<h4 style= color: black;'> Type of Contention </h4>", unsafe_allow_html=True)
                        bse_typeselection = st.selectbox('TYPE OF CONTENTION',(
                            '',
                          'Retag BSE, BAM, BDM',
                          'Retag Branch, Area, Division, or Territory',
                          'Retag Referrer Name or Referrer Category',
                          'Change BSE Segment',
                          'Change Credit Month',
                          'Change ANP / FYP Amount',
                          'Change Production Splitting',
                          'Update Policy Status',
                          'Add Missing Policy',
                          'Remove Policy'), placeholder="Select Type of Contention...",key = 'input_contype_col', label_visibility ='hidden')
                    
                    bcol1, bcol2, bcol3, bcol4 = st.columns(4)
                    with bcol1:
                        ''
                    with bcol2:
                        ''
                    with bcol3:
                        ''
                    with bcol4:
                        clear_button = st.button("Clear Inputs", type="primary", use_container_width=True, on_click=Clear_BAMFilter)
                    
                    st.markdown(f"<h4 style= color: black;'> Contention Report </h4>", unsafe_allow_html=True)
                    df_apprv_cont = Select_TSHApproved(password, date_input[0], date_input[1], pol, bse_name, bse_typeselection).copy()
                   
                    st.dataframe(df_apprv_cont, use_container_width = True)    
                                        
                elif task == "Profiles":
                    st.write("Profile Here")
            else:
                st.error("Account does not Exist")
        else:
            st.warning("Please enter username and password")      
    
    elif choice == "BCA Login":
        username = st.sidebar.text_input("User Surname")
        password = st.sidebar.text_input("BCA CODE",type='password')
        
        if 'button' not in st.session_state:
            st.session_state.button = False
        
        scol1, scol2 = st.sidebar.columns([1,0.5])
        
        scol1.button('Login', type="primary", on_click=click_button)
        
        scol2.button('Logout', on_click=click_logout)
        
        #if st.sidebar.toggle("Login"):
        if st.session_state.button:
            # if password == '12345':
            #hashed_pswd = make_hashes(password)
            
            # result = login_user(username, password, choice)
            result = 'bcauserbcapassword'
            # if len(result) >=1:
            if username+password == result:
                
                option_data = [
                                   {'icon': "bi bi-hand-thumbs-up", 'label':"Contention For Approval"},
                                   {'icon':"fa fa-question-circle",'label':"Approved Contention"},
                                   {'icon':"fa fa-solid fa-coffee", 'label':"Placeholder"},
                                ]
                
                # override the theme, else it will use the Streamlit applied theme
                over_theme = {'txc_inactive': 'white','menu_background':'grey','txc_active':'white','option_active':'black'}
                font_fmt = {'font-class':'h2','font-size':'150%'}       

                task = hc.option_bar(option_definition=option_data,title=' ',key='PrimaryOption',override_theme=over_theme,font_styling=font_fmt,horizontal_orientation=True)
                
                #task = st_navbar(["Contention For Approval", "Approved Contention", "Profiles"])
                # st.success("Logged In as {}".format(result['BAM FULL NAME'].loc[0]))
                    
                if task == "Contention For Approval":
                    #st.markdown(f"<h2 style='text-align: center; color: black;'>CONTENTION FORM FOR APPROVAL FOR BCA </h2> <br>", unsafe_allow_html=True)
                    bca_approval = contention_for_BCAApproval()
                    bca_approval['IMAGE_DATA'] = bca_approval['FILE_UPLOAD'].apply(bytes_to_base64)
                    
                    
                    # ucol1, ucol2, ucol3, ucol4, ucol5, ucol6 = st.columns([1,1.5,2.5,1,1,1])
    
                    # with ucol1:
                    #  ''
                    # with ucol2:
                    #  ''
                    # with ucol3:
                    #  ''
                    # with ucol4:
                    #  ''
                    # with ucol5:
                    #  ''
                    # with ucol6:
                    #  check_all = st.checkbox("Check All", help='Tick for Approve All')
                    
                    
                    col1, col2, col3, col4, col5, col6 = st.columns([1,1.25,1.5,1.5,.75,1])
                    
                    loop_space = 3
                    with col1:
    
                        st.markdown(f"<h4 style= color: black;'>POLICY NUMBER </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bca_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bca_approval.loc[i, "POLICY NUMBER"])
                            for _ in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                        
                    with col2:
                        st.markdown(f"<h4 style= color: black;'>TYPE OF CONTENTION </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bca_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bca_approval.loc[i, "TYPE OF CONTENTION"])
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
    
                    with col3:
                        st.markdown(f"<h4 style= color: black;'>CONTENTION DETAILS</h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bca_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bca_approval.loc[i, "CONTENTION DETAILS"])
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                            
                    with col4:
                        st.markdown(f"<h4 style= color: black;'>FILE UPLOAD </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bca_approval)):
                            container = st.container(border=True, height=150)
                            try:
                                container.image(Image.open(io.BytesIO(base64.b64decode(bca_approval['IMAGE_DATA'][i]))), caption='Image', use_column_width=True)
                            except:
                                pass
                                
                    with col5:
                        st.markdown(f"<h4 style=color: black;'>ENDORSEMENT </h4> <br>", unsafe_allow_html=True)
                        approval_values = [] # To store checkbox values
                        for i in range(len(bca_approval)):
                            container = st.container(border=True, height=150)
                            # if check_all:
                            #     radio_value = container.radio("Approve or Reject", options=["Approve", "Reject"], index=0, key=f"{i}_radiokey", help='Select Approve or Reject')
                            #     for i in range(loop_space):
                            #         container.markdown("<br>", unsafe_allow_html=True)
                            # else:
                            #     radio_value = container.radio("Approve or Reject", options=["Approve", "Reject"], index=0, key=f"{i}_radiokey", help='Select Approve or Reject')
                            #     for i in range(loop_space):
                            #         container.markdown("<br>", unsafe_allow_html=True)

                            radio_value = container.radio("Approve or Reject", options=["Approve", "Reject"], index=0, key=f"{i}_radiokey", help='Select Approve or Reject')
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                                    
                                   # Append the selected value as "Approve" or "Reject"
                            if radio_value == "Approve":
                                approval_values.append(True)
                            else:
                                approval_values.append(False)
                    
                    with col6:
                        comment_values = []
                        st.markdown(f"<h4 style= color: black;'> COMMENTS </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bca_approval)):
                            container = st.container(border=True, height=150)
                            comments_apprvr = container.text_input('Comments',placeholder="Comments", label_visibility="collapsed", key=f"{i}_container")
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                            comment_values.append(comments_apprvr)
                        
                    
                    # Add a "Submit" button
                    if st.button("Submit",):
                        # Update DataFrame with checkbox values
                        bca_approval['BCA NEW STATUS'] = approval_values
                        bca_approval['BCA NEW STATUS'] = np.where(bca_approval['BCA NEW STATUS'] == True, "APPROVED", "REJECTED")
                        bca_approval['BCA COMMENTS'] = comment_values
                        #bca_approval['FINAL STATUS'] = np.where(bca_approval['TSH NEW STATUS'] == 'APPROVED', 'PENDING', 'NO ACTION NEEDED YET')
                        bca_approval = bca_approval[['BCA NEW STATUS', 'contention_key', 'BCA COMMENTS']]

                        
                        for i in range(len(bca_approval)):
                            bcanewstat = bca_approval.loc[i, "BCA NEW STATUS"]
                            contention_key = bca_approval.loc[i, "contention_key"]
                            bcacommt = bca_approval.loc[i, "BCA COMMENTS"]
                            bcaapprvdate = datetime.now().strftime('%Y-%m-%d')
                            #st.write(bamnewstat)
                            
                            sql_query = f'''
                                        UPDATE [db_Contention].[dbo].[tbl_contention_logs]
                                        SET [BCA Approval] = '{bcanewstat}', 
                                            [BCA Comments] = '{bcacommt}', 
                                            [BCA Approved Dates] = '{bcaapprvdate}'
                                        WHERE [contention_key] = {contention_key}
                                    '''
                            
                            sql_update(sql_query, 'db_Contention')
                        
                        
                        time.sleep(1)
                        
                        try:
                            st.rerun()
                            st.write("Updated Successfully!")
    
                        except:
                            st.write("Updated Successfully!")
                            st.write("Refresh the Page")
                            pass
                        #st.experimental_rerun()
                        #streamlit_js_eval(js_expressions="parent.window.location.reload()")
                        
                    
                elif task == "Approved Contention":
                    #st.write('Add Analytics Here')
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"<h4 style= color: black;'> Select Contention Dates </h4>", unsafe_allow_html=True)
                        date_input = st.date_input(
                            "",
                            ((datetime.now() -  timedelta(days=7)) , datetime.now()), key = 'bse_date_col', label_visibility ='hidden'
                            )
                        
                    with col2:
                        st.markdown(f"<h4 style= color: black;'> Input Policy Number</h4>", unsafe_allow_html=True)
                        pol = st.text_input("", placeholder = 'Input Policy Number . . .', key = 'input_pol_col', label_visibility ='hidden')  
                        

                    with col3:
                        st.markdown(f"<h4 style= color: black;'> Input BSE Name </h4>", unsafe_allow_html=True)
                        bse_name = st.text_input("", placeholder = 'Input BSE Name Number . . .', key = 'input_bsename_col', label_visibility ='hidden')

                    with col4:
                        st.markdown(f"<h4 style= color: black;'> Type of Contention </h4>", unsafe_allow_html=True)
                        bse_typeselection = st.selectbox('TYPE OF CONTENTION',(
                            '',
                          'Retag BSE, BAM, BDM',
                          'Retag Branch, Area, Division, or Territory',
                          'Retag Referrer Name or Referrer Category',
                          'Change BSE Segment',
                          'Change Credit Month',
                          'Change ANP / FYP Amount',
                          'Change Production Splitting',
                          'Update Policy Status',
                          'Add Missing Policy',
                          'Remove Policy'), placeholder="Select Type of Contention...",key = 'input_contype_col', label_visibility ='hidden')
                    
                    bcol1, bcol2, bcol3, bcol4 = st.columns(4)
                    with bcol1:
                        ''
                    with bcol2:
                        ''
                    with bcol3:
                        ''
                    with bcol4:
                        clear_button = st.button("Clear Inputs", type="primary", use_container_width=True, on_click=Clear_BAMFilter)
                    
                    st.markdown(f"<h4 style= color: black;'> Contention Report </h4>", unsafe_allow_html=True)
                    df_apprv_cont = Select_BCAApproved(date_input[0], date_input[1], pol, bse_name, bse_typeselection).copy()
                   
                    st.dataframe(df_apprv_cont, use_container_width = True)    
                                        
                elif task == "Profiles":
                    st.write("Profile Here")
            else:
                st.error("Account does not Exist")
        else:
            st.warning("Please enter username and password")      
            
    elif choice == "BAS Login":
        username = st.sidebar.text_input("User Surname")
        password = st.sidebar.text_input("BAS CODE",type='password')
        
        if 'button' not in st.session_state:
            st.session_state.button = False
        
        scol1, scol2 = st.sidebar.columns([1,0.5])
        
        scol1.button('Login', type="primary", on_click=click_button)
        
        scol2.button('Logout', on_click=click_logout)
        
        #if st.sidebar.toggle("Login"):
        if st.session_state.button:
 
            result = 'basuserbaspassword'
            
            if username+password == result:
                option_data = [
                                   {'icon': "bi bi-hand-thumbs-up", 'label':"Contention For Approval"},
                                   {'icon':"fa fa-question-circle",'label':"Approved Contention"},
                                   {'icon':"fa fa-solid fa-coffee", 'label':"Profiles"},
                                ]
                
                # override the theme, else it will use the Streamlit applied theme
                over_theme = {'txc_inactive': 'white','menu_background':'grey','txc_active':'white','option_active':'black'}
                font_fmt = {'font-class':'h2','font-size':'150%'}    
                
                task = hc.option_bar(option_definition=option_data,title=' ',key='PrimaryOption',override_theme=over_theme,font_styling=font_fmt,horizontal_orientation=True)

                #task = st_navbar(["Contention For Approval", "Approved Contention", "Profiles"])
                # st.success("Logged In as {}".format(result['BAM FULL NAME'].loc[0]))
                    
                if task == "Contention For Approval":
                    
                    #st.markdown(f"<h2 style='text-align: center; color: black;'>CONTENTION FORM FOR APPROVAL FOR BAS </h2> <br>", unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"<h4 style= color: black;'> Input Policy Number</h4>", unsafe_allow_html=True)
                        pol = st.text_input("", placeholder = 'Input Policy Number . . .')  
                        
                    with col2:
                        st.markdown(f"<h4 style= color: black;'> Select Contention Dates </h4>", unsafe_allow_html=True)
                        date_input = st.date_input(
                            "",
                            ((datetime.now() -  timedelta(days=7)) , datetime.now())
                            )
                    
                    st.markdown('<br>', unsafe_allow_html=True)
                    
                    bas_approval = contention_for_BASApproval(date_input[0], date_input[1], pol)
                    
                    bas_approval['IMAGE_DATA'] = bas_approval['FILE_UPLOAD'].apply(bytes_to_base64)
                    
                    col1, col2, col3, col4, col5 = st.columns([1,1.25,1.5,1.5,1.75])
                    
                    loop_space = 3
                    with col1:
    
                        st.markdown(f"<h4 style= color: black;'>POLICY NUMBER </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bas_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bas_approval.loc[i, "POLICY NUMBER"])
                            for _ in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                        
                    with col2:
                        st.markdown(f"<h4 style= color: black;'>TYPE OF CONTENTION </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bas_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bas_approval.loc[i, "TYPE OF CONTENTION"])
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
    
                    with col3:
                        st.markdown(f"<h4 style= color: black;'>CONTENTION DETAILS</h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bas_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bas_approval.loc[i, "CONTENTION DETAILS"])
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                            
                    with col4:
                        st.markdown(f"<h4 style= color: black;'>FILE UPLOAD </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bas_approval)):
                            container = st.container(border=True, height=150)
                            try:
                                container.image(Image.open(io.BytesIO(base64.b64decode(bas_approval['IMAGE_DATA'][i]))), caption='Image', use_column_width=True)
                            except:
                                pass
                    
                    with col5:
                        comment_values = []
                        st.markdown(f"<h4 style= color: black;'> COMMENTS </h4> <br>", unsafe_allow_html=True)
                        for i in range(len(bas_approval)):
                            container = st.container(border=True, height=150)
                            comments_apprvr = container.text_input('Comments',placeholder=bas_approval.loc[i, "BAS Comment"], label_visibility="collapsed", key=f"{i}_container")
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                            comment_values.append(comments_apprvr)
                        

                    # Add a "Submit" button
                    if st.button("Submit",):
                        # Update DataFrame with checkbox values
                        bas_approval['BAS COMMENTS'] = comment_values
                        #bas_approval['FINAL STATUS'] = np.where(bca_approval['TSH NEW STATUS'] == 'APPROVED', 'PENDING', 'NO ACTION NEEDED YET')
                        bas_approval = bas_approval[['contention_key', 'BAS COMMENTS']]

                        
                        for i in range(len(bas_approval)):
                            contention_key = bas_approval.loc[i, "contention_key"]
                            bascommt = bas_approval.loc[i, "BAS COMMENTS"]
                            #st.write(bamnewstat)
                            
                            sql_query = f'''
                                        UPDATE [db_Contention].[dbo].[tbl_contention_logs]
                                        SET [BAS Comment] = '{bascommt}'
                                        WHERE [contention_key] = {contention_key}
                                    '''
                            
                            sql_update(sql_query, 'db_Contention')
                        
                        
                        time.sleep(1)
                        
                        try:
                            st.rerun()
                            st.write("Updated Successfully!")
    
                        except:
                            st.write("Updated Successfully!")
                            st.write("Refresh the Page")
                            pass
                        #st.experimental_rerun()
                        #streamlit_js_eval(js_expressions="parent.window.location.reload()")
                        
                    
                elif task == "Approved Contention":
                    #st.write('Add Analytics Here')
                    # col1, col2 = st.columns(2)
                    
                    # with col1:
                    #     st.markdown(f"<h2 style= color: black;'> Input Policy Number</h2>", unsafe_allow_html=True)
                    #     pol = st.text_input("", placeholder = 'Input Policy Number . . .')  
                        
                    # with col2:
                    #     st.markdown(f"<h2 style= color: black;'> Select Contention Dates </h2>", unsafe_allow_html=True)
                    #     date_input = st.date_input(
                    #         "",
                    #         ((datetime.now() -  timedelta(days=7)) , datetime.now())
                    #         )
                    
                    # st.markdown('<br>', unsafe_allow_html=True)
                        
                    # df_apprv_cont = Select_BASApproved(date_input[0], date_input[1], pol)
                    # st.dataframe(df_apprv_cont, hide_index=True, use_container_width = True)
                    
                    st.markdown(f"<h2 style='text-align: center; color: black;'>CONTENTION FORM FOR APPROVAL FOR BAS </h2> <br>", unsafe_allow_html=True)

                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"<h4 style= color: black;'> Select Contention Dates </h4>", unsafe_allow_html=True)
                        date_input = st.date_input(
                            "",
                            ((datetime.now() -  timedelta(days=7)) , datetime.now()), key = 'bse_date_col', label_visibility ='hidden'
                            )
                        
                    with col2:
                        st.markdown(f"<h4 style= color: black;'> Input Policy Number</h4>", unsafe_allow_html=True)
                        pol = st.text_input("", placeholder = 'Input Policy Number . . .', key = 'input_pol_col', label_visibility ='hidden')  
                        

                    with col3:
                        st.markdown(f"<h4 style= color: black;'> Input BSE Name </h4>", unsafe_allow_html=True)
                        bse_name = st.text_input("", placeholder = 'Input BSE Name Number . . .', key = 'input_bsename_col', label_visibility ='hidden')

                    with col4:
                        st.markdown(f"<h4 style= color: black;'> Type of Contention </h4>", unsafe_allow_html=True)
                        bse_typeselection = st.selectbox('TYPE OF CONTENTION',(
                            '',
                          'Retag BSE, BAM, BDM',
                          'Retag Branch, Area, Division, or Territory',
                          'Retag Referrer Name or Referrer Category',
                          'Change BSE Segment',
                          'Change Credit Month',
                          'Change ANP / FYP Amount',
                          'Change Production Splitting',
                          'Update Policy Status',
                          'Add Missing Policy',
                          'Remove Policy'), placeholder="Select Type of Contention...",key = 'input_contype_col', label_visibility ='hidden')

                    
                    bcol1, bcol2, bcol3, bcol4 = st.columns(4)
                    with bcol1:
                        ''
                    with bcol2:
                        ''
                    with bcol3:
                        ''
                    with bcol4:
                       clear_button = st.button("Clear Inputs", type="primary", use_container_width=True, on_click=Clear_BAMFilter)
                    st.markdown('<br>', unsafe_allow_html=True)
                    
                    bas_approval = Select_BASApproved(date_input[0], date_input[1], pol, bse_name, bse_typeselection)
                    
                    bas_approval['IMAGE_DATA'] = bas_approval['FILE_UPLOAD'].apply(bytes_to_base64)
                    
                    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
                    
                    loop_space = 3
                    
                    with col1:
    
                        st.markdown(f"<h5 style= color: black;'>BSE SUBMIT DATE </h5> <br>", unsafe_allow_html=True)
                        for i in range(len(bas_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bas_approval.loc[i, "Date Submit"])
                            for _ in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                    
                    with col2:
    
                        st.markdown(f"<h5 style= color: black;'>POLICY NUMBER </h5> <br>", unsafe_allow_html=True)
                        for i in range(len(bas_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bas_approval.loc[i, "POLICY NUMBER"])
                            for _ in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                                
                    with col3:
                         st.markdown(f"<h5 style= color: black;'>BSE NAME</h5> <br>", unsafe_allow_html=True)
                         for i in range(len(bas_approval)):
                             container = st.container(border=True, height=150)
                             container.write(bas_approval.loc[i, "BSE NAME"])
                             for i in range(loop_space):
                                 container.markdown("<br>", unsafe_allow_html=True)
                        
                    with col4:
                        st.markdown(f"<h5 style= color: black;'>TYPE OF CONTENTION </h5> <br>", unsafe_allow_html=True)
                        for i in range(len(bas_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bas_approval.loc[i, "TYPE OF CONTENTION"])
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
    
                    with col5:
                        st.markdown(f"<h5 style= color: black;'>CONTENTION DETAILS</h5> <br>", unsafe_allow_html=True)
                        for i in range(len(bas_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bas_approval.loc[i, "CONTENTION DETAILS"])
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                            
                    with col6:
                        st.markdown(f"<h5 style= color: black;'>FILE UPLOAD </h5> <br>", unsafe_allow_html=True)
                        for i in range(len(bas_approval)):
                            container = st.container(border=True, height=150)
                            try:
                                container.image(Image.open(io.BytesIO(base64.b64decode(bas_approval['IMAGE_DATA'][i]))), caption='Image', use_column_width=True)
                            except:
                                pass
                    
                    with col7:
                        st.markdown(f"<h5 style= color: black;'>BCA SUBMIT DATE </h5> <br>", unsafe_allow_html=True)
                        for i in range(len(bas_approval)):
                            container = st.container(border=True, height=150)
                            container.write(bas_approval.loc[i, "BCA Approved Dates"])
                            for _ in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                    
                    with col8:
                        comment_values = []
                        st.markdown(f"<h5 style= color: black;'> EFFECTIVE DATE </h5> <br>", unsafe_allow_html=True)
                        for i in range(len(bas_approval)):
                            container = st.container(border=True, height=150)
                            comments_apprvr = container.write(bas_approval.loc[i, "EFFECTIVE DATE"], label_visibility="collapsed", key=f"{i}_container")
                            for i in range(loop_space):
                                container.markdown("<br>", unsafe_allow_html=True)
                            comment_values.append(comments_apprvr)
                                        
                elif task == "Profiles":
                    st.write("Profile Here")
            else:
                st.error("Account does not Exist")
        else:
            st.warning("Please enter username and password")     

    return menu

        
if __name__ == '__main__':
    # main()
    try:
        main()
    except Exception as e:
        st.write("Incomplete or Improper Data Input")
        print(e)
