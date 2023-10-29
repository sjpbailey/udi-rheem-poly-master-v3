
import udi_interface
from nodes import RheemNode

LOGGER = udi_interface.LOGGER
LOG_HANDLER = udi_interface.LOG_HANDLER
Custom = udi_interface.Custom
ISY = udi_interface.ISY

# IF you want a different log format than the current default
LOG_HANDLER.set_log_format(
    '%(asctime)s %(threadName)-10s %(name)-18s %(levelname)-8s %(module)s:%(funcName)s: %(message)s')


class RheemController(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name):
        super(RheemController, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.name = 'Rheem Controller'
        self.hb = 0
        self.Parameters = Custom(polyglot, 'customparams')
        self.Notices = Custom(polyglot, 'notices')
        self.TypedParameters = Custom(polyglot, 'customtypedparams')
        self.TypedData = Custom(polyglot, 'customtypeddata')
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.LOGLEVEL, self.handleLevelChange)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameterHandler)
        self.poly.ready()
        self.poly.addNode(self)

    def start(self):
        self.poly.updateProfile()
        self.poly.setCustomParamsDoc()
        self.discover(self)

    def parameterHandler(self, params):
        self.Parameters.load(params)
        LOGGER.debug('Loading parameters now')
        self.check_params()

    def handleLevelChange(self, level):
        LOGGER.info('New log level: {}'.format(level))

    def query(self, command=None):

        nodes = self.poly.getNodes()
        for node in nodes:
            nodes[node].reportDrivers()

    def discover(self, *args, **kwargs):
        self.poly.addNode(RheemNode(self.poly, self.address,
                                    'rheemnodeid', 'Water Heater', self.email, self.password))

    def delete(self):
        LOGGER.info('deleted.')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def set_module_logs(self, level):
        logging.getLogger('urllib3').setLevel(level)

    def check_params(self):
        self.Notices.clear()
        default_email = "YourUserName"
        default_password = "YourPassword"

        self.email = self.Parameters.email
        if self.email is None:
            self.email = default_email
            LOGGER.error(
                'check_params: email not defined in customParams, please add it.  Using {}'.format(default_email))
            self.email = default_email, self.user = self.Parameters.user

        self.password = self.Parameters.password
        if self.password is None:
            self.password = default_password
            LOGGER.error('check_params: password not defined in customParams, please add it.  Using {}'.format(
                default_password))
            self.password = default_password

        # Add a notice if they need to change the user/password from the default.
        if self.email == default_email or self.password == default_password:
            self.Notices['auth'] = 'Please set proper email and password in configuration page'
            self.setDriver('ST', 0)
        else:
            self.setDriver('ST', 1)

    def remove_notices_all(self, command):
        LOGGER.info('remove_notices_all: notices={}'.format(self.Notices))
        # Remove all existing notices
        self.Notices.clear()

    id = 'controller'
    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'REMOVE_NOTICES_ALL': remove_notices_all,
    }
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
    ]
