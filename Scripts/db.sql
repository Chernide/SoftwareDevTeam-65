CREATE TABLE Politicians (
	Politician_id	serial			NOT NULL PRIMARY KEY, 
	Name 			varchar(250) 	NOT NULL, 
	Chamber			varchar(100)	NOT NULL, 
	Party 			varchar(20)		NOT NULL, 
	State			varchar(50) 	NOT NULL,
	Phone_num		varchar(15)		NOT NULL,
	Twitter			varchar(15)		NOT NULL
)
