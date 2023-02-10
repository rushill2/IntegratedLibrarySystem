# Integrated Library System
Integrated Library System with secure login, 2FA (TBA), search, issue, return functions
Ideal use case is on the Staff side of a Library DBMS

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

### 2FA - In Progress
- Optional two-factor authentication with phone number verification code and email+password

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

1. Using 2FA (TODO) or email/pass for Staff and members

#### Module 3: Create Member

1. Creates member account with info and member id 
2. 2FA possible (TODO)

### Member
Can look up books, borrow books return books 

#### Module 1: Login
1. Currently via email + pass with 2FA (In Progress)
2. Email based verification for reset (In Progress)

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
- Overarching data-store class that allows for pre-computing of values.


- Ex: moving from search to search results - search results table populated onclick 'borrow' on search, and reference stored in DataVault


- Each trigger (button or other) to transition to next page calls a function that precomputes values and then loads those retrieved or updated rows into the UI before initializing that fragment

### Functions

#### populateIssues(): 
Pre-loader for documents already borrowed. Used by HomePage, and SearchResults. Runs when we trigger a state transition via button in these fragments. Also called when book is Returned, to 'refresh'

#### populateResults():
Pre-loader for document search. Used by HomePage, SearchBooks





