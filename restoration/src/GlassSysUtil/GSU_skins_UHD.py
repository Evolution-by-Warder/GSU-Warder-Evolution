ok_plugin = """<screen name="GlassSysUtil" position="center,center" size="1860,1580" title="Glass System Utility" backgroundColor="#31000000" >
		<widget name="list" position="60,0" size="824,1200" zPosition="2" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
		<ePixmap position="990,110" zPosition="1" size="680,960" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/sys_util.png" transparent="1"  alphatest="off"/>     
    <eLabel position="0,1215" size="1860,4" backgroundColor="#888888" zPosition="5" transparent="0" />
		<widget name="info" position="60,1220" size="1740,240" font="priveG;50" zPosition="4" valign="center" halign="center" foregroundColor="#666666" transparent="1" />                        
    <eLabel position="0,1466" size="465,4" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="465,1466" size="465,4" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="930,1466" size="465,4" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="1395,1466" size="465,4" backgroundColor="blue" zPosition="5" transparent="0" />
		<widget name="red" position="0,1486" size="465,74" font="priveG;60" zPosition="1" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
		<widget name="green" position="465,1486" size="465,74" font="priveG;60" zPosition="1" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
		<widget name="yellow" position="930,1486" size="465,74" font="priveG;60" zPosition="4" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
		<widget name="blue" position="1395,1486" size="465,74" font="priveG;60" zPosition="4" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="blue" transparent="1" />
		</screen>"""

no_plugin = """<screen name="GlassSysUtil" position="0,0" size="2160,1728" title="GlassSysUtil" backgroundColor="#31000000" flags="wfNoBorder" >                 
              <eLabel text="This plugin works only with HD,Full HD or Ultra HD skin" font="priveG;66" position="390,780" size="1350,90" halign="center"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>            
      	      </screen>"""

GlassSysInfo = """<screen name="GlassSysInfo" position="0,0" size="3840,2160" title="GlassSysInfo" backgroundColor="#31000000" flags="wfNoBorder" >

                      <widget name="mem_labels" font="priveG;50" position="150,150" zPosition="0" size="300,300" valign="top" halign="left" backgroundColor="#31000000" foregroundColor="#666666" transparent="1" />
                      <widget name="ram" font="priveG;50" position="464,150" zPosition="3" size="270,300" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="swap" font="priveG;50" position="764,150" zPosition="3" size="270,300" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="mem_tot" font="priveG;50" position="1064,150" zPosition="4" size="270,300" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />      
                      <widget name="root" font="priveG;50" position="1364,150" zPosition="5" size="270,300" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="membar" position="434,210" size="14,224" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="swapbar" position="734,210" size="14,224" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="memtotalbar" position="1034,210" size="14,224" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="rootbar" position="1334,210" size="14,224" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar_back.png" position="434,210" size="14,224" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar_back.png" position="734,210" size="14,224" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar_back.png" position="1034,210" size="14,224" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar_back.png" position="1334,210" size="14,224" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/devices/mem.png" position="488,510" size="120,240" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/devices/swap.png" position="792,510" size="120,240" zPosition="2" backgroundColor="#31000000" alphatest="off"/>                      
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/devices/summ.png" position="1076,510" size="120,240" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/devices/root.png" position="1362,510" size="120,240" zPosition="2" backgroundColor="#31000000" alphatest="off"/>

                      <widget name="space_labels" font="priveG;50" position="150,750" zPosition="0" size="300,300" valign="top" halign="left" backgroundColor="#31000000" foregroundColor="#666666" transparent="1" />
                      <widget name="hdd" font="priveG;50" position="464,750" zPosition="3" size="270,300" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="usb" font="priveG;50" position="764,750" zPosition="4" size="270,300" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />      
                      <widget name="cf" font="priveG;50" position="1064,750" zPosition="5" size="270,300" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />      
                      <widget name="sd" font="priveG;50" position="1364,750" zPosition="5" size="270,300" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="hddbar" position="434,810" size="14,224" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="usbbar" position="734,810" size="14,224" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="cfbar" position="1034,810" size="14,224" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="sdbar" position="1334,810" size="14,224" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar_back.png" position="434,810" size="14,224" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar_back.png" position="734,810" size="14,224" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar_back.png" position="1034,810" size="14,224" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bar_back.png" position="1334,810" size="14,224" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/devices/hdd.png" position="488,1110" size="120,240" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/devices/usb.png" position="792,1110" size="120,240" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/devices/cf.png" position="1076,1110" size="120,240" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/devices/sd.png" position="1362,1110" size="120,240" zPosition="2" backgroundColor="#31000000" alphatest="off"/>

                      <widget name="HDDCPULabels" noWrap="1" position="150,1350" size="300,300" font="priveG;50" halign="left" valign="top" zPosition="0" foregroundColor="#666666" backgroundColor="#31000000" />
                      <widget name="HDDTemperature" noWrap="1" position="398,1350" size="330,270" font="priveG;50" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" />
                      <widget name="hdddev" noWrap="1" position="686,1350" size="330,270" font="priveG;50" halign="center" valign="top" backgroundColor="#31000000" />
                      <widget name="cpu" font="priveG;50" position="980,1350" zPosition="2" size="330,270" valign="top" halign="center" backgroundColor="#31000000" transparent="1" />      
                      <widget name="sensors" font="priveG;50" position="1268,1350" zPosition="2" size="330,270" valign="top" halign="center" backgroundColor="#31000000" transparent="1" />      
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/devices/hdd_temp.png" position="488,1500" size="120,240" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/devices/hdd.png" position="792,1500" size="120,240" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/devices/cpu.png" position="1076,1500" size="120,240" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/devices/sensor.png" position="1362,1500" size="120,240" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <widget name="hddtempbar" position="434,1470" size="14,132" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="hddstate" position="738,1470" size="14,132" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="cpubar" position="1022,1470" size="14,132" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="tempDBbar" position="1308,1470" size="14,132" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/barm_back.png" position="434,1470" size="14,132" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/barm_back.png" position="738,1470" size="14,132" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/barm_back.png" position="1022,1470" size="14,132" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/barm_back.png" position="1308,1470" size="14,132" zPosition="1" backgroundColor="#31000000" alphatest="on"/>

                      <eLabel text="Protocols:" font="priveG;50" position="150,1740" zPosition="1" size="300,300" valign="top" halign="left" backgroundColor="#31000000" foregroundColor="#666666" transparent="1" />
                      <eLabel text="FTP" noWrap="1" position="308,1740" size="330,270" font="priveG;50" halign="center" valign="top" backgroundColor="#31000000" />
                      <eLabel text="Telnet" noWrap="1" position="566,1740" size="330,270" font="priveG;50" halign="center" valign="top" backgroundColor="#31000000" />
                      <eLabel text="VPN" font="priveG;50" position="830,1740" zPosition="2" size="330,270" valign="top" halign="center" backgroundColor="#31000000" transparent="1" />      
                      <eLabel text="Samba" font="priveG;50" position="1088,1740" zPosition="2" size="330,270" valign="top" halign="center" backgroundColor="#31000000" transparent="1" /> 
                      <eLabel text="NFS" font="priveG;50" position="1352,1740" zPosition="2" size="330,270" valign="top" halign="center" backgroundColor="#31000000" transparent="1" /> 
                      <widget name="ftp_on" position="444,1822" size="60,60" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <widget name="telnet_on" position="702,1822" size="60,60" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <widget name="vpn_on" position="966,1822" size="60,60" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <widget name="smb_on" position="1224,1822" size="60,60" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <widget name="nfs_on" position="1488,1822" size="60,60" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/red.png" position="444,1822" size="60,60" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/red.png" position="702,1822" size="60,60" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/red.png" position="966,1822" size="60,60" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/red.png" position="1224,1822" size="60,60" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/red.png" position="1488,1822" size="60,60" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <eLabel position="0,1950" size="1280,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1280,1950" size="1280,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="2560,1950" size="1280,4" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1970" size="1280,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="1280,1970" size="1280,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;60" position="2560,1970" size="1280,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
                      <widget name="ProccessInfo" position="1812,390" size="1878,660" font="priveG;50" zPosition="2" halign="left" valign="top" backgroundColor="#31000000" />
                      <widget name="DmesgInfo" position="1812,1350" size="1878,590" font="priveG;50" zPosition="2" halign="left" valign="top" backgroundColor="#31000000" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/lr.png" position="1812,150" size="120,240" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/updown.png" position="1812,1110" size="120,240" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <eLabel text="Process Info" font="priveG;78" position="1812,150" size="1878,150" halign="center"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>
                      <eLabel text="Dmesg Info" font="priveG;78" position="1812,1110" size="1878,150" halign="center"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>
                      
                      </screen>""" 

