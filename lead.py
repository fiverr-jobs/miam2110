# DONE define Lead with all necessary attributes
# TODO define function to check if lead already pushed
# TODO define function to export attributes in a sqllite form
class Lead:
    def __init__(self, lead):
        self.id = lead.get("id")
        self.salutation = lead.get("salutation")
        self.gender = lead.get("gender")
        self.firstName = lead.get("firstName")
        self.lastName = lead.get("lastName")
        self.dateOfBirth = lead.get("dateOfBirth")
        self.occupation = lead.get("occupation")
        self.phone = lead.get("phone")
        self.email = lead.get("email")
        self.street = lead.get("street")
        self.postalCode = lead.get("postalCode")
        self.city = lead.get("city")
        self.state = lead.get("state")
        self.company = lead.get("company")
        self.subject = lead.get("subject")
        self.data = lead.get("data")
        self.createdAt = lead.get("createdAt")

        self.dbId = lead.get("dbId") or None
        self.assfinet = lead.get("assfinet") or False
        self.klicktipp = lead.get("klicktipp") or False
        self.err = lead.get("err") or False
        self.errMess = lead.get("errMess") or ""

    def pushed_to_assfinet(self):
        return self.assfinet

    def pushed_to_klicktipp(self):
        return self.klicktipp

    def has_error(self):
        return self.err
