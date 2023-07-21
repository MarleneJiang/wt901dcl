import operator
import clr
clr.AddReference("C:\\Users\\Administrator\\Desktop\\wt901dcl\\wit.dll")
from Wit.Bluetooth.WinBlue import WinBlueManager
from Wit.SDK.Modular.Sensor.Modular.DataProcessor.Constant import WitSensorKey
from Wit.SDK.Modular.WitSensorApi.Modular.BWT901BLE import BWT901BLE
bWT901BLE = BWT901BLE()

def WitBluetoothManager_OnDeviceFound(mac, deviceName):
    global bWT901BLE
    if (deviceName == "" or operator.contains(deviceName, 'WT') == False):
        return
    bWT901BLE.SetMacAddr(mac)
    bWT901BLE.SetDeviceName(deviceName)
    bWT901BLE.Open()
    print("蓝牙已连接！请稍等~")


WitBluetoothManager = WinBlueManager.GetInstance()
WitBluetoothManager.OnDeviceFound += WitBluetoothManager_OnDeviceFound
WitBluetoothManager.StartScan()

def GetDeviceData():
    global bWT901BLE
    result = {}
    result['DeviceName'] = bWT901BLE.GetDeviceName()

    result['AccX'] = bWT901BLE.GetDeviceData(WitSensorKey.AccX)
    result['AccY'] = bWT901BLE.GetDeviceData(WitSensorKey.AccY)
    result['AccZ'] = bWT901BLE.GetDeviceData(WitSensorKey.AccZ)

    result['GyroX'] = bWT901BLE.GetDeviceData(WitSensorKey.AsX)
    result['GyroY'] = bWT901BLE.GetDeviceData(WitSensorKey.AsY)
    result['GyroZ'] = bWT901BLE.GetDeviceData(WitSensorKey.AsZ)

    result['AngleX'] = bWT901BLE.GetDeviceData(WitSensorKey.AngleX)
    result['AngleY'] = bWT901BLE.GetDeviceData(WitSensorKey.AngleY)
    result['AngleZ'] = bWT901BLE.GetDeviceData(WitSensorKey.AngleZ)

    result['MagX'] = bWT901BLE.GetDeviceData(WitSensorKey.HX)
    result['MagY'] = bWT901BLE.GetDeviceData(WitSensorKey.HY)
    result['MagZ'] = bWT901BLE.GetDeviceData(WitSensorKey.HZ)

    result['VersionNumber'] = bWT901BLE.GetDeviceData(WitSensorKey.VersionNumber)

    return result

def are_dicts_almost_equal(dict1, dict2,accuracy=1):
    for key, value in dict1.items():
        if key not in dict2:
            return False

        if key in dict2 and isinstance(value, str) and isinstance(dict2[key], str):
            try:
                value_float = float(value)
                dict2_value_float = float(dict2[key])

                if round(value_float, accuracy) != round(dict2_value_float, accuracy):
                    return False
            except ValueError:
                if value != dict2[key]:
                    return False
        elif dict2[key] != value:
            return False

    # Check if dict2 has any extra keys not present in dict1
    for key in dict2:
        if key not in dict1:
            return False

    return True

history_result = {}
while (1):
    if (bWT901BLE.IsOpen() and bWT901BLE.GetDeviceData(WitSensorKey.VersionNumber)!=None):
        data = GetDeviceData()
        if are_dicts_almost_equal(data, history_result) == False:
            print(data)
        history_result=data