channelInfo_Center = """<screen name="Channel Info Center" position="0,0" size="3840,2160" title="Channel Info Center" backgroundColor="#31000000" flags="wfNoBorder">
                      <eLabel text="ECM Info" font="priveG;78" position="330,240" size="600,240" halign="center" valign="center" foregroundColor="#ff9c00" backgroundColor="#31000000" transparent="1"/>                     
                      <widget name="ecmlabels" font="priveG;50" position="270,494" zPosition="2" size="300,690" foregroundColor="#666666" transparent="1" />
                      <widget name="ecmValues" font="priveG;50" position="554,494" zPosition="3" size="584,690" transparent="1" />

                      <eLabel text="Bitrate" font="priveG;78" position="360,1238" size="600,240" halign="center" valign="center" foregroundColor="#ff9c00" backgroundColor="#31000000" transparent="1"/>                     
                      <widget name="bit_labels" font="priveG;50" position="264,1494" zPosition="5" size="300,300" foregroundColor="#666666" transparent="1" />
                      <widget name="bit_min" font="priveG;50" position="488,1494" zPosition="6" size="270,300" halign="left" transparent="1" />
                      <widget name="bit_max" font="priveG;50" position="662,1494" zPosition="7" size="270,300" halign="left" transparent="1" />      
                      <widget name="bit_avg" font="priveG;50" position="836,1494" zPosition="8" size="270,300" halign="left" transparent="1" />
                      <widget name="bit_act" font="priveG;50" position="1010,1494" zPosition="9" size="270,300" halign="left" transparent="1" />
                      <widget name="stream_btr" font="priveG;50" position="488,1674" zPosition="10" size="900,60" halign="left" transparent="1" />

                      <eLabel text="Transporder" font="priveG;78" position="2594,240" size="900,240" halign="center" valign="center" foregroundColor="#ff9c00" backgroundColor="#31000000" transparent="1"/>                     
                      <widget name="tp_lab_sat" font="priveG;50" position="2600,494" zPosition="2" size="400,55" foregroundColor="#666666" transparent="1" />
                      <widget name="tp_sat" font="priveG;50" position="2970,494" zPosition="3" halign="left" size="770,120" transparent="1" />
                      <widget name="tp_lab_ref" font="priveG;50" position="2600,614" zPosition="2" size="400,55" foregroundColor="#666666" transparent="1" />
                      <widget name="tp_ref" font="priveG;50" position="2970,614" zPosition="3" halign="left" size="770,120" transparent="1" />
                      <widget name="tp_lab" font="priveG;50" position="2600,734" zPosition="2" size="400,1680" foregroundColor="#666666" transparent="1" />
                      <widget name="tp_values" font="priveG;50" position="2970,734" zPosition="3" halign="left" size="770,1680" transparent="1" />

                      <eLabel text="Signal" font="priveG;78" position="1560,1238" size="600,240" halign="center" valign="center" foregroundColor="#ff9c00" backgroundColor="#31000000" transparent="1"/>                     
                      <eLabel text="Snr:" font="priveG;50" position="1598,1548" zPosition="2" size="284,60" halign="left" foregroundColor="#666666" transparent="1" />
                      <widget source="session.FrontendStatus" render="Label" font="priveG;50" position="1598,1604" zPosition="5" size="210,60" halign="left" transparent="1" >
                      <convert type="FrontendInfo">SNR</convert>
                      </widget>
                      <widget source="session.FrontendStatus" render="Progress" position="1554,1550" size="14,98" zPosition="4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/barmm.png" orientation="orBottomToTop" transparent="1" >
                      <convert type="FrontendInfo">SNR</convert>
                      </widget>
                      <eLabel text="Agc:" font="priveG;50" position="1824,1548" zPosition="3" size="284,60" halign="left" foregroundColor="#666666" transparent="1"  />
                      <widget source="session.FrontendStatus" render="Label" font="priveG;50" position="1824,1604" zPosition="5" size="210,60" halign="left" transparent="1" >
                      <convert type="GSUAgcConv">AgcText</convert>
                      </widget>
                      <widget source="session.FrontendStatus" render="Progress" position="1778,1550" size="14,98" zPosition="4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/barmm.png" orientation="orBottomToTop" transparent="1" >
                      <convert type="GSUAgcConv">AgcNum</convert>
                      </widget>
                      <eLabel text="Ber:" font="priveG;50" position="2048,1548" zPosition="4" size="284,60" halign="left" foregroundColor="#666666" transparent="1" />
                      <widget source="session.FrontendStatus" render="Label" font="priveG;50" position="2048,1604" zPosition="5" size="210,60" halign="left" transparent="1"  >
                      <convert type="FrontendInfo">BER</convert> 
                      </widget>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/barmm_back.png" position="1554,1550" size="14,98" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/barmm_back.png" position="1778,1550" size="14,98" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/barmm_back.png" position="2004,1550" size="14,98" zPosition="1" backgroundColor="#31000000" alphatest="off"/>

                      <widget position="0,60" size="3718,240" source="session.CurrentService" render="Label" font="priveG;114" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
                      <convert type="ServiceName">Name</convert>
                      </widget>
                      <widget source="session.CurrentService" render="Label" position="1184,254" size="1350,180" font="priveG;78" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="green" shadowOffset="-2,-1" transparent="1">
                       <convert type="ServiceName">Provider</convert>
                      </widget>
                      <widget name="picchannel" position="1290,482" size="300,180" zPosition="2" alphatest="on" />
                      <widget name="picprov" position="1710,482" size="300,180" zPosition="2" alphatest="on" />
                      <widget name="picsat" position="2130,482" size="300,180" zPosition="2" alphatest="on" />
                      <widget name="piccode" position="1470,886" size="300,180" zPosition="2" alphatest="on" />
                      <widget name="piccam" position="1950,886" size="300,180" zPosition="2" alphatest="on" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/frame.png" position="1250,450" size="378,374" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/frame.png" position="1670,450" size="378,374" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/frame.png" position="2090,450" size="378,374" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/frame.png" position="1430,854" size="378,374" zPosition="0" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/frame.png" position="1910,854" size="378,374" zPosition="0" backgroundColor="#31000000" alphatest="off"/>
                      <eLabel position="1620,1950" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1970" size="3840,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                      </screen>"""

