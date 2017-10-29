CREATE TABLE Users (
	User_ID 			serial			NOT NULL PRIMARY KEY, 
	Email 				varchar(150)	NOT NULL, 
	Encrypted_Password 	varchar(256)	NOT NULL
)
