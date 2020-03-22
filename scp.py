from pynetdicom import AE, evt, StoragePresentationContexts, VerificationPresentationContexts, QueryRetrievePresentationContexts, RelevantPatientInformationPresentationContexts
from scu import ServiceClassUser
from utils import decryption
import json


class ServiceClassProvider(object):

    def __init__(self, parameters_json):
        self.parameters = parameters_json
        self.ae_title = self.parameters['SERVER_SCP_AET']
        self.address = self.parameters['SERVER_SCP_ADDRESS']
        self.port = self.parameters['SERVER_SCP_PORT']

        self.ae = AE(ae_title=self.ae_title)
        self.ae.supported_contexts = StoragePresentationContexts
        self.ae.supported_contexts = VerificationPresentationContexts
        self.ae.supported_contexts = QueryRetrievePresentationContexts
        self.ae.supported_contexts = RelevantPatientInformationPresentationContexts

    def start_server(self):
        def handle_store(event):
            print('Message received')
            ds = event.dataset
            ds.file_meta = event.file_meta

            if True: #Fordward rules
                scu = ServiceClassUser(self.parameters['SERVER_SCU_AET'])
                scu.associate(remote_address=self.parameters['SERVER_REMOTE_ADDRESS'], remote_port=self.parameters['SERVER_REMOTE_PORT'], remote_aet=self.parameters['SERVER_REMOTE_AET'])

                status = scu.send_c_store(dataset=ds)
                if status == 0:
                    print("Message forwarded successfully")
                    return 0x0000
                else:
                    print("Message error: ", status)

                del(scu)
            else:
                print("Message discarded")
                return 0x0000

        handlers = [(evt.EVT_C_STORE, handle_store), (evt.EVT_C_MOVE, handle_store)]
        print('Server started successfully')
        scp = self.ae.start_server((self.address, self.port), block=True, evt_handlers=handlers)
        return scp


try:
    scp = None
    key_file = open(file='imex_router.json', mode='r')
    hash = key_file.read()
    key_file.close()
    parameters_json = json.loads(decryption(hash = hash, key=None))
    service = ServiceClassProvider(parameters_json)
    scp = service.start_server()
except Exception as e:
    print('Fatal error ', e.__str__())
    pass
finally:
    if scp is not None: #This is not working. We need to check it
        scp.shutdown()
        print('Server Shutdown')