cccam_Info = """<screen name="CCCamMainScreen" position="center,center" size="1320,1110" title="CCCam Menu" backgroundColor="#31000000" >
                <widget name="server_name" font="priveG;50" position="0,0" zPosition="0" size="1320,180" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />      
                <widget name="list" position="60,180" size="1200,960" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,900" size="660,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="660,900" size="660,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,920" size="660,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="660,920" size="660,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""

cccam_InfoChoiseServer = """<screen name="CCCamChoiseServer" position="center,center" size="1800,1134" title="CCCam Server Selection" backgroundColor="#31000000" >
                            <widget name="list" position="60,60" size="1680,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,684" zPosition="3" size="1800,4" backgroundColor="#888888" transparent="0" />
                            <widget name="server_detailed_labels" position="60,720" size="300,690" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                            <widget name="server_detailed_values" position="344,720" size="1184,690" font="priveG;50" halign="left" transparent="1" />
                      <eLabel position="0,1044" size="900,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="900,1044" size="900,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1064" size="900,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="900,1064" size="900,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                            </screen>"""
                            
cccam_servers_Info = """<screen name="ServersInfo" position="center,center" size="1800,1166" title="Servers Status" backgroundColor="#31000000" >
                        <widget name="list" position="60,60" size="1680,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,684" zPosition="3" size="1800,4" backgroundColor="#888888" transparent="0" />
                        <widget name="server_detailed_labels" position="60,720" size="300,690" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="server_detailed_values" position="344,720" size="1184,690" font="priveG;50" halign="left" transparent="1" />
                      <eLabel position="0,1056" size="450,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="450,1056" size="450,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="900,1056" size="450,4" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <eLabel position="1350,1056" size="450,4" backgroundColor="blue" zPosition="5" transparent="0" /> 
                      <widget name="red" font="priveG;60" position="0,1076" size="450,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="enaButton" font="priveG;60" position="450,1076" size="450,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;60" position="900,1076" size="450,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
                      <widget name="disButton" font="priveG;60" position="1350,1076" size="450,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                        </screen>"""

cccam_providers_Info = """<screen name="ProvidersInfo" position="center,center" size="1800,1066" title="Providers Info" backgroundColor="#31000000" >
                          <widget name="list" position="60,60" size="1680,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,684" zPosition="3" size="1800,4" backgroundColor="#888888" transparent="0" />
                          <widget name="prov_detailed_labels" position="60,720" size="300,630" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                          <widget name="prov_detailed_values" position="344,720" size="1184,630" font="priveG;50" halign="left" transparent="1" />
                       <eLabel position="600,956" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,976" size="1800,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                          </screen>"""                        

cccam_shares_Info = """<screen name="SharesInfo" position="center,center" size="1800,1154" title="Shares Info" backgroundColor="#31000000" >
                        <widget name="list" position="60,60" size="1680,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,684" zPosition="3" size="1800,4" backgroundColor="#888888" transparent="0" />
                        <widget name="shares_detailed_labels" position="60,720" size="300,690" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="shares_detailed_values" position="344,720" size="1184,690" font="priveG;50" halign="left" transparent="1" />
                       <eLabel position="600,1044" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1064" size="1800,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                        </screen>"""

cccam_clients_Info = """<screen name="ClientsInfo" position="center,center" size="1800,1204" title="Clients Info" backgroundColor="#31000000" >
                        <widget name="list" position="60,60" size="1680,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,684" zPosition="3" size="1800,4" backgroundColor="#888888" transparent="0" />
                        <widget name="client_detailed_labels" position="60,720" size="300,690" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="client_detailed_values" position="360,720" size="1184,690" font="priveG;50" halign="left" transparent="1" />
                      <eLabel position="0,1094" size="450,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="450,1094" size="450,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="900,1094" size="450,4" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <eLabel position="1350,1094" size="450,4" backgroundColor="blue" zPosition="5" transparent="0" /> 
                      <widget name="red" font="priveG;60" position="0,1114" size="450,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="enaButton" font="priveG;60" position="450,1114" size="450,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;60" position="900,1114" size="450,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
                      <widget name="disButton" font="priveG;60" position="1350,1114" size="450,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                        </screen>"""

cccam_activeClients_Info = """<screen name="ActiveClientsInfo" position="center,center" size="1800,1190" title="Active Clients Info" backgroundColor="#31000000" >
                        <widget name="list" position="60,60" size="1680,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,684" zPosition="3" size="1800,4" backgroundColor="#888888" transparent="0" />
                        <widget name="active_client_detailed_labels" position="60,720" size="300,690" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="active_client_detailed_values" position="344,720" size="1184,690" font="priveG;50" halign="left" transparent="1" />
                       <eLabel position="600,1080" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1100" size="1800,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                        </screen>"""

cccam_entitlements = """<screen name="Entitlements" position="center,center" size="1800,1430" title="Local Card(s) Info" backgroundColor="#31000000" >
                        <widget name="entitlements_info"  noWrap="1" position="30,30" size="1740,1260" font="priveG;50" zPosition="2" halign="left" valign="top" backgroundColor="#31000000" />
                       <eLabel position="600,1320" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1340" size="1800,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                        </screen>"""

