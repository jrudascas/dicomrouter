from pynetdicom import AE, evt, StoragePresentationContexts, VerificationPresentationContexts
import time
from os.path import join
import os


def find_dicom_images(folder_path):
    dicom_files = []
    for (root, dirs, files) in os.walk(folder_path):
        for file in files:
            dicom_files.append(join(root, file))

    return dicom_files


def forward(address, port, dataset, originator_aet, remote_aet):
    ae = AE(ae_title=originator_aet)
    ae.requested_contexts = StoragePresentationContexts

    # Associate with peer AE at IP=address and port=port
    assoc = ae.associate(addr=address, port=port, ae_title=remote_aet)

    if assoc.is_established:

        status = assoc.send_c_store(dataset, originator_aet=originator_aet)
        if status:
            print('C-STORE request status: 0x{0:04x}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')


def start_storage_listener(address, port, ae_title, forward_address, fordward_port, forward_ae_title):
    def handle_store(event):
        print("Llegó un evento")
        ds = event.dataset
        ds.file_meta = event.file_meta
        ds.AccessionNumber = 'ImexDICOMRouter_66fefe77905e99da2e64f290f8b508e87c77f29d'

        forward(address=forward_address, port=fordward_port, dataset=ds, originator_aet=ae_title, remote_aet=forward_ae_title)
        return 0x0000

    ae = AE(ae_title=ae_title)
    ae.supported_contexts = StoragePresentationContexts
    ae.supported_contexts = VerificationPresentationContexts

    handlers = [(evt.EVT_C_STORE, handle_store)]
    scp = ae.start_server((address, port), block=False, evt_handlers=handlers)
    print('Server started successfully')
    return scp


def stop_server(scp):
    time.sleep(600)
    scp.shutdown()