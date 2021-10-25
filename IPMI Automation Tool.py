# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 20:30:25 2021

@author: David & Dennis
"""
import os, re
import time

Note = """
   *******************Common**********************
        1.  Get IP Address and MAC Address
        
   *************Standard Command******************
        2   Set Lan Configuration Parameters
        3.  Get Device ID (raw 06 01)
        4.  BMC Cold Reset (raw 06 02)
        5.  Get Self Test Result (raw 06 04)
        6.  Get ACPI Power State (raw 06 07)
        7.  Get Chassis Status
        8.  Set Chassis Status
        9.  BMC Sel elist
        10. BMC Sel clear
        11. Get Device GUID (raw 06 08)
        12. Get Sensor list
        13. Get SDR elist
        14. Get_BMC_Global_Status
        15. Get POH Counter (raw 0x00 0x0f)
        16. Get Sensor Reading (raw 0x04 0x2d 0x SensorNumber)
        17. Get Sensor Event (raw 0x04 0x2b 0x SensorNumber)
        18. Get Watchdog Timer (raw 0x06 0x25)
        19. Reset Watchdog Timer (raw 0x06 0x22)
        20. Set Watchdog Timer (raw 0x06 0x24)
   ***************AMI Command********************
        21. Fan Control (raw 0x3c 0x42 0x01 0x00 0x%)
        22. Flash FRU
        
   ******************Stress**********************
        23. IPMI Cycle Stress (Warm Boot)
           
        """
#------------------------------------ Function ------------------------------------------#

def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

def get_ipaddress_mac():
    cmd = "ipconfig /all"
    result = execCmd(cmd)
    pat1 = re.compile(r"實體位址[\. ]+: ([\w-]+)")
    pat2 = re.compile(r"IPv4 位址[\. ]+: ([\.\d]+)")
    MAC = re.findall(pat1, result)[0] # 找到MAC
    IP = re.findall(pat2, result)[0] # 找到IP
    print("MAC=%s, IP=%s" %(MAC, IP))

def sel_check():
    try:
        cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " sel list"
        result = execCmd(cmd)
        pat1 = re.compile(r'Critical \W*\w*\W*\w*\W*\w*\W*\w*\w*\s*\w*\W*\w*')
        errormsg = re.findall(pat1, result)
        pat2 = re.compile(r'\w*\s*\w*\W*\w*\W*\w* failure \W*\w*')
        failmsg = re.findall(pat2, result)
        print("errormsg = %s \nfailmsg = %s" %(errormsg,failmsg))
        
        if errormsg != []:
            return True
        else:
           return False
            
    except IndexError:
        print("\n Sel check : Sel list not have Critical error \n")
      
def oslinkcheck(osip):     
    try:
        pingip = "ping " + osip 
        result = execCmd(pingip)
        pat1 = re.compile(r"TTL")
        link = re.findall(pat1, result)[0] 
        print("OS boot Ready !")
        check = True
          
    except IndexError:
        check = False
        print("OS booting.....")
          
    return check

def bmclinkcheck(bmcip):     
    try:
        bmcip = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " chassis status" 
        result = execCmd(bmcip)
        pat1 = re.compile(r"System Power")
        link = re.findall(pat1, result)[0] 
        print("\n BMC Connecting !")
        check = True
          
    except IndexError:
        check = False
        print("\n BMC Connect fail")
        exit() 
    return check



def exportTxt(cmdresult, username):
    with open(username + ".txt","w") as f:
      f.write(cmdresult)
      
#------------------------------------ Function ------------------------------------------#


BMCIP = str(input("請輸入BMCIP: \n"))
BMCID = str(input("請輸入BMC User ID: \n"))
BMCPW = str(input("請輸入BMC PW: \n"))

bmclinkcheck(BMCIP)

while 1:
    
  currenttime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
  num = int(input(Note + "\n" + "Input: "))

        
#------------------------------------Standard Command------------------------------------------#
  def set_BMCIP_address():
      StatusNote = """
                  1. Set channel IP address
                  2. Set channel IP netmask
                  """
      select = int(input(StatusNote + "\n"))
      if select == 1:
           print("input: ", select, "\n")
           channel = str(input("請輸入 Channel Number (1 or 2): " + "\n"))
           print("input: " + channel , "\n")
           newip = str(input("請輸入 New IP: " + "\n"))
           cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP + " lan set " + channel + " ipaddr " + newip
           result = execCmd(cmd)
           print("\n" + " Please Reconnect the BMC !!!")
           
      if select == 2:
           print("input: ", select , "\n")
           channel = str(input("請輸入 Channel Number (1 or 2): " + "\n"))
           print("input: ", channel ,"\n")
           newmask = str(input("請輸入 New Mask: " + "\n"))
           cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+ BMCIP + " lan set " + channel + " netmask " + newmask
           result = execCmd(cmd)
           
           
  def get_device_id():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 06 01"
      result = execCmd(cmd)
      print("response: \n\n" + result)

  def cold_reset():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 06 02"
      result = execCmd(cmd)
      print("response: \n\n" + result)

  def get_self_test_result():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 06 04"
      result = execCmd(cmd)
      print("response: \n\n" + result)     

  def get_ACPI_Power_State():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 06 07"
      result = execCmd(cmd)
      print("response: \n\n" + result) 

  def get_Chassis_Status():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " chassis status"
      result = execCmd(cmd)
      print("response: \n\n" + result)

  def set_Chassi_Status():
      StatusNote = """
                  1. Chassis Power On
                  2. Chassis Power Off
                  3. Chassis Power Cycle
                  4. Chassis power Reset
                  5. Chassis power Diag
                   """
      select = int(input(StatusNote + "\n"))

      if select == 1:
           cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " chassis power on"
           result = execCmd(cmd)
           print("response: \n\n" + result)
           
      if select == 2:
           cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " chassis power off"
           result = execCmd(cmd)
           print("response : \n\n" + result)

      if select == 3:
           cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " chassis power cycle"
           result = execCmd(cmd)
           print("response: \n\n" + result)

      if select == 4:
           cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " chassis power reset"
           result = execCmd(cmd)
           print("response: \n\n" + result)

      if select == 5:
           cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " chassis power diag"
           result = execCmd(cmd)
           print("response: \n\n" + result)

  def get_sel_elist():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " sel elist"
      result = execCmd(cmd)
      print("response: \n\n" + result)

  def sel_clear():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " sel clear"
      result = execCmd(cmd)
      print("response: \n\n" + result)

  def get_Device_GUID():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 0x06 0x08"
      result = execCmd(cmd)
      print("response: \n\n" + result) 
      
  def get_sensor_list():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " sensor list"
      result = execCmd(cmd)
      print("response: \n\n" + result) 

  def get_sdr_elist():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " sdr elist"
      result = execCmd(cmd)
      print("response: \n\n" + result)

  def get_bmc_Global_Enables():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 0x06 0x2f"
      result = execCmd(cmd)
      print("response: \n\n" + result)

  def get_POH():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 0x00 0x0f"
      result = execCmd(cmd)
      print("response: \n\n" + result)

  def get_Sensor_Reading():
      sensornumber = str(input("請輸入 Sensor Number: "))
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 0x04 0x2d 0x" + sensornumber
      result = execCmd(cmd)
      print("response: \n\n" + result)

  def get_Sensor_Event():
      sensorevent = str(input("請輸入 Sensor Number: "))
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 0x04 0x2b 0x" + sensornumber
      result = execCmd(cmd)
      print("response: \n\n" + result) 

  def get_Watchdog_timer():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 0x06 0x25"
      result = execCmd(cmd)
      print("response: \n\n" + result)

  def reset_Watchdog_timer():
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 0x06 0x22"
      result = execCmd(cmd)
      print("response: \n\n" + result + "Reset Successfully")    

  def set_Watchdog_timer():
      print("ipmitool raw 0x06 0x24 0xByte1 0xByte2 0xByte3 0xByte4 0xByte5 0xByte6\n")
      byte1 = str(input("Byte1: "))
      byte2 = str(input("Byte2: "))
      byte3 = str(input("Byte3: "))
      byte4 = str(input("Byte4: "))
      byte5 = str(input("Byte5: "))
      byte6 = str(input("Byte6: "))
      print("\n\n")
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 0x06 0x24 " + "0x" + byte1 + " 0x" + byte2 + " 0x" + byte3 + " 0x" + byte4 + " 0x" + byte5 + " 0x" + byte6
      result = execCmd(cmd)
      print("response: \n\n" + result)

#------------------------------------AMI Command------------------------------------------#

  def fan_speed_control():
      speedrateinput = int(input("請輸入想要的風扇轉速 0~100%: "))
      speedrate = hex(speedrateinput)
      cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 0x3c 0x42 0x01 0x00 "+speedrate
      result = execCmd(cmd)
      print("response: \n\n" + result)
      print("風扇轉速已調整為" + str(speedrateinput) + "%")

  def flash_FRU():
      FRU_name = str(input("請輸入FRU名稱: "))
      cmd_unlock = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 0x06 0x05 0x00"
      execCmd(cmd_unlock)

      print("SUT start to flash FRU now...") 
      cmd_flash = "frugen_win64.exe -t FRU -i 0 -r "+FRU_name+" -R -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP
      execCmd(cmd_flash)
      
      cmd_lock = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " raw 0x06 0x05 0x01"
      execCmd(cmd_lock)

      print("Flash successfully, BMC is cold resetting now...") 
      cold_reset()

#------------------------------------AMI Command------------------------------------------#
#------------------------------------- Stress --------------------------------------------#

  def ipmi_power_cycle():
      cycle = int(input("請輸入Cycle圈數: "))
      osip = str(input("請輸入OS IP: "))
      osdelay = int(input("請輸入 OS Delay 時間: "))
      for i in range(1, cycle+1):
                  
          checkresult = oslinkcheck(osip)
          # time.sleep(osdelay)
          sel_check()       
                
          print("第" + str(i) + "圈")
          
          cmd = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " sel list"
          result = execCmd(cmd)
          
          powercycle = "ipmitool.exe -I lanplus -U "+BMCID+" -P "+BMCPW+ " -H "+BMCIP+ " chassis power cycle"
          execCmd(powercycle)

          checkresult = False
          checkpoint = 0

          while checkresult == False:
            while 1==1:                
                checkresult = oslinkcheck(osip)
                if checkresult == True:
                    checkpoint += 1
                if checkpoint == osdelay:
                    break
                
          exportTxt(result, "IPMI_Power_Cycle " + currenttime)
      
#------------------------------------- Stress --------------------------------------------#       

  if __name__ == '__main__':
    
      if num == 1:
          get_ipaddress_mac()

      if num == 2:
          set_BMCIP_address()

      if num == 3:
          get_device_id()

      if num == 4:
          cold_reset()

      if num == 5:
          get_self_test_result()

      if num == 6:
          get_ACPI_Power_State()

      if num == 7:
          get_Chassis_Status()

      if num == 8:
          set_Chassi_Status()

      if num == 9:
          get_sel_elist()

      if num == 10:
          sel_clear()

      if num == 11:
          get_Device_GUID()

      if num == 12:
          get_sensor_list()

      if num == 13:
          get_sdr_elist()
          
      if num == 14:
          get_bmc_Global_Enables()

      if num == 15:
          get_POH()

      if num == 16:
          get_Sensor_Reading()

      if num == 17:
          get_Sensor_Event()

      if num == 18:
          get_Watchdog_timer()

      if num == 19:
          reset_Watchdog_timer()

      if num == 20:
          set_Watchdog_timer()
          
      if num == 21:
          fan_speed_control()

      if num == 22:
          flash_FRU()

      if num == 23:
          ipmi_power_cycle()
          