cccam_summary_Info = """<screen name="CccamSumaryInfo" position="center,center" size="1410,850" title="Summary information" backgroundColor="#31000000" >
                        <widget name="summary_labels" font="priveG;50" position="90,90" zPosition="1" size="750,780" foregroundColor="#666666" transparent="1" />
                        <widget name="summary_values" font="priveG;50" position="794,90" zPosition="1" size="600,780" transparent="1" />
                       <eLabel position="405,740" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,760" size="1410,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                        </screen>"""                        

cccam_providerCardView_Info = """<screen name="Extend view" position="center,center" size="2700,1250" title="Extend view" backgroundColor="#31000000" >
                                 <widget name="count" font="priveG;60" position="30,14" zPosition="1" size="600,780" transparent="1" />
                                 <widget name="list" position="60,120" size="2580,960" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                       <eLabel position="1050,1140" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1160" size="2700,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                                 </screen>""" 

UCM = """
			<screen name="Glass Cams Manager" position="center,center" size="3060,1790" title="UCM" backgroundColor="#31000000" >
			<widget name="config" font="priveG;60" position="120,14" size="2820,164" itemHeight="80" zPosition="2" backgroundColor="#353e575e" transparent="1" />
			<ePixmap position="60,18" size="30,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/left.png" zPosition="3" alphatest="blend" />
			<ePixmap position="2970,18" size="30,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/right.png" zPosition="3" alphatest="blend" />
			<ePixmap position="60,108" size="30,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/left.png" zPosition="3" alphatest="blend" />
			<ePixmap position="2970,108" size="30,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/right.png" zPosition="3" alphatest="blend" />
   <eLabel position="50,192" size="2060,4" backgroundColor="#bbbbbb" zPosition="5" transparent="0" />
			<widget name="commPic" position="60,218" size="44,46" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/white.png" alphatest="blend" />
			<widget name="statPic" position="60,312" size="44,46" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/white.png" alphatest="blend" />
			<widget name="statCamSrvcmd" position="120,210" size="1492,70" zPosition="1" font="priveG;60" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
			<widget name="statCamSrvbin" position="120,300" size="1492,70" zPosition="1" font="priveG;60" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
   <eLabel position="50,386" size="1554,4" backgroundColor="#bbbbbb" zPosition="5" transparent="0" />
			<widget name="CamPic" position="60,432" size="44,46" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/white.png" alphatest="blend" />
			<widget name="SrvPic" position="60,508" size="44,46" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/white.png" alphatest="blend" />
			<widget name="activCam" position="120,424" size="1492,70" zPosition="1" font="priveG;60" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
			<widget name="activSrv" position="120,508" size="1492,70" zPosition="1" font="priveG;60" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
   <eLabel position="50,592" size="1554,4" backgroundColor="#bbbbbb" zPosition="5" transparent="0" />
			<widget name="fullEcmLine" position="42,910" size="1570,280" zPosition="1" font="priveG;60" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/frame_hd.png" position="830,644" size="378,246" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/frame_hd.png" position="1224,644" size="378,246" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/frame_hd.png" position="42,644" size="378,246" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/frame_hd.png" position="436,644" size="378,246" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
			<widget name="picECM" position="81,678"  size="300,180" zPosition="2" alphatest="on" />
      <widget name="picchannel" position="475,678" size="300,180" zPosition="2" alphatest="on" />
      <widget name="picprov" position="869,678" size="300,180" zPosition="2" alphatest="on" />
      <widget name="picsat" position="1263,678" size="300,180" zPosition="2" alphatest="on" />
			<widget name="CAID_info" position="42,1210" size="1570,460" zPosition="1" font="priveG;60" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
      <widget name="txt0" position="1782,210" size="1332,70" font="priveG;60" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
      <widget name="txt1" position="1782,286" size="1332,70" font="priveG;60" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt2" position="1782,364" size="1332,70" zPosition="5" font="priveG;60" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt3" position="1782,440" size="1332,70" zPosition="5" font="priveG;60" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt4" position="1782,518" size="1332,70" zPosition="5" font="priveG;60" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt5" position="1782,594" size="1332,70" zPosition="5" font="priveG;60" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt6" position="1782,672" size="1332,70" zPosition="5" font="priveG;60" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
      <widget name="txt7" position="1782,748" size="1332,70" font="priveG;60" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
      <widget name="txt8" position="1782,826" size="1332,70" font="priveG;60" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
      <widget name="txt9" position="1782,902" size="1332,70" font="priveG;60" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />

			<widget name="select_pict" position="1692,210" size="60,60" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/arrow.png" zPosition="8" alphatest="blend" />
   <eLabel position="1782,1010" size="1248,4" backgroundColor="#bbbbbb" zPosition="5" transparent="0" />
			<widget name="helpTXT" position="1782,1030" size="1248,630" zPosition="1" font="priveG;60" halign="center" valign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel position="0,1680" size="764,4" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="764,1680" size="766,4" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="1530,1680" size="764,4" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="2294,1680" size="764,4" backgroundColor="blue" zPosition="5" transparent="0" />            			  
			<widget name="red" position="0,1700" size="764,70" font="priveG;60" valign="top" halign="center" zPosition="1" foregroundColor="red" backgroundColor="#31000000" transparent="1"/>
			<widget name="green" position="764,1700" size="766,70" font="priveG;60" valign="top" halign="center" zPosition="1" foregroundColor="green" backgroundColor="#31000000" transparent="1"/>
			<widget name="yellow" position="1530,1700" size="764,70" font="priveG;60" valign="top" halign="center" zPosition="1" foregroundColor="yellow" backgroundColor="#31000000" transparent="1"/>
			<widget name="blue" position="2294,1700" size="766,70" font="priveG;60" valign="top" halign="center" zPosition="1" foregroundColor="blue" backgroundColor="#31000000" transparent="1"/>
 			</screen>"""

oscam_start = """<screen name="OscamStartCfg" position="center,240" size="2700,1760" title="Oscam start cfg" backgroundColor="#31000000" >
	                  <widget name="config" font="priveG;60" itemHeight="80" position="60,30" size="2580,1500" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
		<widget name="white" position="0,1550" size="2550,74" font="priveG;60" zPosition="2" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="#888888" transparent="1"/>
                      <eLabel position="0,1670" size="1350,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1350,1670" size="1350,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1690" size="1350,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="1350,1690" size="1350,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
	                  </screen>"""
                
ipkScript_center = """<screen name="GlassIpkScriptCenter" position="center,center" size="1500,1050" title="Ipk and Script Manager" backgroundColor="#31000000" >
                        <widget name="list" position="60,60" size="1380,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,678" zPosition="3" size="1500,4" backgroundColor="#888888" transparent="0" />
                        <widget name="descriptions" position="60,684" size="1380,234" font="priveG;50" valign="center" halign="center" foregroundColor="#666666" transparent="1" />
                      <eLabel position="0,940" size="750,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="750,940" size="750,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,960" size="750,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="750,960" size="750,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                        </screen>"""
                 
