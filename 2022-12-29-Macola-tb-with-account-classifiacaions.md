{
 "cells": [
 {
 "cell_type": "code",
 "execution_count": 1,
 "id": "409493d9",
 "metadata": {},
 "outputs": [],
 "source": [
 "#Macola TB to Excel with classifications\n",
 "#In this post, we convert the Macola trial balance to a workable format and assign classifications to accounts as maintained\n",
 "#by the library classifications excel file by Financial Reporting unit"
 ]
 },
 {
 "cell_type": "code",
 "execution_count": 3,
 "id": "2a377703",
 "metadata": {},
 "outputs": [],
 "source": [
 "#Copy and paste contents from the legacy system in the form of a text file into an excel sheet\n",
 "#Insert a \"header\" line at the top of the file and name it \"description\" (At this point all contents of the TB \n",
 "#raw file should be contained in a single column of an excel document (column \"A\") called \"description\" )\n",
 "\n",
 "#Read the excel file from its saved location and save to a variable (dataframe)\n",
 "tb=pd.read_excel('insert file_path/directory')"
 ]
 },
 {
 "cell_type": "code",
 "execution_count": null,
 "id": "12019548",
 "metadata": {},
 "outputs": [],
 "source": [
 "#The following lines of code transform the Macola file into separate columns and drops all unnecessary lines\n",
 "tb[['Account_num','Account_desc']]=tb['description'].str.extract('(\\d{7}\\-\\d{2}\\-\\d{6})\\s+(.*)')\n",
 "tb['Account_num']=tb['Account_num'].ffill()\n",
 "tb['Account_desc']=tb['Account_desc'].ffill()\n",
 "tb['Account_total']=tb['description'].str.extract('Account Total:(.*)')\n",
 "tb_=tb['Account_total'].dropna()\n",
 "tb_=pd.merge(tb_,tb)\n",
 "tb_1=tb_['Account_total'].str.split('\\s+', expand=True).iloc[:,1:]\n",
 "tb_1.columns=['Beg_bal','Total_cr','Total_db','Net_ch','Ending_bal']\n",
 "tb_=tb_.join(tb_1)\n",
 "tb_=tb_.drop(['Account_total','description'],axis=1)\n",
 "tb_=tb_.drop_duplicates()"
 ]
 },
 {
 "cell_type": "code",
 "execution_count": null,
 "id": "da07cf6a",
 "metadata": {},
 "outputs": [],
 "source": [
 "#Convert balances ending with 'CR' to negative values and sum each column to ensure balances are correct\n",
 "mask = tb_['Beg_bal'].str.endswith('CR')\n",
 "tb_.loc[mask, 'Beg_bal'] = '-' + tb_.loc[mask, 'Beg_bal'].str[:-2]\n",
 "tb_['Beg_bal']=tb_['Beg_bal'].str.replace(',','')\n",
 "tb_['Beg_bal']=tb_['Beg_bal'].astype(float)\n",
 "sum=tb_['Beg_bal'].sum() \n",
 "\n",
 "mask = tb_['Total_cr'].str.endswith('CR')\n",
 "tb_.loc[mask, 'Total_cr'] = '-' + tb_.loc[mask, 'Total_cr'].str[:-2]\n",
 "tb_['Total_cr']=tb_['Total_cr'].str.replace(',','')\n",
 "tb_['Total_cr']=tb_['Total_cr'].astype(float)\n",
 "sum=tb_['Total_cr'].sum() \n",
 "\n",
 "mask = tb_['Total_db'].str.endswith('CR')\n",
 "tb_.loc[mask, 'Total_db'] = '-' + tb_.loc[mask, 'Total_db'].str[:-2]\n",
 "tb_['Total_db']=tb_['Total_db'].str.replace(',','')\n",
 "tb_['Total_db']=tb_['Total_db'].astype(float)\n",
 "sum=tb_['Total_db'].sum() \n",
 "\n",
 "mask = tb_['Net_ch'].str.endswith('CR')\n",
 "tb_.loc[mask, 'Net_ch'] = '-' + tb_.loc[mask, 'Net_ch'].str[:-2]\n",
 "tb_['Net_ch']=tb_['Net_ch'].str.replace(',','')\n",
 "tb_['Net_ch']=tb_['Net_ch'].astype(float)\n",
 "sum=tb_['Net_ch'].sum() \n",
 "\n",
 "mask = tb_['Ending_bal'].str.endswith('CR')\n",
 "tb_.loc[mask, 'Ending_bal'] = '-' + tb_.loc[mask, 'Ending_bal'].str[:-2]\n",
 "tb_['Ending_bal']=tb_['Ending_bal'].str.replace(',','')\n",
 "tb_['Ending_bal']=tb_['Ending_bal'].astype(float)\n",
 "sum=tb_['Ending_bal'].sum() "
 ]
 },
 {
 "cell_type": "code",
 "execution_count": null,
 "id": "66aa6b74",
 "metadata": {},
 "outputs": [],
 "source": [
 "tb_.rename(columns={'Account_num':'Account_num_original'},inplace=True)\n",
 "tb_['Account_num']=tb_['Account_num_original'].str[1:]\n"
 ]
 },
 {
 "cell_type": "markdown",
 "id": "36b47043",
 "metadata": {},
 "source": [
 "Define the location of the classifications library - where is the map library located?"
 ]
 },
 {
 "cell_type": "code",
 "execution_count": null,
 "id": "fd7fbd3f",
 "metadata": {},
 "outputs": [],
 "source": [
 "library_path='enter path of the library classifications.xlsx' # Name the sheet with the QPP account classifications as \"QPP\" and \"TDA\" with the TDA account classifications\n",
 "df=pd.read_excel(library_path,sheet_name='qpp', keep_default_na=False)\n"
 ]
 },
 {
 "cell_type": "code",
 "execution_count": null,
 "id": "5ca4b0bf",
 "metadata": {},
 "outputs": [],
 "source": [
 "#Assign tb_ from above to macola_gl\n",
 "macola_gl=tb_"
 ]
 },
 {
 "cell_type": "code",
 "execution_count": null,
 "id": "df33c661",
 "metadata": {},
 "outputs": [],
 "source": [
 "#Assign categores based on last six fiscal years and check for any discrepancies/inconsistencies between the account classifications accross the years\n",
 "list=[2018,2019,2020,2021,2022,2023]\n",
 "df=df.loc[df['Year'].isin(list)]\n",
 "df_group=df.groupby('Account_num')['Description 5'].nunique()\n",
 "df_group_s=df_group>1\n",
 "df_group=df_group.loc[df_group_s].reset_index()\n",
 "df_loc=df.loc[df['Account_num'].isin(df_group['Account_num'])]\n",
 "df_loc['Account_num'].nunique()"
 ]
 },
 {
 "cell_type": "code",
 "execution_count": null,
 "id": "90dd3a79",
 "metadata": {},
 "outputs": [],
 "source": [
 "#drop duplicates over ['Account_num','Acct_desc','New_map','Description 1','Description 2','Description 3','Description 4'], sort accts first\n",
 "df=df.sort_values(by=['Account_num','Year'])\n",
 "df_no_dups=df.drop_duplicates(subset=['Type','Account_num','New_map','Description 1','Description 2','Description 3','Description 4'],keep='last')"
 ]
 },
 {
 "cell_type": "code",
 "execution_count": null,
 "id": "e04ed7f8",
 "metadata": {},
 "outputs": [],
 "source": [
 "#perform the merge between the gl from Macola (already in Excel and the library classifications file, the resulting output is named \"tb_merged\")\n",
 "#export this file into an excel workbook, see below - last line\n",
 "\n",
 "\n",
 "\n",
 "tb_merged=pd.merge(macola_gl,df_no_dups,on='Account_num',how='left').reset_index()\n",
 "\n",
 "tb_merged['var_num']=tb_merged['Account_num'].str.extract('\\-(\\d{2})\\-')\n",
 "tb_merged['var_num']=tb_merged['var_num'].astype(int)\n",
 "\n",
 "#assign Fund column name for QPP\n",
 "def assign_var_type(x):\n",
 " if x['var_num']== 11:\n",
 " var_type = 'FX'\n",
 " return var_type\n",
 " elif x['var_num'] == 12:\n",
 " var_type = 'VA'\n",
 " return var_type\n",
 " elif x['var_num']== 13:\n",
 " var_type = 'VB'\n",
 " return var_type\n",
 " elif x['var_num']== 14:\n",
 " var_type = 'VC'\n",
 " return var_type\n",
 " elif x['var_num']== 15:\n",
 " var_type = 'VD'\n",
 " return var_type\n",
 " elif x['var_num']== 16:\n",
 " var_type = 'VE'\n",
 " return var_type\n",
 " elif x['var_num']== 17:\n",
 " var_type = 'VF'\n",
 " return var_type\n",
 " elif x['var_num']== 18:\n",
 " var_type = 'VG'\n",
 " return var_type\n",
 " \n",
 " else:\n",
 " return 0\n",
 "\n",
 "tb_merged['Fund_name']=tb_merged.apply(assign_var_type,axis=1)\n",
 "\n",
 "tb_merged['Description 1']=tb_merged['Description 1'].fillna('not_reviewed')\n",
 "tb_merged['Fund_name']=np.where(tb_merged['Description 1'].str.contains('TDA Investment'),'TDA'+' '+tb_merged['Fund_name'],tb_merged['Fund_name'])\n",
 "\n",
 "columns=['Type','Fund_name','var_num','status','Year','Account_num','Account_desc','Beg_bal','Total_cr','Total_db','Net_ch','Ending_bal',\\\n",
 " 'New_map','Description 1','Description 2','Description 3','Description 4','Description 5','Description 6','Description 7','Actuarial Accounts']\n",
 "\n",
 "\n",
 "tb_merged=tb_merged[columns]\n",
 "\n",
 "tb_merged.to_excel(\"G:/specify the location where this output file should be stored\")"
 ]
 }
 ],
 "metadata": {
 "kernelspec": {
 "display_name": "Python 3 (ipykernel)",
 "language": "python",
 "name": "python3"
 },
 "language_info": {
 "codemirror_mode": {
 "name": "ipython",
 "version": 3
 },
 "file_extension": ".py",
 "mimetype": "text/x-python",
 "name": "python",
 "nbconvert_exporter": "python",
 "pygments_lexer": "ipython3",
 "version": "3.9.7"
 }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
