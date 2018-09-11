#!/usr/bin/env python

import pyserial

class dorji:
    '''
    A class for managing the Dorji818 chip via serial
    '''

    def __init__(self, **kwargs):
        '''
        Set defaults

        Establish a serial connection to device at baud rate, uses pyserial

          Serial options:
            * baud - Baud rate string        | Default: "9600"
            * device - a device string       | Default: "/dev/ttyS0"
            * timeout - serial timeout       | Defautt: 2

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

        if kwargs['tx']: self.settings['tx'] = kwargs['tx']
        else: self.settings['tx'] = "134.0000"

        if kwargs['rx']: self.settings['rx'] = kwargs['rx']
        else: self.settings['rx'] = "134.0000"

        if kwargs['tx_ctcss']: self.settings['tx_ctcss'] = kwargs['tx_ctcss']
        else: self.settings['tx_ctcss'] = "0000"

        if kwargs['rx_ctcss']: self.settings['rx_ctcss'] = kwargs['rx_ctcss']
        else: self.settings['rx_ctcss'] = "0000"

        if kwargs['sq']: self.settings['sq'] = kwargs['sq']
        else: self.settings['sq'] = "1"

        if kwargs['gwb']: self.settings['gwb'] = kwargs['gwb']
        else: self.settings['gwb'] = "0"

        if kwargs['vol']: self.settings['vol'] = kwargs['vol']
        else: self.settings['vol'] = "1"

        if kwargs['baud']: self.settings['baud'] = kwargs['baud']
        else: self.settings['baud'] = "9600"

        if kwargs['device']: self.settings['device'] = kwargs['device']
        else: self.settings['device'] = "/dev/ttyS0"

        if kwargs['timeout']: self.settings['timeout'] = kwargs['timeout']
        else: self.settings['timeout'] = 2

        self.ser = serial.Serial(self.settings['device'],
                                 self.settings['baud'],
                                 timeout=self.settings['timeout'])

        if not self.send_command('AT+DMOCONNECT\r\n')
            return False
        else:
            return True

    def __getitem__(self, key):
        if key not in self.keys():
            raise KeyError
        return self.settings[key]

    def __setitem__(self, key, value):
        if key not in self.keys():
            raise KeyError
        self.settings[key] = value

    def scan_freq(self,freq):
        '''
        Scans wanted frequency for signal
        Expects: Frequency (xxx.yyyy)
        Returns: boolean
        '''
        if self.ser and freq:
            cmd="S+%s" %(freq)
            self.ser.write(cmd)
            r = self.ser.readline().split("=")[1].rstrip('\r\n')
            if r == "1": return False
            elif r == "0": return True
            else: return False


    def send_atcommand(self,cmd):
        '''
        Sends commands via serial.
        Expects: serial device, and command string.

        Returns boolean
        '''
        if self.ser and cmd:
            self.ser.write(cmd)
            r = self.ser.readline().split(":")[1].rstrip('\r\n')
            if r == "1": return False
            elif r == "0": return True
            else: return False


    def set_volume(self,vol):
        '''
        Sets the volume on the dorji chip,

        Expects: serial device, and volume int (1-8)

        Returns boolean
        '''
        if vol:
            if self.send_atcommand(self.ser,'AT+DMOSETVOLUME=%s\r\n' %(volume)):
                return True
            else:
                return False


    def set_filer(self,filter):
        '''
        Used to turn on/off Pre/de-emphasis, lowpass, and highpass filters

        Expects a serial device and dict with:
        {pre_de_emph},{highpass},{lowpass}

        Returns boolean
        '''
        if filter:
            cmd = 'AT+SETFILTER={pre_de_emph},{highpass},{lowpass}\r\n'.format(**filter)

            if self.send_atcommand(self.ser, cmd):
                return True
            else:
                return False


    def set_settingssetgroup(self,settings):
        '''
        Configure a group of Dorji module options.

        Expects a serial device and a dict with:
        {channel_space},{tx_freq},{rx_freq},{tx_ctcss},{sq},{rx_ctcss}

        Returns a array with [0] - Status, [1] - Message
        '''
        if settings:
            cmd = 'AT+settingsSETGROUP={channel_space},{tx_freq},{rx_freq},{tx_ctcss},{sq},{rx_ctcss}\r\n'.format(**settings))
            if self.send_atcommand(self.ser, cmd):
                return True
            else:
                return False