Script_center_scr = """<screen name="GlassScriptCenter" position="center,center" size="2700,1050" title="Script Center" backgroundColor="#31000000" >
                        <widget name="list" position="60,60" size="2580,660" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,750" size="2700,4" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="descriptions" position="60,756" size="2580,174" font="priveG;50" valign="center" halign="center" foregroundColor="#666666" transparent="1" />
                      <eLabel position="0,930" size="1350,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1350,930" size="1350,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,944" size="1350,90" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="1350,944" size="1350,90" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""
                
ipk_center_scr = """<screen name="GlassIpkCenter" position="center,center" size="2700,1040" title="Ipk Install Center" backgroundColor="#31000000" >
                <widget name="list" position="60,60" size="2580,810" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,930" size="1350,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1350,930" size="1350,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,950" size="1350,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="1350,950" size="1350,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""               

ipk_uninstall_scr = """<screen name="GlassIpkUninstallCenter" position="center,center" size="2700,1040" title="Ipk Uninstall Center" backgroundColor="#31000000" >
                <widget name="list" position="60,60" size="2580,810" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,930" size="1350,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1350,930" size="1350,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,950" size="1350,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="1350,950" size="1350,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""
                
tar_center_scr = """<screen name="GlassTarCenter" position="center,center" size="2700,1040" title="Tar Install Center" backgroundColor="#31000000" >
                <widget name="list" position="60,60" size="2580,810" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,930" size="1350,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1350,930" size="1350,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,950" size="1350,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="1350,950" size="1350,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""                
                
oscam_Info = """<screen name="OScamMainScreen" position="center,center" size="1620,1280" title="OScam Menu" backgroundColor="#31000000" >
                <widget name="server_name" font="priveG;54" position="0,0" zPosition="0" size="1620,480" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />      
                <widget name="list" position="60,480" zPosition="1" size="1200,570" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                <widget name="info" font="priveG;50" position="450,870" zPosition="3" size="1140,300" valign="center" halign="center" backgroundColor="#31000000" transparent="1" />      
                <widget name="logo" position="30,864" zPosition="2" size="300,180" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/bp_icons/ca_small/oscam.png" backgroundColor="#31000000" alphatest="on" />
                      <eLabel position="0,1170" size="810,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="810,1170" size="810,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1190" size="810,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="810,1190" size="810,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""

oscam_Files_scr = """<screen name="OscamFilesMenu" position="center,center" size="1320,1294" title="OScam Select Files " backgroundColor="#31000000" >
                <widget name="list" position="60,60" size="1200,1350" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,1184" size="660,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="660,1184" size="660,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1204" size="660,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="660,1204" size="660,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""

oscam_Files_scr2 = """<screen name="OscamFileShow" position="center,center" size="3300,1414" title="Oscam File" backgroundColor="#31000000" >
                        <widget name="file_info" position="30,30" size="3270,1244" font="priveG;48" valign="top" backgroundColor="#31000000" halign="left" />
                      <eLabel position="1350,1304" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1324" size="3300,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                        </screen>"""

oscam_InfoChoiseServer = """<screen name="OScamChoiseServer" position="center,center" size="1800,1154" title="OScam Server Selection" backgroundColor="#31000000" >
                            <widget name="list" position="60,60" size="1680,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
        <eLabel position="0,684" zPosition="3" size="1800,4" backgroundColor="#888888" transparent="0" />
                            <widget name="server_detailed_labels" position="60,720" size="300,690" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                            <widget name="server_detailed_values" position="344,720" size="1184,690" font="priveG;50" halign="left" transparent="1" />
                      <eLabel position="0,1044" size="900,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="900,1044" size="900,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1064" size="900,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="900,1064" size="900,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                            </screen>"""
                            
oscam_Summary_scr = """<screen name="OscamSummary" position="center,center" size="2880,1714" title="Oscam Summary Info" backgroundColor="#31000000" >
                        <widget name="list" position="60,38" size="2760,1122" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,1194" zPosition="3" size="2880,4" backgroundColor="#888888" transparent="0" />
                        <widget name="status_labels_0" position="30,1230" size="270,690" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_0" position="300,1230" size="1200,690" font="priveG;50" halign="left" transparent="1" />
                        <widget name="status_labels_1" position="870,1230" size="330,690" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_1" position="1170,1230" size="1200,690" font="priveG;50" halign="left" transparent="1" />
                        <widget name="status_labels_2" position="1784,1230" size="360,690" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_2" position="2084,1230" size="1200,690" font="priveG;50" halign="left" transparent="1" />
                      <eLabel position="0,1604" size="1440,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1440,1604" size="1440,4" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1624" size="1440,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="blue" font="priveG;60" position="1440,1624" size="1440,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                        </screen>"""
                            
oscam_logInfo_scr = """<screen name="OscamLogInfo" position="center,center" size="3840,2160" title="Oscam Log Info" backgroundColor="#31000000" flags="wfNoBorder" >
                        <widget name="log_info" position="150,150" size="3540,1860" scrollbarMode="showOnDemand" backgroundColor="#31000000" />                                                
                        </screen>"""

oscam_Readers_scr = """<screen name="OscamReaders" position="center,center" size="2700,1040" title="Oscam Readers Info" backgroundColor="#31000000" >
                        <widget name="list" position="60,60" size="2580,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,684" zPosition="3" size="2700,4" backgroundColor="#888888" transparent="0" />
                        <widget name="status_labels_0" position="30,720" size="810,720" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_0" position="840,720" size="510,720" font="priveG;50" halign="left" transparent="1" />
                        <widget name="status_labels_1" position="1380,720" size="810,720" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_1" position="2190,720" size="510,720" font="priveG;50" halign="left" transparent="1" />
                      <eLabel position="0,930" size="900,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="900,930" size="900,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="1800,930" size="900,4" backgroundColor="blue" zPosition="5" transparent="0" /> 
                      <widget name="red" font="priveG;60" position="0,950" size="900,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="900,950" size="900,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="blue_button" font="priveG;60" position="1800,950" size="900,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                        </screen>"""
                        
oscam_Users_scr = """<screen name="OscamUsers" position="center,center" size="2880,1220" title="Oscam Users Info" backgroundColor="#31000000" >
                        <widget name="list" position="60,60" size="2760,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,684" zPosition="3" size="2880,4" backgroundColor="#888888" transparent="0" />
                        <widget name="status_labels_0" position="30,720" size="270,690" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_0" position="300,720" size="600,690" font="priveG;50" halign="left" transparent="1" />
                        <widget name="status_labels_1" position="930,720" size="330,690" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_1" position="1260,720" size="600,690" font="priveG;50" halign="left" transparent="1" />
                        <widget name="status_labels_2" position="1890,720" size="360,690" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_2" position="2250,720" size="600,690" font="priveG;50" halign="left" transparent="1" />
                      <eLabel position="0,1110" size="1440,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1440,1110" size="1440,4" backgroundColor="blue" zPosition="5" transparent="0" /> 
                      <widget name="red" font="priveG;60" position="0,1130" size="1440,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="blue_button" font="priveG;60" position="1440,1130" size="1440,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                        </screen>"""
                        
