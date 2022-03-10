import sqlite3
from lead import Lead


class Database(object):
    __DB_LOCATION = "lead.db"

    def __del__(self):
        self.connection.close()

    def __enter__(self):
        self.cur = self.connection.cursor()
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()

    def __init__(self):
        """Initialize db class variables"""

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            d = Lead(d)
            return d

        self.connection = sqlite3.connect(Database.__DB_LOCATION)
        self.connection.row_factory = dict_factory
        self.cur = None

    def close(self):
        """close sqlite3 connection"""
        self.connection.close()

    def commit(self):
        """commit changes to database"""
        self.connection.commit()

    def add_lead(self, lead):
        query = 'insert into leads (id, salutation, firstName, lastName, dateOfBirth, occupation, phone, email, street, postalCode, city, state, company, subject, data, createdAt) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(
            lead.id,
            lead.salutation,
            lead.firstName,
            lead.lastName,
            lead.dateOfBirth,
            lead.occupation,
            lead.phone,
            lead.email,
            lead.street,
            lead.postalCode,
            lead.city,
            lead.state,
            lead.company,
            lead.subject,
            lead.data,
            lead.createdAt,
        )

        with self:
            self.cur.execute(query)
            lead.id = self.cur.lastrowid

    def lead_exists(self, lead):
        query = 'select * from leads where "id" = {}'.format(lead.id)
        with self:
            self.cur.execute(query)
            lead = self.cur.fetchone()
        return bool(lead)

    def confirm_assfinet(self, lead):
        query = 'update leads set "assfinet" = 1 where "id" = {}'.format(lead.id)
        with self:
            self.cur.execute(query)

    def confirm_klicktipp(self, lead):
        query = 'update leads set "klicktipp" = 1 where "id" = {}'.format(lead.id)
        with self:
            self.cur.execute(query)

    def get_assfinet(self):
        query = 'select * from leads where "assfinet" = 0'
        with self:
            self.cur.execute(query)
            leads = self.cur.fetchall()
        return leads

    def get_klicktipp(self):
        query = 'select * from leads where "klicktipp" = 0'
        with self:
            self.cur.execute(query)
            leads = self.cur.fetchall()
        return leads

    def save_error(self, lead, error):
        query = 'update leads set "err" = 1, "errMess" = {} where "id" = {}'.format(
            error, lead.id
        )
        with self:
            self.cur.execute(query)
