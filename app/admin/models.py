""" ADMIN MODELS"""
from app import db


class Admin(object):
    """ Ito yung mga functions sa dropdown ng model sa admin page sidebar (eg. Create new, View all)
    """
    __amfunctions__ = None
    
    """ Ito yung icon sa admin page (eg. pe-7s-users).
    Refer sa dashboardpack.com sa mga available icons
    """
    __amicon__ = ""
    
    __view_url__ = 'bp_admin.no_view_url'

    __parent_model__ = None

    @property
    def __amname__(self):
        """ Ito yung parang code nya(eg. auth) for authentication.
        Ito yung reference mo sa model sa mga code mo wag yung description
        Ex. if model.__amcode__ = 'auth': 
        """
        raise NotImplementedError('Must implement admin-model name')

    @property
    def __amdescription__(self):
        """ Ito ung visible sa admin page(eg. Authentication)
        """
        raise NotImplementedError('Must implement admin-model description')


class AdminOptions(db.Model):
    __tablename__ = 'admin_options'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    header_color = db.Column(db.String(64))
    sidebar_color = db.Column(db.String(64))


class AdminDashboard(Admin):
    __amname__ = 'admin_dashboard'
    __amdescription__ = 'Admin Dashboard'
    __amicon__ = 'pe-7s-graph1'
    __view_url__ = 'bp_admin.dashboard'


class AdminApp(Admin):
    __amname__ = 'admin_app'
    __amdescription__ = 'Apps'
    __amicon__ = 'pe-7s-graph1'
    __view_url__ = 'bp_admin.apps'

