from meas import snapshot

oscillResource = 'USB0::0x1AB1::0x04CE::DS1ZD171500380::INSTR'
channels = '1'


data = snapshot(oscillResource, channels)
