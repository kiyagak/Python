from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
from mysql.connector import errorcode
import json




# replace with your own MySQL database name, username, and password
db_name = "your_db_name"
user = "your_user_name"
password = "your_password"


# function to query the database for a table's result set,
# sorted by date in descending order
def select_order_date(table, publication):
	cnx = mysql.connector.connect(user=user,
		password=password,
		database=db_name,
		port=3306)
	cursor = cnx.cursor(buffered=True)
	
	dbTblName = db_name + "." + table

	query = ("SELECT * FROM " + dbTblName + 
		" WHERE PUBLICATION = \"" + publication + "\""
		" ORDER BY DATEPUB DESC;")
	
	cursor.execute(query)
	
	result_set = cursor.fetchall()
	
	if len(result_set) == 0:
		return None
	else:
		return result_set[0]

# function to create a table
def create_table(table):
	cnx = mysql.connector.connect(user=user,
		password=password,
		database=db_name,
		port=3306)
	cursor = cnx.cursor(buffered=True)
	
	dbTblName = db_name + "." + table

	stmt = (
		"CREATE TABLE IF NOT EXISTS " + dbTblName + # made only if the table doesn't exist
		"(ARTICLE_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY," # primary key column
		"DATEPUB DATE,"
		"PUBLICATION TEXT,"
		"TITLE TEXT,"
		"LINK TEXT NOT NULL,"
		"UNIQUE (LINK(767)));" # unique constraint to prevent storage of duplicate links
		)
	
	# deletes all records dates before 2 weeks ago
	del_stmt = ("DELETE FROM " + dbTblName + " WHERE DATEPUB < DATE(NOW() - INTERVAL 14 DAY)")
	
	cursor.execute(stmt)
	cursor.execute(del_stmt)
	cnx.commit()
	cnx.close()
	
	print(table + " has successfully been created in the " + db_name + " database.  ")
	
def insert(table, publication, DATEPUB, title, LINK):
	cnx = mysql.connector.connect(user=user,
		password=password,
		database=db_name,
		port=3306)
	cursor = cnx.cursor(buffered=True)
		
	dbTblName = db_name + "." + table
	
	# statement that inserts records without adding records with duplicate links
	insert_entry = ("INSERT IGNORE INTO " + dbTblName + " "
				   "(PUBLICATION, DATEPUB, TITLE, LINK) "
				   "VALUES (%(PUBLICATION)s, %(DATEPUB)s, %(TITLE)s, %(LINK)s)")
	
	# JSON object containing values to be inserted in their appropriate column
	data_entry = {
	'PUBLICATION': publication, 
	'DATEPUB': DATEPUB, 
	'TITLE': title, 
	'LINK': LINK,
	}

	# execute insert statement
	cursor.execute(insert_entry, data_entry)
	cnx.commit()

	print("Records have successfully been inserted.  ")

create_table("tbl_name")
insert(
	"tbl_name",
	"Source Site", 
	datetime.now().strftime("%Y-%m-%d"), 
	"A Headline", 
	"https://www.google.com/"
)

result_set = select_order_date("tbl_name", "Source Site")

#create JSON object to contain the query results
json_result_set = {}

# create keys for each column from the SQL query result set
# assign the column records to their appropriate key
json_result_set['article_id'] = result_set[0]
json_result_set['date'] = str(result_set[1])
json_result_set['publication'] = result_set[2]
json_result_set['headline'] = result_set[3]
json_result_set['link'] = result_set[4]

print()
print("Below is the result set of the database query in JSON form:  ")
print(json.dumps(json_result_set, indent=4))