oscam_Entitlements_scr = """<screen name="Entitlements" position="center,center" size="3840,2160" title="Reader Entitlements" flags="wfNoBorder" backgroundColor="#31000000" >
                        <widget name="Crd_info" position="690,148" font="priveG;50" zPosition="1" size="3240,246" valign="center" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
                 	      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/frame_hd.png" position="140,148" size="378,246" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                        <widget name="Crd_system" position="179,181" zPosition="2" size="300,180"  backgroundColor="#31000000" alphatest="on" />
                        <widget name="Host" text="Host" position="180,456" font="priveG;44" zPosition="0" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="CAID" text="CAID" position="1020,456" font="priveG;44" zPosition="1" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="System" text="System" position="1170,456" font="priveG;44" zPosition="2" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Type" text="Type" position="1500,456" font="priveG;42" zPosition="3" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Share ID" text="Share ID" position="1620,456" font="priveG;44" zPosition="4" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Remote ID" text="Remote ID" position="1920,456" font="priveG;50" zPosition="5" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Up" text="Up" position="2220,456" font="priveG;44" zPosition="6" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Re" text="Re" position="2310,456" font="priveG;44" zPosition="7" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Providers" text="Providers" position="2400,456" font="priveG;44" zPosition="8" size="990,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="TypeCRD" text="Type" position="210,456" font="priveG;44" zPosition="1" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="CAIDcrd" text="CAID" position="494,456" font="priveG;44" zPosition="2" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="ProvID" text="ProvID" position="720,456" font="priveG;42" zPosition="3" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="ID" text="ID" position="1020,456" font="priveG;44" zPosition="4" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Class" text="Class" position="1620,456" font="priveG;50" zPosition="5" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Start Date" text="Start Date" position="2070,456" font="priveG;44" zPosition="6" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Expire Date" text="Expire Date" position="2534,456" font="priveG;44" zPosition="7" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Name" text="Name" position="3000,456" font="priveG;44" zPosition="7" size="900,60" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="entitlements_list" position="120,516" size="3600,1254" zPosition="9" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,1830" size="1920,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1920,1830" size="1920,4" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1850" size="1920,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="blue" font="priveG;60" position="1920,1850" size="1920,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                        </screen>""" 
                        
Ecm_Info_scr = """<screen name="ECMInfo" position="center,center" size="1050,1146" title="ECM Informations" backgroundColor="#31000000" >              
	               	<widget name="ecmlabels" font="priveG;48" position="60,44" zPosition="1" size="300,780" backgroundColor="#31000000" foregroundColor="#666666" transparent="1" />
                 	<widget name="ecmValues" font="priveG;48" position="348,44" zPosition="2" size="702,780" backgroundColor="#31000000" transparent="1" />
                 	<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/frame_hd.png" position="336,860" size="378,246" zPosition="3" backgroundColor="#31000000" alphatest="off"/>
                  <widget name="piccode" position="376,892" size="300,180" zPosition="4" alphatest="on" />                        
                  </screen>"""                        

OSD_ECM_Menu_scr = """<screen name="OSDECMMenu" position="center,center" size="3000,800" title="OSD Ecm Info setup" backgroundColor="#31000000" >
                      <widget name="config" font="priveG;60" itemHeight="80" position="20,0" size="2960,480" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <widget name="info" position="60,540" size="2880,150" font="priveG;50" valign="center" halign="center" foregroundColor="#888888" transparent="1" />
                      <eLabel position="0,690" size="1500,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1500,690" size="1500,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,710" size="1500,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="1500,710" size="1500,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      </screen>"""

onScreenEcm_scr = """<screen name="OSDECMInfo" position="3090,210" size="612,102" title="..." flags="wfNoBorder" backgroundColor="#31000000" >
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/frame-1.png" position="0,0" size="612,102" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>                                      
	                 	<widget name="OSD_Ecm_info" font="priveG;54" position="6,14" halign="left" noWrap="1" zPosition="0" size="600,74" backgroundColor="#31000000" transparent="1" />                         
                    </screen>"""

onScreenEcmBig_scr = """<screen name="BigOSDECMInfo" position="3090,210" size="612,522" title="..." flags="wfNoBorder" backgroundColor="#31000000" >                   
                        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/frame-2.png" position="0,0" size="612,522" zPosition="0" backgroundColor="#31000000" alphatest="blend"/>                                      
	                    	<widget name="ecm_items" font="priveG;48" position="30,36" zPosition="2" valign="top" halign="left" size="224,510" backgroundColor="#31000000" transparent="1" />
	                    	<widget name="OSD_Ecm_info" font="priveG;48" position="254,36" zPosition="3" valign="top" halign="left" size="330,510" backgroundColor="#31000000" transparent="1" />                         
                        </screen>"""
                    
mbox_Main = """<screen name="MboxMainScreen" position="center,center" size="2880,1180" title="Mbox Menu" backgroundColor="#31000000" >
               <widget name="server_name" font="priveG;50" position="0,0" zPosition="0" size="2880,134" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />      
               <widget name="list" position="60,134" size="600,330" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,484" zPosition="3" size="2880,4" backgroundColor="#888888" transparent="0" />
               <widget name="info" position="30,500" size="2820,540" font="priveG;42" valign="center" halign="left" backgroundColor="#31000000" transparent="1" />
                      <eLabel position="0,1070" size="1440,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1440,1070" size="1440,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1090" size="1440,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="1440,1090" size="1440,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
               </screen>"""
                
mbox_pid_scr = """<screen name="MboxPidInfo" position="center,center" size="1200,1066" title="Pid Info" backgroundColor="#31000000" >
                  <widget name="list" position="60,60" size="1080,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,684" zPosition="3" size="1200,4" backgroundColor="#888888" transparent="0" />
                  <widget name="status_labels_0" position="60,720" size="300,630" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                  <widget name="status_values_0" position="344,720" size="1184,630" font="priveG;50" halign="left" transparent="1" />
                      <eLabel position="300,956" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,976" size="1200,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                  </screen>"""                
                
mbox_servers_scr = """<screen name="MboxServerInfo" position="center,center" size="1200,1066" title="Servers Info" backgroundColor="#31000000" >
                      <widget name="list" position="60,60" size="1080,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,684" zPosition="3" size="1200,4" backgroundColor="#888888" transparent="0" />
                      <widget name="status_labels_0" position="60,720" size="300,630" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                      <widget name="status_values_0" position="344,720" size="1184,630" font="priveG;50" halign="left" transparent="1" />
                      <eLabel position="300,956" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,976" size="1200,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                      </screen>"""                

