from database import Database
from finanzen import Finanzen

from assfinet import Assfinet
from klicktipp import Klicktipp
from datetime import datetime
import time


def daily_pull():
    db_instance = Database()
    finanzen_instance = Finanzen()

    print("pulling Leads from the last 24 hours ...\n")

    last_day_data_pull = finanzen_instance.last_day_pull()
    new_leads = len(last_day_data_pull)
    print("Searching for new Leads ...\n")
    for lead in last_day_data_pull:
        if db_instance.lead_exists(lead):
            new_leads -= 1
            continue
        print("Adding Lead with Id {} to Database ...".format(lead.id))
        db_instance.add_lead(lead)
    print("Added {} new Leads to the Database\n".format(new_leads))

    del db_instance
    del finanzen_instance
    del last_day_data_pull
    del new_leads


def initial_pull():
    db_instance = Database()
    finanzen_instance = Finanzen()

    print("Pulling all leads ...\n")
    initial_pull_data = finanzen_instance.initial_pull()
    new_leads = len(initial_pull_data)

    """
    loop over leads and check if they exist
    """

    print("Searching for new Leads ...\n")

    for lead in initial_pull_data:
        if db_instance.lead_exists(lead):
            new_leads -= 1
            continue
        print("Adding Lead with Id {} to Database".format(lead.id))
        db_instance.add_lead(lead)
    print("\nAdded {} new Leads to the Database\n".format(new_leads))

    del db_instance
    del finanzen_instance
    del initial_pull_data
    del new_leads


def klicktipp_push():
    db_instance = Database()
    klicktipp_instance = Klicktipp()

    """
    Pushing Leads to Klicktipp
    """
    print("searching for Leads to push to KlickTipp ...\n")

    klicktipp_pushed = 0
    klicktipp_errors = 0

    leads_for_klicktipp = db_instance.get_klicktipp()
    for lead in leads_for_klicktipp:
        klicktipp_instance.post_lead(lead)
        db_instance.confirm_klicktipp(lead)
        klicktipp_pushed += 1
    print(
        "Pushed {} Leads to Klicktipp with {} errors\n".format(
            klicktipp_pushed, klicktipp_errors
        )
    )
    del klicktipp_instance
    del db_instance
    del leads_for_klicktipp
    del klicktipp_pushed
    del klicktipp_errors


def assfinet_push():
    pass


def main():

    print("Inizializing Script ...\n")

    """
    initial pull of all leads and push to klickTipp and Assfinet
    """

    initial_pull()
    klicktipp_push()
    assfinet_push()

    """
    Start the ongoing loop for pulling the latest leads
    """

    while True:
        print("====================================================")
        print("Starting the Loop at {}\n".format(datetime.now()))

        """
        pulling Leads from the last 24 hours
        """
        daily_pull()
        klicktipp_push()
        assfinet_push()
        print("sleeping for 3 hours ...\n")
        time.sleep(10800)

main()
