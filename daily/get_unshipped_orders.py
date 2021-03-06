#!/usr/bin/python3
#init path
import os,time,shutil,configparser,requests,random,codecs
from app.local import newlocal
from mws import mws
import csv



root_path=os.path.split(os.path.abspath(__file__))[0]+'/'
root_path=root_path.replace('\\','/')
reports_dir_path=newlocal.get_path(root_path,['src','reports'])
orders_dir_path=newlocal.get_path(root_path,['src','orders'])
mws_config_path=newlocal.get_path(root_path,['app','config'])+'mwsconfig.ini'
config_path=newlocal.get_path(root_path,['app','config'])+'config.ini'
#market_place_ids
market_place_ids={'UK':'A1F83G8C2ARO7P',
    'FR':'A13V1IB3VIYZZH',
    'DE':'A1PA6795UKMFR9',
    'IT':'APJ6JRA9NG5V4',
    'ES':'A1RKKUPIHCS9HS',
    'US':'ATVPDKIKX0DER'}
# get mws info
mwsconfig=configparser.ConfigParser()
mwsconfig.read(mws_config_path)
access_key=mwsconfig.get('mws','aws_access_key')
secret_key=mwsconfig.get('mws','aws_secret_key')
account_id=mwsconfig.get('mws','seller_id')
# get info
config=configparser.ConfigParser()
config.read(config_path)
days=int(config.get('info','days'))
region=config.get('info','region').upper()
market_place_id=market_place_ids.get(region)
account_num=config.get('info','accountnum').upper()
# print(access_key,secret_key,account_id,region)
Reports_client=mws.Reports(access_key,secret_key,account_id,region,domain='', uri="", version="", auth_token="")
# print(dir(Orders_client))

def get_unshipped_orders():

	orders_file_name=time.strftime("%Y-%m-%d",time.localtime())+region.lower()+'-unshipped.txt'
	orders_file_path=orders_dir_path+orders_file_name
	# orders=Orders_client.list_orders(marketplaceids=[market_place_id,],created_after=created_after, created_before=created_before, lastupdatedafter=None, lastupdatedbefore=None, orderstatus=(), fulfillment_channels=(), payment_methods=(), buyer_email=None, seller_orderid=None, max_results='100')
	# report_type='_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_'
	# report_type='_GET_FLAT_FILE_ORDERS_DATA_'
	report_type='_GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_'
	report_list=Reports_client.get_report_list(requestids=(), max_count=None, types=(report_type,), acknowledged=None,
							fromdate=None, todate=None)
							
	print(report_list)
	try:
		first_report=report_list.parsed['ReportInfo'][0]
		report_time=first_report['AvailableDate']['value']
	except:
		report_time='0'
	date_format="%Y-%m-%dT%H:%M:%SZ"
	created_before=time.strftime(date_format,time.gmtime())
	created_after=time.strftime(date_format,time.gmtime(time.time()-3600*24*days))
	acceptable_time=time.strftime(date_format,time.gmtime(time.time()-100))
	print(report_time,acceptable_time)
	if report_time<acceptable_time:
		Reports_client.request_report(report_type, start_date=None, end_date=None, marketplaceids=())
	while report_time<acceptable_time:
		time.sleep(30)
		report_list=Reports_client.get_report_list(requestids=(), max_count=None, types=(report_type,), acknowledged=None,
								fromdate=None, todate=None)
		print(report_list)
		try:
			first_report=report_list.parsed['ReportInfo'][0]
			report_time=first_report['AvailableDate']['value']
		except:
			print('wating for report...')
			report_time='0'
		print(report_time)
	report_id=first_report['ReportId']['value']
	print(report_id)
	report=Reports_client.get_report(report_id)
	content=report.parsed
	with open(orders_file_path,'w') as f:
		f.write(codecs.decode(content,'utf8','ignore').replace('\r\n','\n'))

	return orders_file_path


 #because some unshipped order is not need to confirm
def needconfirmorder(unshippedorder_file,carrier_code):

    unshippedorder = open(unshippedorder_file, 'r' ,encoding='utf-8',errors='ignore')
    file_read = csv.reader(unshippedorder, delimiter = '\t')
    csv_file=orders_dir_path+time.strftime("%Y-%m-%d",time.localtime())+'_'+account_num.lower()+region.lower()+'_needconfirm.txt'
    fcsv=open(csv_file, 'wt', newline='')
    out_csv = csv.writer(fcsv,delimiter = '\t')
    headers = next(file_read)

    headersnew=['order-id','Ship Date','carrier-code']
    out_csv.writerow(headersnew)
    for row in file_read:

    	if int(row[6])<=-1:
    		newrow=[row[0],time.strftime("%Y-%m-%d",time.localtime()),carrier_code]
    		out_csv.writerow(newrow)


    unshippedorder.close()
    return csv_file

    #return confirmorder_file

filedir=get_unshipped_orders()
#filedir=orders_dir_path+'2016-07-06ca-unshipped.txt'
#print "Please type in your carrier code"
carrier_code=input("Please type in your carrier code: ")
print(carrier_code)
needconfirmorder(filedir,carrier_code)
