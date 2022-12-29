password = None

createtable = {
    "Mem": "CREATE TABLE IF NOT EXISTS Member (Member_Id int, PRIMARY KEY(Member_Id), first_name VARCHAR(255), last_name VARCHAR(255), date_of_birth DATE, Books_Borrowed VARCHAR(255), No_of_Borrows int,  Phone int)",
    "Issue": "CREATE TABLE IF NOT EXISTS Issues (Issue_Id int,  PRIMARY KEY(Issue_Id), Item_Id int, Title VARCHAR(255), Date_Issued DATE, Date_Due DATE)",
    "Docs": "CREATE TABLE IF NOT EXISTS Documents(Doc_Id int, PRIMARY KEY(Doc_Id), Copies int, Issue_Id int, FOREIGN KEY(Issue_Id) references Issues(Issue_Id))",
    "Book": "CREATE TABLE IF NOT EXISTS Books(Book_Id int, PRIMARY KEY(Book_Id), Book_Title VARCHAR(255), Edition VARCHAR(255), Keywords VARCHAR(255), Genre VARCHAR(255), Topic VARCHAR(255), Authors VARCHAR(255), Publication_Date DATE)",
    "Mags": "CREATE TABLE IF NOT EXISTS Magazines(Mag_Id Integer PRIMARY KEY, FOREIGN KEY(Mag_Id) references Documents(Doc_Id), Title VARCHAR(255), Issue VARCHAR(255), Publication_Date DATE, Editors VARCHAR(255), Contributors VARCHAR(255), Keywords VARCHAR(255),  Genre VARCHAR(255), Topic VARCHAR(255))",
    "Journs": "CREATE TABLE IF NOT EXISTS Journals(Journ_Id Integer PRIMARY KEY,FOREIGN KEY(Journ_Id) references Documents(Doc_Id),Title VARCHAR(255),Journal VARCHAR(255),Authors VARCHAR(255),Keywords VARCHAR(255),Genre VARCHAR(255),Topic VARCHAR(255),Publisher VARCHAR(255),Issue VARCHAR(255),Publication_Date DATE)",
    "Loc": "CREATE TABLE IF NOT EXISTS Location(Doc_Id int, FOREIGN KEY(Doc_Id) references Documents(Doc_Id), Room VARCHAR(255), Shelf VARCHAR(255))"
}

tables = {
    'Mem': "Member",
    'Issue': 'Issues',
    'Book': 'Books',
    'Mags': 'Magazines',
    'Journs': 'Journals',
    'Loc': 'Location'
}


sql = {
    'searchDocs': "SELECT * FROM librarian.{_tbl} WHERE ",
    'borrowDoc': 'INSERT INTO librarian.Issues(Issue_Id, Item_Id, Title, Date_Issued, Date_Due) VALUES({_tbl}, {_tbl},{_tbl},{_tbl},{_tbl} )',
    'returnDoc': 'DELETE FROM librarian.Issues() WHERE Issue_Id = {_id}',
    'updateMemberIssues': "UPDATE librarian.Member SET No_of_Borrows = {_borrows}, Books_Borrowed = {_books}",
    'selectMemberIssues': "SELECT No_of_Borrows, Books_Borrowed FROM librarian.Member WHERE ",
    'memberlogin': 'SELECT * FROM librarian.Member WHERE Member_Id = {_id}'
}

template = {
    'Books': {
        0: "Book_Title",
        1: "Edition",
        2: "Keywords",
        3: "Genre",
        4: "Topic",
        5: "Authors",
        6: "Publication_Date"
    },
    'Journs': {
        0: "Title",
        1: "Journal",
        2: "Authors",
        3: "Keywords",
        4: "Genre",
        5: "Topic",
        6: "Publisher",
        7: "Issue",
        8: "Publication_Date"
    },
    'Mags': {
        0: "Title",
        1: "Issue",
        2: "Editors",
        3: "Contributors",
        4: "Keywords",
        5: "Genre",
        6: "Topic",
        7: "Publication_Date"
    }
}