# Integrated Library System
Integrated Library System with secure login, 2FA (TBA), search, issue, return functions

# Instructions
-  just run main.py!

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
1. Currently via member id - progress to email pass and 2FA
2. TODO - Functionality for forgot or reset password (2FA extension)

#### Module 2: Search
1. TODO - Parametrized queries against SQLi
2. Search filters and then view results 

#### MOdule 3: Results
1. TODO - State should be preserved on entering page
2. Shows table of search results 

#### Module 4: Borrow/Return
1. Issues table display TODO
2. Remove button needed for state transition

## DataVault
Overarching data-store class that allows for pre-computing of values.
Ex: moving from search to search results - search results table populated onclick 'borrow' on search, and reference stored in DataVault

### Functions

#### populateIssues(): 
Pre-loader for documents already borrowed. Used by HomePage, and SearchResults. Runs when we trigger a state transition via button in these fragments. Also called when book is Returned, to 'refresh'

#### populateResults():
Pre-loader for document search. Used by HomePage, SearchBooks

# Further work
1. 2FA, security measures
2. CLeanup frontend and bind buttons
3. 




