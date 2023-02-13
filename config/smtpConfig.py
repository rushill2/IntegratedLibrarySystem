noreply = "friendlyneighborhoodlibrary@gmail.com"
passw = 'zlipphvwdkctrjmz'
templates = {
    'reminder' : "Hello! \n \t This email is a reminder for your recent issue from ILS. The book "+ '"' + '{_title}' + '"' + " is due in {_days}. \n Hope to see you soon!\n ILS Team",
    'overdue': "Hello! \n \t This email is an overdue notification for your recent issue from ILS. The book "+ '"' + '{_title}' + '"' + " was due {_days} ago. No cookie for you. \n Hope to see you soon!\n ILS Team",
    'today': "Hello! \n \t This email is a reminder for your recent issue from ILS. The book "+ '"' + '{_title}' + '"' + " is due today. Run! \n Hope to see you soon! \n ILS Team"
}