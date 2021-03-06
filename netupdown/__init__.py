import sys
import gtk
import appindicator

import imaplib
import re

PING_FREQUENCY = 10 # seconds


class NetUpDown(object):
    def __init__(self):
        self.ind = appindicator.Indicator(
            "net-status-indicator",
            "indicator-messages",
            appindicator.CATEGORY_APPLICATION_STATUS
        )
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon("new-messages-red")

        self.menu_setup()
        self.ind.set_menu(self.menu)

    def menu_setup(self):
        self.menu = gtk.Menu()

        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def main(self):
        self.check_status()
        gtk.timeout_add(PING_FREQUENCY * 1000, self.check_status)
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

    def check_status(self):
        messages, unread = self.gmail_checker('myaddress@gmail.com','mypassword')
        if unread > 0:
            self.ind.set_status(appindicator.STATUS_ATTENTION)
        else:
            self.ind.set_status(appindicator.STATUS_ACTIVE)
        return True

    def gmail_checker(self, username, password):
        i = imaplib.IMAP4_SSL('imap.gmail.com')
        try:
            i.login(username, password)
            x, y = i.status('INBOX', '(MESSAGES UNSEEN)')
            messages = int(re.search('MESSAGES\s+(\d+)', y[0]).group(1))
            unseen = int(re.search('UNSEEN\s+(\d+)', y[0]).group(1))
            return (messages, unseen)
        except:
            return False, 0

def main():
    indicator = NetUpDown()
    indicator.main()

    
if __name__ == "__main__":
    main()
    