mbox_netstat_scr = """<screen name="MboxNetState" position="center,center" size="1800,1186" title="Net Status" backgroundColor="#31000000" >
                      <widget name="list" position="60,60" size="1680,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,684" zPosition="3" size="1800,4" backgroundColor="#888888" transparent="0" />
                      <widget name="status_labels_0" position="60,720" size="300,630" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                      <widget name="status_values_0" position="390,720" size="1350,630" font="priveG;50" halign="left" transparent="1" />
                      <eLabel position="600,1076" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1096" size="1800,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                      </screen>"""

mbox_share_scr = """<screen name="MboxShare" position="center,center" size="1200,1246" title="Share Info" backgroundColor="#31000000" >
                    <widget name="list" position="60,60" size="1080,588" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,684" zPosition="3" size="1200,4" backgroundColor="#888888" transparent="0" />
                    <widget name="status_labels_0" position="60,720" size="300,630" font="priveG;50" halign="left" foregroundColor="#666666" transparent="1" />
                    <widget name="status_values_0" position="344,720" size="1184,630" font="priveG;50" halign="left" transparent="1" />
                      <eLabel position="300,1136" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1156" size="1200,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                    </screen>"""
                        
swap_info = """<screen name="Swap Summary Info" position="center,center" size="2400,830" title="Swap info and delete" backgroundColor="#31000000" >
               <eLabel text="Filename:" font="priveG;50" position="60,60" size="750,60" backgroundColor="#31000000"/>
               <eLabel text="Type:" font="priveG;50" position="1260,60" size="300,60" backgroundColor="#31000000"/>
               <eLabel text="Size:" font="priveG;50" position="1530,60" size="300,60" backgroundColor="#31000000"/>
               <eLabel text="Used:" font="priveG;50" position="1860,60" size="300,60" backgroundColor="#31000000"/>
               <eLabel text="Priority:" font="priveG;50" position="2130,60" size="240,60" backgroundColor="#31000000"/>
               <widget name="list" position="60,120" size="2280,300" scrollbarMode="showOnDemand" backgroundColor="#31000000" zPosition="2"  />
                      <eLabel position="0,720" size="800,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="800,720" size="800,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="1600,720" size="800,4" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,740" size="800,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="800,740" size="800,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;60" position="1600,740" size="800,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
               </screen>"""
                        
swap_create = """<screen name="Swap create" position="center,400" size="3000,530" title="Swap create" backgroundColor="#31000000" >
                 <widget name="config" font="priveG;60" itemHeight="80" position="20,60" size="2960,240" zPosition="2" backgroundColor="#353e575e" transparent="1" />
                      <eLabel position="0,420" size="1500,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1500,420" size="1500,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,440" size="1500,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="1500,440" size="1500,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                 </screen>"""                                                                                                                                                                                

devices_management_main = """<screen name="Devices Management" position="center,center" size="2400,1174" title="Devices Management" backgroundColor="#31000000" >
      <eLabel position="30,60" zPosition="3" size="2340,4" backgroundColor="#888888" transparent="0" />
                 <widget name="devices" position="30,60" size="2340,962" scrollbarMode="showOnDemand" />
                      <eLabel position="0,1064" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="600,1064" size="600,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="1200,1064" size="600,4" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <eLabel position="1800,1064" size="600,4" backgroundColor="blue" zPosition="5" transparent="0" /> 
                      <widget name="red" font="priveG;60" position="0,1084" size="600,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="600,1084" size="600,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;60" position="1200,1084" size="600,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
                      <widget name="button_bg" font="priveG;60" position="1800,1084" size="600,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                 </screen>"""
                 
usbhdd_management = """<screen name="Hdd Management" position="center,center" size="1500,1126" title="Hdd Management" backgroundColor="#31000000" >
                        <widget name="list" position="60,30" size="824,750" zPosition="2" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                        <ePixmap position="938,54" zPosition="-1" size="434,462" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/uhd/devices/hdd2.png" alphatest="off"/>     
      <eLabel position="0,790" zPosition="3" size="1500,4" backgroundColor="#888888" transparent="0" />
                        <widget name="info" position="60,796" size="1380,224" font="priveG;50" zPosition="4" valign="center" halign="center" foregroundColor="#666666" transparent="1" />
                      <eLabel position="0,1016" size="750,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="750,1016" size="750,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1036" size="750,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="750,1036" size="750,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                        </screen>"""
                        
select_Partition = """<screen name="Select Partition" position="center,center" size="3150,1344" title="Select Partition" backgroundColor="#31000000" >
                        <widget name="part" position="120,30" font="priveG;60" zPosition="1" size="510,74" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="mnt" position="570,30" font="priveG;60" zPosition="2" size="600,74" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="start" position="1290,30" font="priveG;60" zPosition="3" size="600,74" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="end" position="1800,30" font="priveG;60" zPosition="4" size="600,74" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="size" position="2310,30" font="priveG;60" zPosition="5" size="360,74" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="id" position="2670,30" font="priveG;60" zPosition="6" size="150,74" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="fstype" position="2820,30" font="priveG;60" zPosition="7" size="360,74" valign="center" halign="left" backgroundColor="#31000000" />                        
                        <widget name="list" position="0,120" size="3150,1050" zPosition="0" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,1196" size="786,2" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="786,1196" size="788,2" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="1574,1196" size="786,2" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="2360,1196" size="788,2" backgroundColor="blue" zPosition="5" transparent="0" />
		<widget name="red" position="0,1212" size="786,74" font="priveG;60" zPosition="1" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
		<widget name="green" position="786,1212" size="788,74" font="priveG;60" zPosition="1" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
		<widget name="yellow" position="1574,1212" size="786,74" font="priveG;60" zPosition="4" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
		<widget name="blue" position="2360,1212" size="788,74" font="priveG;60" zPosition="4" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="blue" transparent="1" />
                        </screen>"""
                        
autoInst_cfg = """<screen name="AutoInstCfg" position="center,480" size="2550,530" title="AutoInstall" backgroundColor="#31000000" >
	                  <widget name="config" font="priveG;60" itemHeight="80" position="10,60" size="2530,270" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
		<widget name="white" position="0,300" size="2550,74" font="priveG;60" zPosition="2" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="#888888" transparent="1"/>
    <eLabel position="0,420" size="637,4" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="637,420" size="638,4" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="1275,420" size="637,4" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="1912,420" size="638,4" backgroundColor="blue" zPosition="5" transparent="0" />
		<widget name="red" position="0,440" size="637,74" font="priveG;60" zPosition="1" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
		<widget name="green" position="637,440" size="638,74" font="priveG;60" zPosition="1" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
		<widget name="yellow" position="1275,440" size="637,74" font="priveG;60" zPosition="4" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
		<widget name="blue" position="1912,440" size="638,74" font="priveG;60" zPosition="4" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="blue" transparent="1" />
	                  </screen>"""
                                                                    
