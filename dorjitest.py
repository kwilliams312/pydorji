#!/usr/bin/env python

class dorji:
    '''
    A class for managing the Dorji818 chip via serial
    '''

    def __init__( self, **kwargs ):
        '''
        Set defaults

        Establish a serial connection to device at baud rate, uses pyserial

          Serial options:
            * baud - Baud rate string        | Default: "9600"
            * device - a device string       | Default: "/dev/ttyS0"

          Frequency options:
            * tx - transmit frequency string | Default: "134.0000"
            * rx - receive frequency string  | Default: "134.0000"
            * sq - squelch integer 1-8       | Default: 1
            * vol - volume integer 1-8       | Default: 1
            * gwb - Channel Space 1-25000    | Default: 0

          Continuous Tone-Coded Squelch System
            * tx_ctcss - transmit - string   | Default: "0000"
            * rx_ctcss - receive - string    | Default"0000"

        Also runs a handshake validation that the Dorji module is working.
        '''

        self.settings = {
            'tx' : "134.0000",
            'rx' : "134.0000",
            'tx_ctcss' : "0000",
            'rx_ctcss' : "0000",
            'gwb' : "0",
            'sq' : "1",
            'device' : "/dev/ttyS0",
            'baud' : "9600",
            'vol' : "1",
        }

        self.settings.update(kwargs)

        print(self.settings['device'],
              self.settings['baud'])


    def __getitem__(self, key):
        if key not in self.settings.keys():
            raise KeyError
        return self.settings[key]

    def __setitem__(self, key, value):
        if key not in self.settings.keys():
            raise KeyError

        self.settings[key] = value
        self.set_dmosetgroup()

    def scan_freq(self,freq):
        '''
        Scans wanted frequency for signal
        Expects: Frequency (xxx.yyyy)
        Returns: boolean
        '''
        if self.ser and freq:
            cmd="S+%s" %(freq)
            print(cmd)


    def send_atcommand(self,cmd):
        '''
        Sends commands via serial.
        Expects: serial device, and command string.

        Returns boolean
        '''
        if cmd:
            print(cmd)

    def set_volume(self,vol):
        '''
        Sets the volume on the dorji chip,

        Expects: serial device, and volume int (1-8)

        Returns boolean
        '''
        if vol:
            if self.send_atcommand('AT+DMOSETVOLUME=%s\r\n' %(volume)):
                return True
            else:
                return False


    def set_filter(self,filter):
        '''
        Used to turn on/off Pre/de-emphasis, lowpass, and highpass filters

        Expects a serial device and dict with:
        {pre_de_emph},{highpass},{lowpass}

        Returns boolean
        '''
        if filter:
            cmd = 'AT+SETFILTER={pre_de_emph},{highpass},{lowpass}\r\n'.format(**filter)

            if self.send_atcommand(cmd):
                return True
            else:
                return False


    def set_dmosetgroup(self):
        '''
        Configure a group of Dorji module options.

        Expects a serial device and a dict with:
        {channel_space},{tx_freq},{rx_freq},{tx_ctcss},{sq},{rx_ctcss}

        Returns a array with [0] - Status, [1] - Message
        '''
        cmd = 'AT+DMOSETGROUP={gwb},{tx},{rx},{tx_ctcss},{sq},{rx_ctcss}\r\n'.format(**self.settings)
        if self.send_atcommand(cmd):
            return True
        else:
            return False


conf = {'tx': "134.0000", 'rx': "134.0000", }

d = dorji(**conf)
d['tx'] = "160.0000"
