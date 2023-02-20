import logging
logger = logging.getLogger()


class DataVault:
    mem_id = None
    member = None
    type = None
    bookdatafields = []
    twofa_origin=None
    twofa_back = None
    memberloggedin = None
    loggedinID = None
    pageMap = {}
    staffloggedin = None
    delarr = []
    borrowbuttons = []
    bookborrows_msg = None
    bookborrows_prev = "SearchResults"
    lib_loggedin = False
    mem_loggedin = False
    modbtnarr = []
    currMem = None
    deetbtnarr = []
    issues = []
    memDetails = None
    borrowarr = []
    returnarr = []
    memberarr = []
    retbook = None
    BBorrows = None
    searchBooks = None
    inputvalues = {}
    searchRes = None
    viewMems = None
    viewMemberList = []
    globallog = None
