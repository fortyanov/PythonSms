import serial
import time
import sys

class Modem(object):

    def __init__(self):
        self.port_id = 0
        while self.port_id <= 10:
            try:
                self.open(port_id=self.port_id)
                break
            except serial.serialutil.SerialException:
                self.port_id += 1
        if self.port_id >= 10:
            print('Something goes wrong with connection to ports')
            sys.exit(333)
        else:
            self.stat()

    def open(self, port_id):
        self.ser = serial.Serial(port='/dev/ttyUSB%s' % port_id, baudrate=460800, timeout=5)
        self.ser.write('ATZ\r')
        time.sleep(1)
        self.ser.write('AT+CMGF=1\r')
        time.sleep(1)
        self.ser.write('AT+CNMI=2,1,0,0,0\r')
        time.sleep(1)
        self.ser.write('AT+CPMS="ME","ME","ME"\r')


    def stat(self):
        print('--STAT-- \nreadable: %s, writable: %s seekable: %s\nport: %s' %
             (self.ser.readable(), self.ser.writable(), self.ser.seekable(), '/dev/ttyUSB%s' % self.port_id))
        print('all data on port:\n%s' % self.ser.readlines())


    def GetReadSMS(self):
        self.ser.write('AT+CMGL="REC READ"\r')
        #time.sleep(2)
        data = self.ser.readall().strip('\r')
        #print('DATA:\n' + data)
        data_lines = data.splitlines()
        res = {}
        for i, data in enumerate(data_lines):
            if data.startswith('+CMGL'):
                spn = data.find('+7')           # start_phone_number
                key = data[spn:spn + 12]
                value = data_lines[i + 1]
                res[key] = value
        return res


    def GetUnReadSMS(self):
        self.ser.write('AT+CMGL="REC UNREAD"\r')
        time.sleep(2)
        data = self.ser.readall().strip('\r')
        #print('DATA:\n' + data)
        data_lines = data.splitlines()
        res = {}
        for i, data in enumerate(data_lines):
            if data.startswith('+CMGL'):
                spn = data.find('+7')           # start_phone_number
                key = data[spn:spn + 12]
                value = data_lines[i + 1]
                res[key] = value
        return res


    def SendSMS(self, numb, mes):
        self.ser.write('AT+CMGS="%s"\r' % numb)
        time.sleep(1)
        self.ser.write('%s\r' % mes)
        time.sleep(1)
        self.ser.write(chr(26))
        print('SMS sent to %s' % numb)


    def clearMemory(self):
        self.ser.write('AT+CMGD=1,4\r')


    def checkNewSMS(self):
        self.ser.readall()


if __name__ == "__main__":
    m = Modem()
    #print(m.GetReadSMS())
    #print(m.GetUnReadSMS())
    print(m.checkNewSMS())
    #h.SendSMS(numb='+79516490617', mes='time to party')
