from Adafruit_SHT31 import *
import datetime, time, Adafruit_ADS1x15, csv, os, pytz

CSVDIR = "/home/pi/test_Code/localData"
deltaSeconds = 3600
SAMPLEPERIOD = 1
SHT31ADDRESS = 0x44


class DATACOLLECT(object):
    def __init__(self):
        self.adc1 = Adafruit_ADS1x15.ADS1115(address=0x48,busnum=1)
	self.adc2 = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1)
        self.SHT31 = SHT31(address=SHT31ADDRESS)
        self.timeAjust()
        self.makeCSV()

    def timeAjust(self):
        try:
            os.system('sudo htpdate -s -t google.com')
        except:
            return

    def main(self):
        while True:
            self.checkTime()
            self.csvDataWrite()
            time.sleep(SAMPLEPERIOD)

    def csvDataWrite(self):
        temp = self.SHT31.read_temperature()
        humidity = self.SHT31.read_humidity()
  
	CH4_Collector = self.adc1.read_adc(2)
	CH4_1 = self.adc1.read_adc(3)
	CH4_2 = self.adc2.read_adc(0)
	CH4_3 = self.adc2.read_adc(1)
	CH4_4 = self.adc2.read_adc(2)
        CH4_5 = self.adc2.read_adc(3)
        timeStamp = self.getTime()


        with open(self.csvData, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["{:.02f}".format(temp), "{:.02f}".format(humidity), "{:.03f}".format(CH4_Collector), "{:.03f}".format(CH4_1), "{:.03f}".format(CH4_2), "{:.03f}".format(CH4_3),"{:.03f}".format(CH4_4),"{:.03f}".format(CH4_5), timeStamp])

    def makeCSV(self):
        self.csvData = self.getTime() + ".csv"
        dataCST = datetime.datetime.now()
        timeDelta = datetime.timedelta(seconds=deltaSeconds)
        self.dataCET = dataCST + timeDelta

        with open(self.csvData, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["Temp (C)", "Humidity (%)", "CH4_Collector", "CH4_1","CH4_2","CH4_3","CH4_4","CH4_5", "System Time"])

    def getTime(self):
        return str(datetime.datetime.now(pytz.timezone('America/Denver')))

    def checkTime(self):
        if datetime.datetime.now() >= self.dataCET:
            self.dataDump()

    def dataDump(self):
        self.fileMover()
        self.makeCSV()

    def fileMover(self):
        newLocation = os.path.join(CSVDIR, self.csvData)
        os.rename(self.csvData, newLocation)


def programExicute():
    inst1 = DATACOLLECT()
    inst1.main()


if __name__ == "__main__":
    programExicute()
