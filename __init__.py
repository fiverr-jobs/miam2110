from database import Database
from finanzen import Finanzen

# from assfinet import Assfinet
from klicktipp import Klicktipp
from datetime import datetime
import time


# """
# initial pull of all leads
# """

# print("Inizializing Script ...\n")
# print("Pulling all leads ...\n")
# db_instance = Database()
# finanzen_instance = Finanzen()
# initial_pull_data = finanzen_instance.initial_pull()
# new_leads = len(initial_pull_data)

# """
# loop over leads and check if they exist
# """

# print("Searching for new Leads ...\n")

# for lead in initial_pull_data:
#     if db_instance.lead_exists(lead):
#         new_leads -= 1
#         continue
#     print("Adding Lead with Id {} to Database".format(lead.id))
#     db_instance.add_lead(lead)
# print("\nAdded {} new Leads to the Database\n".format(new_leads))

# """
# clean variables
# """
# del db_instance
# del finanzen_instance
# del initial_pull_data
# del new_leads

# """
# Start the ongoing loop for pulling the latest leads
# """
# print("Starting pull Loop every 5 min\n")

while True:
    db_instance = Database()
    finanzen_instance = Finanzen()

    print("sleeping for 5 minutes ...\n")
    # time.sleep(300)
    time.sleep(5)
    print("====================================================")
    print("Starting the Loop at {}\n".format(datetime.now()))

    """
    pulling Leads from the last 24 hours
    """
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

    """
    Pushing Leads to Klicktipp
    """
    print("searching for Leads to push to KlickTipp ...\n")
    klicktipp_instance = Klicktipp()

    klicktipp_pushed = 0
    klicktipp_errors = 0
    leads_for_klicktipp = db_instance.get_klicktipp()
    for lead in leads_for_klicktipp:
        # klicktipp_instance.post_lead(lead)
        print(lead)
    print(
        "Pushed {} Leads to Assfinet with {} errors\n".format(
            klicktipp_pushed, klicktipp_errors
        )
    )

    # """
    # Pushing Leads to Assfinet
    # """
    # print("searching for Leads to push to Assfinet ...\n")
    # assfinet_pushed = 0
    # assfinet_errors = 0
    # leads_for_assfinet = db_instance.get_assfinet()
    # for lead in leads_for_assfinet:
    #     # TODO push lead to Assfinet
    #     # print(lead.id)
    #     pass
    # print(
    #     "Pushed {} Leads to Assfinet with {} errors\n".format(
    #         assfinet_pushed, assfinet_errors
    #     )
    # )

    """
    clean variables
    """
    del db_instance
    del finanzen_instance
    del last_day_data_pull
    del new_leads
    # del leads_for_assfinet
    del leads_for_klicktipp
    # del assfinet_pushed
    del klicktipp_instance
    del klicktipp_pushed
    # del assfinet_errors
    del klicktipp_errors
