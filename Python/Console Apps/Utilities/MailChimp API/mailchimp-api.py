from mailchimp3 import MailChimp


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key) + '\n')
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value) + '\n')


def menu():
    print("""
    MailChimp API Menu:
    1.  List campaigns
    2.  List Subscribers
    3.  Exit
    """)
    choice = input("Enter your numerical selection, please: ")

    if choice == "1":
        pretty(client.campaigns.all(get_all=True))
    elif choice == "2":
        print("The following are the available lists with their list ID:\n",
              client.lists.all(get_all=True, fields="lists.name,lists.id"))
        choice = input("What is the list ID of the member list you wish to see? ")
        pretty(client.lists.members.all(choice, get_all=True))
    else:
        exit()


client = MailChimp(mc_api='2b05f96cead1dc46d3fcd595cb40f76f-us13', mc_user='optimalleader')
menu()
