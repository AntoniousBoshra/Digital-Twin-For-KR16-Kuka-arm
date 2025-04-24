import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/antoniousboshra/antonious_boshra_kuka_arm/install/kuka_mqtt_bridge'
