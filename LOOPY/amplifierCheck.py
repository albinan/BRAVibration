import time

def amplifierCheck(inst):
    y = float(inst.query(':VOLTage?'))
    if y > 4.9:
        print('Increase level on amplifier')
        print('Waiting 7 seconds...')
        time.sleep(7)
    elif y < 21*1e-3:
        print('Decrease level on amplifier')
        print('Waiting 7 seconds...')
        time.sleep(7)
