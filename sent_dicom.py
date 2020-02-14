from utils import forward, find_dicom_images
from pydicom import dcmread

dicom_path = '/home/jrudascas/Downloads/dicom/1A14A951/92B94F7B/'

#To DICOM Router
#address = '127.0.0.1'
#port = 11112
#ae_title = 'DICOMROUTER'

#To PACS test
#http://192.168.200.132:45210/hiruko-pacs/
address = '192.168.200.132'
port = 11112
ae_title = 'HIRUKOPACS2'

[forward(address=address, port=port, dataset=dcmread(dicom_file), originator_aet='DAEMONTEST', remote_aet=ae_title) for dicom_file in find_dicom_images(dicom_path)]

