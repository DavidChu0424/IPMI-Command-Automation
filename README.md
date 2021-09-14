1. IPMI Used for Server Project which have BMC chip, it's Intel protocal to control the Server.
2. Archiving some of the IPMI Standard command and OEM commnad that you can used by select the GUI mode to send IPMI command. 
3. Periodical to update the new IPMI command code. 
4. 
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
        
   ***************AMI Command******************** 
