from utils import start_storage_listener, stop_server

scp = start_storage_listener(address='127.0.0.1', port=11112, ae_title='DICOMROUTER', forward_address='192.168.200.132', fordward_port=11112, forward_ae_title='HIRUKOPACS2')
stop_server(scp)
