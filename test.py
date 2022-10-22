from gmailAuthentication import authentication
from gmailExtract import    gmailExtract


obj = authentication()
obj1 = gmailExtract(obj.getgmailAuthentication())
obj1.extractUnreadEmails()