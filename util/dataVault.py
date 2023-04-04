import logging
logger = logging.getLogger()


class DataVault:
    # Member Variables
    mem_id = None
    member = None
    type = None

    # Book Data Fields
    bookdatafields = []

    # Two Factor Authentication
    twofa_origin = None
    twofa_back = None
    twoFAid = None
    twoFAtype = None

    # Member and Staff Login
    memberloggedin = None
    loggedinID = None
    lib_loggedin = False
    mem_loggedin = False
    staffloggedin = None
    createdStaffId = None

    # Page Map and Navigation
    pageMap = {}
    delarr = []
    borrowbuttons = []
    modbtnarr = []
    deetbtnarr = []

    # Borrowing and Returning
    borrowarr = []
    returnarr = []
    retbook = None
    BBorrows = None

    # Members and Search
    memDetails = None
    memberarr = []
    searchBooks = None
    searchRes = None
    viewMems = None
    viewMemberList = []

    # Other
    issues = []
    inputvalues = {}
    globallog = None
    bookborrows_msg = None
    bookborrows_prev = "SearchResults"