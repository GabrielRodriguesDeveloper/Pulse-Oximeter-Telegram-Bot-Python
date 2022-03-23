import serial


def validHeartRateValue(heart_rate):
    if heart_rate < 90 or heart_rate > 150:
        return True
    return False


def validSpo2Value(spo2):
    if spo2 < 100 and spo2 > 40:
        return True
    return False


def getMaxValues(heart_rate_values, spo2_values):
    max_heart_rate = max(heart_rate_values)
    max_spo2_value = max(spo2_values)
    return max_heart_rate, max_spo2_value


def splitValues(values):
    heart_rate, spo2 = values.split('/')
    spo2 = spo2.split('\r')
    return heart_rate, spo2[0]


def pickValues():
    count = 0
    heart_rate_values = []
    spo2_values = []
    while count < 25:
        while serial_setting.inWaiting():
            values = serial_setting.readline().decode()
            print(values)
            if values not in incorrectValues():
                heart_rate, spo2 = splitValues(values)
                heart_rate_values.append(float(heart_rate))
                spo2_values.append(int(spo2))
                count += 1

    return heart_rate_values, spo2_values

        
def incorrectValues():
    return ["ets Jun  8 2016 00:22:57\r\n", "\r\n", "rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)\r\n", "configsip: 0, SPIWP:0xee\r\n", "clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00\r\n", "clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00\r\n", "mode:DIO, clock div:1\r\n", "load:0x3fff0018,len:4\r\n", "load:0x3fff001c,len:1216\r\n", "ho 0 tail 12 room 4\r\n", "load:0x40078000,len:10944\r\n", "load:0x40080400,len:6388\r\n", "entry 0x400806b4\r\n", "Beat!\r\n"]


serial_setting = serial.Serial('COM6', 115200)