
def overshoot(inst, channel):
    Vpp = float(inst.query(':MEASure:ITEM? VPP,'+channel))
    window_size = 8*float(inst.query(':' + channel + ':SCALe?'))
    #print('Vpp: ' + str(Vpp) + ' window_size ' + str(window_size))
    while Vpp > 9999:
        window_size = 8*inst.write(':' + channel + ':SCALe ' + str(window_size*0.9))
        Vpp = float(inst.query(':MEASure:ITEM? VPP,'+channel))
        window_size = 8*float(inst.query(':' + channel + ':SCALe?'))
