# Integrated Library System
Integrated Library System with secure login, 2FA, search, issue, return functions
Ideal use case is on the Staff side of a Library DBMS

## Version History

#### 1.0.0:
- Initial Commit, basic search functions working

#### 1.0.1:
- Added login with email ID and password instead of member id

#### 1.0.2:
- Stored password as hash, created staff home page

#### 1.1.0:
- Completed Member side (except for magazines and journals (low priority)
- Set up input validation for account creation (edge case - empty fields - defaults to date issue)

#### 1.2.0:
- Fixed state transition issues
- Added SMTP client for book reminder emails

#### 1.3.0:
- Added 2FA for member account create and login
- Changed all UI widgets to grid layout, earlier used tk.__widget__.pack()

#### 1.3.1
- Refactor
- Check for if email already in use
- 2FA for Staff login added

#### 1.3.2
- Fixed details regression
- Validation Class added


# Instructions
### To Run
-  just run main.py!
### First Time Setup
- While there already is data in the server, the first step would be to create a Staff Account by choosing Librarian on the home page and then Create
- Second, create member accounts
- Now, users can log in as Librarian or Member and execute any of their actions

# Security Features
### Password Hashing
Passwords are stored as an MD5 Hash. When logging in, the input's hash is computed and compared to stored hash

### 2FA
- Optional two-factor authentication with phone number verification code and email+password. For both Members and Staff

### Password Reset - In Progress
- Uses 2FA to verify and sends an email using the SMTP server for the email domain name with a code (since it's not a web app can't do a url)

### Parametrized SQL
Mainly to prevent injections. Input validation as well in order to prevent any mischief

# Specifications

## User Types

### Staff

Able to create members and librarian accounts, lookup book journal or magazine entries and alter their contents. Can also create new librarian and delete members. Checks borrowed books as well a whole list of books borrowed etc).

#### Module 1: Create Account

1. Login Options: Email + Password or set up 2FA. Password stored as MD5 Hash

#### Module 2: Login

1. Using 2FA and email/pass for Staff and members

#### Module 3: Create Member

1. Creates member account with info and member id 
2. 2FA

#### Module 4: Member Details:
1. Can view member issues and send email reminders by clicking Notify button

### Member
Can look up books, borrow books return books 

#### Module 1: Login
1. Currently via email + pass with 2FA
2. Email based verification for reset (In Progress) - move to phone 2FA

#### Module 2: Search
1. TODO - Parametrized queries against SQLi
2. Set search filters and then view results 

#### MOdule 3: Results
1. TODO - State should be preserved on entering page
2. Shows table of search results 

#### Module 4: Borrow/Return
1. Issues table display TODO
2. Remove button needed for state transition

## DataVault
1. Overarching data-store class that allows for pre-computing of values.


2. Ex: moving from search to search results - search results table populated onclick 'borrow' on search, and reference stored in DataVault


3. Each trigger (button or other) to transition to next page calls a function that precomputes values and then loads those retrieved or updated rows into the UI before initializing that fragment

### Functions

#### populateIssues(): 
Pre-loader for documents already borrowed. Used by HomePage, and SearchResults. Runs when we trigger a state transition via button in these fragments. Also called when book is Returned, to 'refresh'

#### populateResults():
Pre-loader for document search. Used by HomePage, SearchBooks