autoInstStatus_scr = """<screen name="AutoInstState" position="center,center" size="2400,1230" title="AutoInstall Status" backgroundColor="#31000000" >
                        <widget name="list" position="60,60" size="2280,900" zPosition="0" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="900,1020" size="600,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1140" size="2400,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                        </screen>"""
                        
settings_menu = """<screen name="SettingsMenu" position="center,center" size="1800,842" title="Settings/satellites.xml menu" backgroundColor="#31000000" >
                        <widget name="list" position="60,30" size="1680,494" zPosition="2" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,524" zPosition="3" size="1800,4" backgroundColor="#888888" transparent="0" />
                        <widget name="info" position="60,530" size="1680,204" font="priveG;50" zPosition="4" valign="center" halign="center" foregroundColor="#666666" transparent="1" />
                      <eLabel position="0,732" size="900,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="900,732" size="900,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,752" size="900,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="900,752" size="900,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                        </screen>"""

settings_center_scr = """<screen name="SettingsCenter" position="center,center" size="2700,1030" title="Please, select zip/rar file with settings" backgroundColor="#31000000" >
                <widget name="list" position="60,60" size="2580,810" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,930" size="1350,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1350,930" size="1350,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,940" size="1350,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="1350,940" size="1350,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""  
                
cronMng_scr = """<screen position="center,center" size="3060,1230" title="Cron Manager" backgroundColor="#31000000" >
                <widget name="list" position="30,12" size="3000,1080" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,1110" size="612,4" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="612,1110" size="612,4" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="1224,1110" size="612,4" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="1836,1110" size="612,4" backgroundColor="blue" zPosition="5" transparent="0" />
    <eLabel position="2448,1110" size="612,4" backgroundColor="white" zPosition="5" transparent="0" />   
    <widget name="key_red" position="0,1130" zPosition="1" size="612,140" font="priveG;60" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1" />
    <widget name="key_green" position="612,1130" zPosition="1" size="612,140" font="priveG;60" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1" />
    <widget name="key_yellow" position="1224,1130" zPosition="1" size="612,140" font="priveG;60" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
    <widget name="key_blue" position="1836,1130" zPosition="1" size="612,140" font="priveG;60" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1" />
    <widget name="key_ok" position="2448,1130" zPosition="1" size="612,140" font="priveG;60" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="white" transparent="1" />
    </screen>"""                

cfgScreen = """<screen name="GSUcfgScreen" position="center,center" size="3000,1310" title="GSU configuration" backgroundColor="#31000000" >
    <widget name="config" font="priveG;60" itemHeight="80" position="10,10" size="2980,1120" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
                      <eLabel position="0,1200" size="1500,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1500,1200" size="1500,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1220" size="1500,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="1500,1220" size="1500,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
	  </screen>"""
	                  
ftpScr = """<screen name="FtpCenter" position="center,center" size="2100,1142" title="Download menu" backgroundColor="#31000000" >
            <widget name="list" position="60,60" size="1980,762" zPosition="2" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
      <eLabel position="0,840" zPosition="3" size="2100,4" backgroundColor="#888888" transparent="0" />
                      <eLabel position="0,1032" size="1050,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1050,1032" size="1050,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1052" size="1050,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="1050,1052" size="1050,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
            </screen>"""

cifsNfsScr = """<screen name="createCifsNfs" position="center,center" size="3000,1230" title="Set parameters for CIFS/NFS" backgroundColor="#31000000" >
			<widget name="config" font="priveG;60" itemHeight="80" position="60,60" size="2880,1000" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
                      <eLabel position="0,1120" size="1000,4" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1000,1120" size="1000,4" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="2000,1120" size="1000,4" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;60" position="0,1140" size="1000,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;60" position="1000,1140" size="1000,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;60" position="2000,1140" size="1000,70" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
	</screen>"""
	
cronScr = """<screen position="center,center" size="3000,1660" title="Add Job:" backgroundColor="#31000000" >
	<widget name="config" font="priveG;60" itemHeight="80" position="10,30" size="2980,1200" scrollbarMode="showOnDemand" backgroundColor="#31000000"  />
    <eLabel position="0,1550" size="1000,4" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="1000,1550" size="1000,4" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="2000,1550" size="1000,4" backgroundColor="white" zPosition="5" transparent="0" />
	<widget name="key_red" position="0,1570" zPosition="1" size="1000,70" font="priveG;60" halign="center" valign="top" foregroundColor="red" backgroundColor="#31000000"  transparent="1" />
	<widget name="key_green" position="1000,1570" zPosition="1" size="1000,70" font="priveG;60" halign="center" valign="top" foregroundColor="green" backgroundColor="#31000000"  transparent="1" />
		<widget name="key_txt" position="2000,1570" size="1000,70" font="priveG;60" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="white" transparent="1"/>
	</screen>"""
  
txtEdScr = """<screen position="0,0" size="3840,2160" title="Txt editor" flags="wfNoBorder" backgroundColor="#31000000" >
						<widget source="Title" render="Label" position="0,150" zPosition="1" size="3840,74" font="priveG;60" halign="center" valign="center" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
						<widget name="txt" font="priveG;60" position="150,254" size="3540,1650" itemHeight="80" transparent="1" backgroundColor="#31000000" zPosition="2" />
                      <eLabel position="0,1934" size="1278,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="1278,1934" size="1280,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="2558,1934" size="1278,2" backgroundColor="yellow" zPosition="5" transparent="0" />
						<widget name="key_red" position="0,1950" zPosition="1" size="1278,74" font="priveG;60" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1" />
						<widget name="key_yellow" position="2558,1950" zPosition="1" size="1280,74" font="priveG;60" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
						<widget name="key_green" position="1278,1950" zPosition="1" size="1278,74" font="priveG;60" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1" />
						</screen>"""
            
filebrowser = """<screen name="DirBrowser" position="center,center" size="1560,1500" title="Dir Browser" backgroundColor="#31000000" >
			<widget name="filelist" position="30,30" size="1500,1320" scrollbarMode="showOnDemand" />
	<widget source="key_red" render="Label" position="0,1400" size="780,70" zPosition="2" valign="top" halign="center" font="priveG;60" transparent="1" foregroundColor="red" />
	<widget source="key_green" render="Label" position="780,1400" size="780,70" zPosition="2" valign="top" halign="center" font="priveG;60" transparent="1" foregroundColor="green" />
   <eLabel position="0,1380" size="780,4" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="780,1380" size="780,4" backgroundColor="green" zPosition="5" transparent="0" />
		</screen>"""               	
