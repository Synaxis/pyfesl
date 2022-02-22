from twisted.web.resource import Resource

from Database import Database
from Logger import Log

logger = Log("SecureWebServer", "\033[36m")
logger_err = Log("SecureWebServer", "\033[36;41m")

header = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

db = Database()


class Handler(Resource):
    isLeaf = True

    def render_GET(self, request):
        uri = request.uri
        request.setHeader('Content-Type', 'text/xml; charset=utf-8')

        if uri == '/nucleus/authToken':
            serverKey = request.getHeader("X-SERVER-KEY")

            logger.new_message("[MAGMA] Sending authToken...", 2)
            if serverKey is None:
                userKey = request.getCookie("magma")

                response = header
                response += '<success><token code="NEW_TOKEN">' + userKey + '</token></success>'

                return response.encode()
        elif uri.find('/nucleus/entitlements/') != -1:
            userID = uri.split("/")[-1]

            entitlements = db.getUserEntitlements(userID)
            logger.new_message("[MAGMA] Sending entitlements for userID " + str(userID), 2)

            response = header
            response += '<entitlements>'
            for entitlement in entitlements:
                response += '<entitlement>'
                response += '<entitlementId>' + str(entitlement['entitlementId']) + '</entitlementId>'
                response += '<entitlementTag>' + str(entitlement['entitlementTag']) + '</entitlementTag>'
                response += '<useCount>0</useCount>'
                response += '<status>' + str(entitlement['status']) + '</status>'
                response += '<userId>' + str(entitlement['userId']) + '</userId>'
                response += '</entitlement>'
            response += '</entitlements>'

            return response.encode()
        elif uri.find('/nucleus/wallets/') != -1:
            userID = uri.split("/")[-1]
            logger.new_message("[MAGMA] Sending wallets info for userID " + str(userID), 2)

            response = header
            response += '<billingAccounts>'

            response += '<walletAccount>'
            response += '<currency>_DV</currency>'  # valor points
            response += '<balance>0</balance>'
            response += '</walletAccount>'

            response += '<walletAccount>'
            response += '<currency>_DB</currency>'  # battle funds
            response += '<balance>0</balance>'
            response += '</walletAccount>'

            response += '<walletAccount>'
            response += '<currency>_DH</currency>'  # hero points
            response += '<balance>0</balance>'
            response += '</walletAccount>'

            response += '</billingAccounts>'

            return response.encode()
        elif uri == '/ofb/products':
            logger.new_message("[MAGMA] Sending products...", 2)

            file_handler = open('Data/products.xml', 'rb')
            response = file_handler.read()
            return response.encode()
        elif uri.split(":")[0] == '/relationships/roster/nucleus':
            logger.new_message("[MAGMA] Sending Roster response...")
            response = header
            response += '<roster relationships="0"/><success code="SUCCESS"/>'

            return response.encode()
        elif uri.find('/nucleus/name/') != -1:
            userID = uri.split("/")[-1]

            logger.new_message("[MAGMA] Sending name response for PID " + str(userID))

            response = header
            response += "<name>" + db.getPersonaName(userID) + "</name>"

            return response.encode()
        else:
            logger.new_message("Unknown GET: " + uri, 2)

    def render_POST(self, request):
        uri = request.uri

        if uri.split(':')[0] == '/relationships/status/nucleus':
            logger.new_message("[MAGMA] Sending Relationship status...")

            request.setHeader('content-type', 'text/plain; charset=utf-8')
            return '<update><id>1</id><name>Test</name><state>ACTIVE</state><type>server</type><status>Online</status><realid>' + uri.split(':')[1] + '</realid></update>'
        elif uri.split(':')[0] == '/relationships/status/server':
            request.setHeader('content-type', 'text/plain; charset=utf-8')
            return '<update><id>1</id><name>Test</name><state>ACTIVE</state><type>server</type><status>Online</status><realid>' + uri.split(':')[1] + '</realid></update>'
        else:
            logger_err.new_message("Unknown POST: " + request.uri, 2)
