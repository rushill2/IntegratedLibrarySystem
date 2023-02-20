createtable = {
    "Mem": "CREATE TABLE IF NOT EXISTS Member (Member_Id int, PRIMARY KEY(Member_Id), first_name VARCHAR(255), last_name VARCHAR(255), date_of_birth DATE, Books_Borrowed VARCHAR(255), No_of_Borrows int,  Phone VARCHAR(255), Email VARCHAR(255), TwoFA TINYINT)",
    "Issue": "CREATE TABLE IF NOT EXISTS Issues (Issue_Id int,  PRIMARY KEY(Issue_Id), Item_Id int, Title VARCHAR(255), Date_Issued DATE, Date_Due DATE, Member_Id INT)",
    "Docs": "CREATE TABLE IF NOT EXISTS `Documents` (`Doc_Id` int NOT NULL,`Copies` int DEFAULT NULL,`Issue_Id` int DEFAULT NULL,`Doctype` varchar(45) DEFAULT NULL,`Member_Id` int DEFAULT NULL,PRIMARY KEY (`Doc_Id`))",
    "Book": "CREATE TABLE IF NOT EXISTS Books(Book_Id int, PRIMARY KEY(Book_Id), Book_Title VARCHAR(255), Edition VARCHAR(255), Keywords VARCHAR(255), Genre VARCHAR(255), Topic VARCHAR(255), Authors VARCHAR(255), Publication_Date DATE)",
    "Loc": "CREATE TABLE IF NOT EXISTS Location(Doc_Id int, FOREIGN KEY(Doc_Id) references Documents(Doc_Id), Room VARCHAR(255), Shelf VARCHAR(255))"
}


sql = {
    'getMemberBorrows': 'SELECT Books_Borrowed, No_of_Borrows from Librarian.Member WHERE Member_Id = {_id};',
    'update': 'UPDATE Librarian.{_tbl} SET ',
    'selectbyId': "SELECT * FROM Librarian.{_tbl} WHERE {_idtype} = {_id};",
    'searchDocs': "SELECT Doc_Id, Book_Title, Edition, Keywords, Genre, Authors, Publication_Date FROM Librarian.{_tbl} WHERE ",
    'insertIssues': 'INSERT INTO Librarian.Issues(Title, Date_Issued, Date_Due, Item_Id, Member_Id) VALUES({_ttl},{_date},{_due}, {_docid}, {_memid});',
    'deleteIssues': "DELETE FROM Librarian.Issues WHERE Item_Id = {_id}",
    'returnDoc': 'DELETE FROM Librarian.Issues WHERE Issue_Id = {_id}',
    'updateMemberIssues': "UPDATE Librarian.Member SET No_of_Borrows = %s, Books_Borrowed = %s WHERE Member_Id = %s",
    'selectMemberIssues': "SELECT No_of_Borrows, Books_Borrowed FROM Librarian.Member WHERE ",
    'memberlogin': 'SELECT * FROM Librarian.Member WHERE {_login} = {_input} AND Password = {_pass}',
    'getDocDetails': 'SELECT * from Librarian.Documents WHERE Doc_Id = {_id};',
    'getColumns' : 'SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = "{_table}";',
    'getMemberIssues': 'SELECT * FROM Librarian.Issues where Member_Id = {_memid};',
    'selectMembers': "SELECT * FROM Librarian.Member WHERE Member_Id = {_memid};",
    'insertStaff': "INSERT INTO Librarian.Staff (Staff_Id, FirstName, LastName, DOB, Phone, Email, Password) VALUES (%s, %s, %s, %s, %s, %s, %s);",
    'memberIssued': "SELECT * FROM Librarian.Issues WHERE Item_Id = {_id} AND Member_Id = {_memid};",
    'loginStaff': "SELECT * FROM Librarian.Staff WHERE {_login} = {_input} AND Password = {_pass};",
    'viewMembers' : "SELECT Member_Id, first_name, last_name, date_of_birth, Books_Borrowed, No_of_Borrows,Phone, Email  FROM Librarian.Member;",
    'insertMember': 'INSERT INTO Librarian.Member (Member_Id, first_name, last_name, date_of_birth, Phone, Email, Password, No_of_Borrows) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);',
    'deleteMember': 'DELETE FROM Librarian.Member WHERE Member_Id = {_memid};',
    'emailExists': 'SELECT * FROM Librarian.{_table} WHERE Email = {_email};',
    'updateMember': "UPDATE Librarian.Member SET first_name = %s, last_name = %s, date_of_birth = %s, Phone = %s, Email = %s WHERE Member_Id = %s;",
    'insertBook': "INSERT INTO Librarian.Books (Book_Id, Doc_Id, Book_Title, Edition, Keywords, Genre, Authors, Publication_Date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
    'allBooks': "SELECT Doc_Id, Book_Title, Edition, Keywords, Genre, Authors, Publication_Date FROM Librarian.Books;"
}

columns = {
    "Books": ("Number", "Title", "Edition", "Keywords", "Genre", "Topic", "Authors", "Publication Date"),
}