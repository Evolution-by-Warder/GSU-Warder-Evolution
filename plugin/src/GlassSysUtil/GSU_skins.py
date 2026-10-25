ok_plugin = """<screen name="GlassSysUtil" position="center,center" size="620,525" title="Glass System Utility" backgroundColor="#31000000" >
		<widget name="list" position="20,0" size="275,400" zPosition="2" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
		<ePixmap position="330,37" zPosition="1" size="227,320" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/sys_util.png" transparent="1"  alphatest="off"/>     
    <eLabel position="0,405" size="620,1" backgroundColor="#888888" zPosition="5" transparent="0" />
		<widget name="info" position="20,410" size="580,75" font="priveG;16" zPosition="4" valign="center" halign="center" foregroundColor="#666666" transparent="1" />                        
    <eLabel position="0,490" size="155,1" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="155,490" size="155,1" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="310,490" size="155,1" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="465,490" size="155,1" backgroundColor="blue" zPosition="5" transparent="0" />
		<widget name="red" position="0,495" size="155,25" font="priveG;20" zPosition="1" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
		<widget name="green" position="155,495" size="155,25" font="priveG;20" zPosition="1" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
		<widget name="yellow" position="310,495" size="155,25" font="priveG;20" zPosition="4" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
		<widget name="blue" position="465,495" size="155,25" font="priveG;20" zPosition="4" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="blue" transparent="1" />
		</screen>"""

no_plugin = """<screen name="GlassSysUtil" position="0,0" size="720,576" title="GlassSysUtil" backgroundColor="#31000000" flags="wfNoBorder" >                 
              <eLabel text="This plugin works only with HD,Full HD or Ultra HD skin" font="priveG;22" position="130,260" size="450,30" halign="center"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>            
      	      </screen>"""

GlassSysInfo = """<screen name="GlassSysInfo" position="0,0" size="1280,720" title="GlassSysInfo" backgroundColor="#31000000" flags="wfNoBorder" >

                      <widget name="mem_labels" font="priveG;16" position="50,50" zPosition="0" size="100,100" valign="top" halign="left" backgroundColor="#31000000" foregroundColor="#666666" transparent="1" />
                      <widget name="ram" font="priveG;16" position="155,50" zPosition="3" size="90,100" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="swap" font="priveG;16" position="255,50" zPosition="3" size="90,100" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="mem_tot" font="priveG;16" position="355,50" zPosition="4" size="90,100" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />      
                      <widget name="root" font="priveG;16" position="455,50" zPosition="5" size="90,100" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="membar" position="145,70" size="5,75" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="swapbar" position="245,70" size="5,75" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="memtotalbar" position="345,70" size="5,75" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="rootbar" position="445,70" size="5,75" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar_back.png" position="145,70" size="5,75" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar_back.png" position="245,70" size="5,75" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar_back.png" position="345,70" size="5,75" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar_back.png" position="445,70" size="5,75" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/devices/mem.png" position="163,170" size="40,80" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/devices/swap.png" position="264,170" size="40,80" zPosition="2" backgroundColor="#31000000" alphatest="off"/>                      
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/devices/summ.png" position="359,170" size="40,80" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/devices/root.png" position="460,170" size="40,80" zPosition="2" backgroundColor="#31000000" alphatest="off"/>

                      <widget name="space_labels" font="priveG;16" position="50,250" zPosition="0" size="100,100" valign="top" halign="left" backgroundColor="#31000000" foregroundColor="#666666" transparent="1" />
                      <widget name="hdd" font="priveG;16" position="155,250" zPosition="3" size="90,100" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="usb" font="priveG;16" position="255,250" zPosition="4" size="90,100" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />      
                      <widget name="cf" font="priveG;16" position="355,250" zPosition="5" size="90,100" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />      
                      <widget name="sd" font="priveG;16" position="455,250" zPosition="5" size="90,100" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="hddbar" position="145,270" size="5,75" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="usbbar" position="245,270" size="5,75" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="cfbar" position="345,270" size="5,75" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="sdbar" position="445,270" size="5,75" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar_back.png" position="145,270" size="5,75" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar_back.png" position="245,270" size="5,75" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar_back.png" position="345,270" size="5,75" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/bar_back.png" position="445,270" size="5,75" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/devices/hdd.png" position="163,370" size="40,80" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/devices/usb.png" position="264,370" size="40,80" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/devices/cf.png" position="359,370" size="40,80" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/devices/sd.png" position="454,370" size="40,80" zPosition="2" backgroundColor="#31000000" alphatest="off"/>

                      <widget name="HDDCPULabels" noWrap="1" position="50,450" size="100,100" font="priveG;16" halign="left" valign="top" zPosition="0" foregroundColor="#666666" backgroundColor="#31000000" />
                      <widget name="HDDTemperature" noWrap="1" position="133,450" size="110,90" font="priveG;16" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" />
                      <widget name="hdddev" noWrap="1" position="229,450" size="110,90" font="priveG;16" halign="center" valign="top" backgroundColor="#31000000" />
                      <widget name="cpu" font="priveG;16" position="327,450" zPosition="2" size="110,90" valign="top" halign="center" backgroundColor="#31000000" transparent="1" />      
                      <widget name="sensors" font="priveG;16" position="423,450" zPosition="2" size="110,90" valign="top" halign="center" backgroundColor="#31000000" transparent="1" />      
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/devices/hdd_temp.png" position="163,500" size="40,80" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/devices/hdd.png" position="264,500" size="40,80" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/devices/cpu.png" position="359,500" size="40,80" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/devices/sensor.png" position="454,500" size="40,80" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <widget name="hddtempbar" position="145,490" size="5,44" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="hddstate" position="246,490" size="5,44" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="cpubar" position="341,490" size="5,44" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="tempDBbar" position="436,490" size="5,44" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/barm_back.png" position="145,490" size="5,44" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/barm_back.png" position="246,490" size="5,44" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/barm_back.png" position="341,490" size="5,44" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/barm_back.png" position="436,490" size="5,44" zPosition="1" backgroundColor="#31000000" alphatest="on"/>

                      <eLabel text="Protocols:" font="priveG;16" position="50,580" zPosition="1" size="100,100" valign="top" halign="left" backgroundColor="#31000000" foregroundColor="#666666" transparent="1" />
                      <eLabel text="FTP" noWrap="1" position="103,580" size="110,90" font="priveG;16" halign="center" valign="top" backgroundColor="#31000000" />
                      <eLabel text="Telnet" noWrap="1" position="189,580" size="110,90" font="priveG;16" halign="center" valign="top" backgroundColor="#31000000" />
                      <eLabel text="VPN" font="priveG;16" position="277,580" zPosition="2" size="110,90" valign="top" halign="center" backgroundColor="#31000000" transparent="1" />      
                      <eLabel text="Samba" font="priveG;16" position="363,580" zPosition="2" size="110,90" valign="top" halign="center" backgroundColor="#31000000" transparent="1" /> 
                      <eLabel text="NFS" font="priveG;16" position="451,580" zPosition="2" size="110,90" valign="top" halign="center" backgroundColor="#31000000" transparent="1" /> 
                      <widget name="ftp_on" position="148,601" size="20,20" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <widget name="telnet_on" position="234,601" size="20,20" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <widget name="vpn_on" position="322,601" size="20,20" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <widget name="smb_on" position="408,601" size="20,20" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <widget name="nfs_on" position="496,601" size="20,20" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/red.png" position="148,601" size="20,20" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/red.png" position="234,601" size="20,20" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/red.png" position="322,601" size="20,20" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/red.png" position="408,601" size="20,20" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/red.png" position="496,601" size="20,20" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <eLabel position="0,645" size="427,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="427,645" size="426,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="853,645" size="427,1" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,650" size="427,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="427,650" size="426,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;20" position="853,650" size="427,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
                      <widget name="ProccessInfo" position="604,130" size="626,220" font="priveG;16" zPosition="2" halign="left" valign="top" backgroundColor="#31000000" />
                      <widget name="DmesgInfo" position="604,450" size="626,190" font="priveG;16" zPosition="2" halign="left" valign="top" backgroundColor="#31000000" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/lr.png" position="604,50" size="40,80" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/updown.png" position="604,370" size="40,80" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <eLabel text="Process Info" font="priveG;26" position="604,50" size="626,50" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>
                      <eLabel text="Dmesg Info" font="priveG;26" position="604,370" size="626,50" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>
                      
                      </screen>""" 

channelInfo_Center = """<screen name="Channel Info Center" position="0,0" size="1280,720" title="Channel Info Center" backgroundColor="#31000000" flags="wfNoBorder">
                      <eLabel text="ECM Info" font="priveG;26" position="110,80" size="200,80" halign="center" valign="center" foregroundColor="#ff9c00" backgroundColor="#31000000" transparent="1"/>                     
                      <widget name="ecmlabels" font="priveG;16" position="90,165" zPosition="2" size="100,230" foregroundColor="#666666" transparent="1" />
                      <widget name="ecmValues" font="priveG;16" position="185,165" zPosition="3" size="195,230" transparent="1" />

                      <eLabel text="Bitrate" font="priveG;26" position="120,413" size="200,80" halign="center" valign="center" foregroundColor="#ff9c00" backgroundColor="#31000000" transparent="1"/>                     
                      <widget name="bit_labels" font="priveG;16" position="88,498" zPosition="5" size="100,100" foregroundColor="#666666" transparent="1" />
                      <widget name="bit_min" font="priveG;16" position="161,498" zPosition="6" size="90,100" halign="left" transparent="1" />
                      <widget name="bit_max" font="priveG;16" position="219,498" zPosition="7" size="90,100" halign="left" transparent="1" />      
                      <widget name="bit_avg" font="priveG;16" position="277,498" zPosition="8" size="90,100" halign="left" transparent="1" />
                      <widget name="bit_act" font="priveG;16" position="335,498" zPosition="9" size="90,100" halign="left" transparent="1" />
                      <widget name="stream_btr" font="priveG;16" position="161,559" zPosition="10" size="300,22" halign="left" transparent="1" />

                      <eLabel text="Transporder" font="priveG;26" position="865,80" size="300,80" halign="center" valign="center" foregroundColor="#ff9c00" backgroundColor="#31000000" transparent="1"/>                     
                      <widget name="tp_lab_sat" font="priveG;16" position="867,165" zPosition="2" size="134,22" foregroundColor="#666666" transparent="1" />
                      <widget name="tp_sat" font="priveG;16" position="990,165" zPosition="3" halign="left" size="240,44" transparent="1" />
                      <widget name="tp_lab_ref" font="priveG;16" position="867,209" zPosition="2" size="134,22" foregroundColor="#666666" transparent="1" />
                      <widget name="tp_ref" font="priveG;16" position="990,209" zPosition="3" halign="left" size="240,44" transparent="1" />
                      <widget name="tp_lab" font="priveG;16" position="867,253" zPosition="2" size="134,560" foregroundColor="#666666" transparent="1" />
                      <widget name="tp_values" font="priveG;16" position="990,253" zPosition="3" halign="left" size="240,560" transparent="1" />

                      <eLabel text="Signal" font="priveG;26" position="520,413" size="200,80" halign="center" valign="center" foregroundColor="#ff9c00" backgroundColor="#31000000" transparent="1"/>                     
                      <eLabel text="Snr:" font="priveG;16" position="533,516" zPosition="2" size="95,20" halign="left" foregroundColor="#666666" transparent="1" />
                      <widget source="session.FrontendStatus" render="Label" font="priveG;16" position="533,535" zPosition="5" size="70,20" halign="left" transparent="1" >
                      <convert type="FrontendInfo">SNR</convert>
                      </widget>
                      <widget source="session.FrontendStatus" render="Progress" position="518,517" size="5,33" zPosition="4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/barmm.png" orientation="orBottomToTop" transparent="1" >
                      <convert type="FrontendInfo">SNR</convert>
                      </widget>
                      <eLabel text="Agc:" font="priveG;16" position="608,516" zPosition="3" size="95,20" halign="left" foregroundColor="#666666" transparent="1"  />
                      <widget source="session.FrontendStatus" render="Label" font="priveG;16" position="608,535" zPosition="5" size="70,20" halign="left" transparent="1" >
                      <convert type="GSUAgcConv">AgcText</convert>
                      </widget>
                      <widget source="session.FrontendStatus" render="Progress" position="593,517" size="5,33" zPosition="4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/barmm.png" orientation="orBottomToTop" transparent="1" >
                      <convert type="GSUAgcConv">AgcNum</convert>
                      </widget>
                      <eLabel text="Ber:" font="priveG;16" position="683,516" zPosition="4" size="95,20" halign="left" foregroundColor="#666666" transparent="1" />
                      <widget source="session.FrontendStatus" render="Label" 	font="priveG;16" position="683,535" zPosition="5" size="70,20" halign="left" transparent="1"  >
                      <convert type="FrontendInfo">BER</convert> 
                      </widget>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/barmm_back.png" position="518,517" size="5,33" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/barmm_back.png" position="593,517" size="5,33" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/barmm_back.png" position="668,517" size="5,33" zPosition="1" backgroundColor="#31000000" alphatest="off"/>

                      <widget position="0, 20" size="1240,80" source="session.CurrentService" render="Label" font="priveG;38" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
                      <convert type="ServiceName">Name</convert>
                      </widget>
                      <widget source="session.CurrentService" render="Label" position="395,85" size="450,60" font="priveG;26" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="green" shadowOffset="-2,-1" transparent="1">
                       <convert type="ServiceName">Provider</convert>
                      </widget>
                      <widget name="picchannel" position="430,161" size="100,60" zPosition="2" alphatest="on" />
                      <widget name="picprov" position="570,161" size="100,60" zPosition="2" alphatest="on" />
                      <widget name="picsat" position="710,161" size="100,60" zPosition="2" alphatest="on" />
                      <widget name="piccode" position="472,274" size="126,82" zPosition="2" alphatest="on" />
                      <widget name="piccam" position="642,274" size="126,82" zPosition="2" alphatest="on" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/frame.png" position="417,150" size="126,125" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/frame.png" position="557,150" size="126,125" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/frame.png" position="697,150" size="126,125" zPosition="1" backgroundColor="#31000000" alphatest="off"/> 
                      <eLabel position="540,645" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,650" size="1280,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                      
                      </screen>"""

cccam_Info = """<screen name="CCCamMainScreen" position="center,center" size="440,340" title="CCCam Menu" backgroundColor="#31000000" >
                <widget name="server_name" font="priveG;16" position="0,0" zPosition="0" size="440,60" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />      
                <widget name="list" position="20,60" size="400,320" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,300" size="220,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="220,300" size="220,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,305" size="220,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="220,305" size="220,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""

cccam_InfoChoiseServer = """<screen name="CCCamChoiseServer" position="center,center" size="600,388" title="CCCam Server Selection" backgroundColor="#31000000" >
                            <widget name="list" position="20,20" size="560,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,228" size="600,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                            <widget name="server_detailed_labels" position="20,240" size="100,230" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                            <widget name="server_detailed_values" position="115,240" size="395,230" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="0,348" size="300,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="300,348" size="300,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,353" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="300,353" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                            </screen>"""
                            
cccam_servers_Info = """<screen name="ServersInfo" position="center,center" size="600,397" title="Servers Status" backgroundColor="#31000000" >
                        <widget name="list" position="20,20" size="560,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,228" size="600,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="server_detailed_labels" position="20,240" size="100,230" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="server_detailed_values" position="115,240" size="395,230" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="0,352" size="150,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="150,352" size="150,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="300,352" size="150,1" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <eLabel position="450,352" size="150,1" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,357" size="150,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="enaButton" font="priveG;20" position="150,357" size="150,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;20" position="300,357" size="150,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
                      <widget name="disButton" font="priveG;20" position="450,357" size="150,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
             </screen>"""

cccam_providers_Info = """<screen name="ProvidersInfo" position="center,center" size="600,359" title="Providers Info" backgroundColor="#31000000" >
                          <widget name="list" position="20,20" size="560,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
     <eLabel position="0,228" size="600,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                          <widget name="prov_detailed_labels" position="20,240" size="100,210" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                          <widget name="prov_detailed_values" position="115,240" size="395,210" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="200,319" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,324" size="600,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                      
                          </screen>"""                        

cccam_shares_Info = """<screen name="SharesInfo" position="center,center" size="600,385" title="Shares Info" backgroundColor="#31000000" >
                        <widget name="list" position="20,20" size="560,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,228" size="600,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="shares_detailed_labels" position="20,240" size="100,230" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="shares_detailed_values" position="115,240" size="395,230" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="200,348" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,353" size="600,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                      
                        </screen>"""

cccam_clients_Info = """<screen name="ClientsInfo" position="center,center" size="600,405" title="Clients Info" backgroundColor="#31000000" >
                        <widget name="list" position="20,20" size="560,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,228" size="600,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="client_detailed_labels" position="20,240" size="100,230" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="client_detailed_values" position="120,240" size="395,230" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="0,365" size="150,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="150,365" size="150,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="300,365" size="150,1" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <eLabel position="450,365" size="150,1" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,370" size="150,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="enaButton" font="priveG;20" position="150,370" size="150,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;20" position="300,370" size="150,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
                      <widget name="disButton" font="priveG;20" position="450,370" size="150,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                        </screen>"""

cccam_activeClients_Info = """<screen name="ActiveClientsInfo" position="center,center" size="600,400" title="Active Clients Info" backgroundColor="#31000000" >
                        <widget name="list" position="20,20" size="560,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,228" size="600,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="active_client_detailed_labels" position="20,240" size="100,230" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="active_client_detailed_values" position="115,240" size="395,230" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="200,360" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,365" size="600,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                      
                        </screen>"""

cccam_entitlements = """<screen name="Entitlements" position="center,center" size="600,480" title="Local Card(s) Info" backgroundColor="#31000000" >
                        <widget name="entitlements_info"  noWrap="1" position="10,10" size="580,420" font="priveG;16" zPosition="2" halign="left" valign="top" backgroundColor="#31000000" />
                      <eLabel position="200,440" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,445" size="600,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                      
                        </screen>"""

cccam_summary_Info = """<screen name="CccamSumaryInfo" position="center,center" size="470,285" title="Summary information" backgroundColor="#31000000" >
                        <widget name="summary_labels" font="priveG;16" position="30,30" zPosition="1" size="250,260" foregroundColor="#666666" transparent="1" />
                        <widget name="summary_values" font="priveG;16" position="265,30" zPosition="1" size="200,260" transparent="1" />
                      <eLabel position="135,247" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,252" size="470,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                      
                        </screen>"""                        

cccam_providerCardView_Info = """<screen name="Extend view" position="center,center" size="900,420" title="Extend view" backgroundColor="#31000000" >
                                 <widget name="count" font="priveG;20" position="10,5" zPosition="1" size="200,260" transparent="1" />
                                 <widget name="list" position="20,40" size="860,320" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="350,380" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,385" size="900,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                      
                                 </screen>""" 

UCM = """
			<screen name="Glass Cams Manager" position="center,center" size="1020,596" title="UCM" backgroundColor="#31000000" >
			<widget name="config" position="40,2" size="940,62" zPosition="2" backgroundColor="#353e575e" transparent="1" />
			<ePixmap position="20,6" size="10,18" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/left.png" zPosition="3" alphatest="blend" />
			<ePixmap position="990,6" size="10,18" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/right.png" zPosition="3" alphatest="blend" />
			<ePixmap position="20,36" size="10,18" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/left.png" zPosition="3" alphatest="blend" />
			<ePixmap position="990,36" size="10,18" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/right.png" zPosition="3" alphatest="blend" />
   <eLabel position="16,64" size="988,1" backgroundColor="#bbbbbb" zPosition="5" transparent="0" />
			<widget name="commPic" position="20,72" size="14,15" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/white.png" alphatest="blend" />
			<widget name="statPic" position="20,104" size="14,15" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/white.png" alphatest="blend" />
			<widget name="statCamSrvcmd" position="40,70" size="497,23" zPosition="1" font="priveG;20" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
			<widget name="statCamSrvbin" position="40,100" size="497,23" zPosition="1" font="priveG;20" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
   <eLabel position="16,128" size="518,1" backgroundColor="#bbbbbb" zPosition="5" transparent="0" />
			<widget name="CamPic" position="20,144" size="14,15" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/white.png" alphatest="blend" />
			<widget name="SrvPic" position="20,169" size="14,15" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/white.png" alphatest="blend" />
			<widget name="activCam" position="40,141" size="497,23" zPosition="1" font="priveG;20" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
			<widget name="activSrv" position="40,169" size="497,23" zPosition="1" font="priveG;20" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
   <eLabel position="16,197" size="518,1" backgroundColor="#bbbbbb" zPosition="5" transparent="0" />
			<widget name="fullEcmLine" position="14,303" size="523,90" zPosition="1" font="priveG;20" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/frame_hd.png" position="276,214" size="126,82" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/frame_hd.png" position="408,214" size="126,82" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/frame_hd.png" position="145,214" size="126,82" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
			<widget name="picECM" position="14,214"  size="126,82" zPosition="2" alphatest="on" />
      <widget name="picchannel" position="158,226" size="100,60" zPosition="2" alphatest="on" />
      <widget name="picprov" position="289,226" size="100,60" zPosition="2" alphatest="on" />
      <widget name="picsat" position="421,226" size="100,60" zPosition="2" alphatest="on" />
			<widget name="CAID_info" position="14,403" size="523,150" zPosition="1" font="priveG;20" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
      <widget name="txt0" position="594,70" size="444,23" font="priveG;20" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
      <widget name="txt1" position="594,95" size="444,23" font="priveG;20" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt2" position="594,121" size="444,23" zPosition="5" font="priveG;20" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt3" position="594,146" size="444,23" zPosition="5" font="priveG;20" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt4" position="594,172" size="444,23" zPosition="5" font="priveG;20" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt5" position="594,198" size="444,23" zPosition="5" font="priveG;20" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt6" position="594,224" size="444,23" zPosition="5" font="priveG;20" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
      <widget name="txt7" position="594,249" size="444,23" font="priveG;20" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
      <widget name="txt8" position="594,275" size="444,23" font="priveG;20" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
      <widget name="txt9" position="594,300" size="444,23" font="priveG;20" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />

			<widget name="select_pict" position="564,70" size="20,20" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/bp_icons/arrow.png" zPosition="8" alphatest="blend" />
   <eLabel position="594,340" size="416,1" backgroundColor="#bbbbbb" zPosition="5" transparent="0" />
			<widget name="helpTXT" position="594,345" size="416,210" zPosition="1" font="priveG;20" halign="center" valign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel position="0,560" size="254,1" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="254,560" size="255,1" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="510,560" size="254,1" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="764,560" size="254,1" backgroundColor="blue" zPosition="5" transparent="0" />            			  
			<widget name="red" position="0,566" size="254,23" font="priveG;20" valign="top" halign="center" zPosition="1" foregroundColor="red" backgroundColor="#31000000" transparent="1"/>
			<widget name="green" position="254,566" size="255,23" font="priveG;20" valign="top" halign="center" zPosition="1" foregroundColor="green" backgroundColor="#31000000" transparent="1"/>
			<widget name="yellow" position="510,566" size="254,23" font="priveG;20" valign="top" halign="center" zPosition="1" foregroundColor="yellow" backgroundColor="#31000000" transparent="1"/>
			<widget name="blue" position="764,566" size="255,23" font="priveG;20" valign="top" halign="center" zPosition="1" foregroundColor="blue" backgroundColor="#31000000" transparent="1"/>
 			</screen>"""

oscam_start = """<screen name="OscamStartCfg" position="center,80" size="900,600" title="Oscam start cfg" backgroundColor="#31000000" >
	                  <widget name="config" position="20,10" size="860,500" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
                      <widget name="white" position="0,520" size="900,25" font="priveG;20" zPosition="2" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="#888888" transparent="1"/>
                      <eLabel position="0,560" size="450,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="450,560" size="450,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,565" size="450,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="450,565" size="450,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
	                  </screen>"""
                
ipkScript_center = """<screen name="GlassIpkScriptCenter" position="center,center" size="500,360" title="Ipk and Script Manager" backgroundColor="#31000000" >
                        <widget name="list" position="20,20" size="460,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,230" size="500,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="descriptions" position="20,232" size="460,78" font="priveG;16" valign="center" halign="center" foregroundColor="#666666" transparent="1" />
                      <eLabel position="0,320" size="250,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="250,320" size="250,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,325" size="250,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="250,325" size="250,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                        </screen>"""
                
Script_center_scr = """<screen name="GlassScriptCenter" position="center,center" size="900,350" title="Script Center" backgroundColor="#31000000" >
                        <widget name="list" position="20,20" size="860,220" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,250" size="900,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="descriptions" position="20,252" size="860,58" font="priveG;16" valign="center" halign="center" foregroundColor="#666666" transparent="1" />
                      <eLabel position="0,310" size="450,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="450,310" size="450,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,315" size="450,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="450,315" size="450,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""  
                
ipk_center_scr = """<screen name="GlassIpkCenter" position="center,center" size="900,350" title="Ipk Install Center" backgroundColor="#31000000" >
                <widget name="list" position="20,20" size="860,270" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,310" size="450,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="450,310" size="450,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,315" size="450,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="450,315" size="450,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""               

ipk_uninstall_scr = """<screen name="GlassIpkUninstallCenter" position="center,center" size="900,350" title="Ipk Uninstall Center" backgroundColor="#31000000" >
                <widget name="list" position="20,20" size="860,270" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,310" size="450,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="450,310" size="450,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,315" size="450,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="450,315" size="450,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""
                
tar_center_scr = """<screen name="GlassTarCenter" position="center,center" size="900,350" title="Tar Install Center" backgroundColor="#31000000" >
                <widget name="list" position="20,20" size="860,270" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,310" size="450,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="450,310" size="450,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,315" size="450,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="450,315" size="450,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""                
                
oscam_Info = """<screen name="OScamMainScreen" position="center,center" size="540,430" title="OScam Menu" backgroundColor="#31000000" >
                <widget name="server_name" font="priveG;18" position="0,0" zPosition="0" size="540,160" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />      
                <widget name="list" position="20,160" zPosition="1" size="400,190" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                <widget name="info" font="priveG;16" position="150,290" zPosition="3" size="380,100" valign="center" halign="center" backgroundColor="#31000000" transparent="1" />      
                <widget name="logo" position="10,298" zPosition="2" size="160,82" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/oscam.png" backgroundColor="#31000000" alphatest="on" />
                      <eLabel position="0,390" size="270,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="270,390" size="270,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,395" size="270,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="270,395" size="270,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""

oscam_Files_scr = """<screen name="OscamFilesMenu" position="center,center" size="440,435" title="OScam Select Files " backgroundColor="#31000000" >
                <widget name="list" position="20,20" size="400,450" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,395" size="220,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="220,395" size="220,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,400" size="220,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="220,400" size="220,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""

oscam_Files_scr2 = """<screen name="OscamFileShow" position="center,center" size="1100,475" title="Oscam File" backgroundColor="#31000000" >
                        <widget name="file_info" position="10,10" size="1090,415" font="priveG;16" valign="top" backgroundColor="#31000000" halign="left" />
                      <eLabel position="450,435" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,440" size="1100,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                      
                        </screen>"""

oscam_InfoChoiseServer = """<screen name="OScamChoiseServer" position="center,center" size="600,388" title="OScam Server Selection" backgroundColor="#31000000" >
                            <widget name="list" position="20,20" size="560,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,228" size="600,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                            <widget name="server_detailed_labels" position="20,240" size="100,230" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                            <widget name="server_detailed_values" position="115,240" size="395,230" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="0,348" size="300,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="300,348" size="300,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,353" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="300,353" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                            </screen>"""
                            
oscam_Summary_scr = """<screen name="OscamSummary" position="center,center" size="960,575" title="Oscam Summary Info" backgroundColor="#31000000" >
                        <widget name="list" position="20,13" size="920,374" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,398" size="960,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="status_labels_0" position="10,410" size="90,230" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_0" position="100,410" size="400,230" font="priveG;16" halign="left" transparent="1" />
                        <widget name="status_labels_1" position="290,410" size="110,230" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_1" position="390,410" size="400,230" font="priveG;16" halign="left" transparent="1" />
                        <widget name="status_labels_2" position="595,410" size="120,230" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_2" position="695,410" size="400,230" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="0,535" size="480,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="480,535" size="480,1" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,540" size="480,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="blue" font="priveG;20" position="480,540" size="480,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                        </screen>"""
                            
oscam_logInfo_scr = """<screen name="OscamLogInfo" position="center,center" size="1280,720" title="Oscam Log Info" backgroundColor="#31000000" flags="wfNoBorder" >
                        <widget name="log_info" position="50,50" size="1180,620" scrollbarMode="showOnDemand" backgroundColor="#31000000" />                                                
                        </screen>"""

oscam_Readers_scr = """<screen name="OscamReaders" position="center,center" size="900,350" title="Oscam Readers Info" backgroundColor="#31000000" >
                        <widget name="list" position="20,20" size="860,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,228" size="900,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="status_labels_0" position="10,240" size="270,240" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_0" position="280,240" size="170,240" font="priveG;16" halign="left" transparent="1" />
                        <widget name="status_labels_1" position="460,240" size="270,240" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_1" position="730,240" size="170,240" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="0,310" size="300,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="300,310" size="300,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="600,310" size="300,1" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,315" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="300,315" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="blue_button" font="priveG;20" position="600,315" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                        </screen>"""
                        
oscam_Users_scr = """<screen name="OscamUsers" position="center,center" size="960,410" title="Oscam Users Info" backgroundColor="#31000000" >
                        <widget name="list" position="20,20" size="920,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,228" size="960,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="status_labels_0" position="10,240" size="90,230" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_0" position="100,240" size="200,230" font="priveG;16" halign="left" transparent="1" />
                        <widget name="status_labels_1" position="310,240" size="110,230" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_1" position="420,240" size="200,230" font="priveG;16" halign="left" transparent="1" />
                        <widget name="status_labels_2" position="630,240" size="120,230" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_2" position="750,240" size="200,230" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="0,370" size="480,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="480,370" size="480,1" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,375" size="480,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="blue_button" font="priveG;20" position="480,375" size="480,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                        </screen>"""
                        
oscam_Entitlements_scr = """<screen name="Entitlements" position="center,center" size="1280,720" title="Reader Entitlements" flags="wfNoBorder" backgroundColor="#31000000" >
                        <widget name="Crd_info" position="230,60" font="priveG;20" zPosition="1" size="1080,82" valign="center" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
                        <widget name="Crd_system" position="60,60" zPosition="0" size="126,82"  backgroundColor="#31000000" alphatest="on" />
                        <widget name="Host" text="Host" position="60,152" font="priveG;15" zPosition="0" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="CAID" text="CAID" position="340,152" font="priveG;15" zPosition="1" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="System" text="System" position="390,152" font="priveG;15" zPosition="2" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Type" text="Type" position="500,152" font="priveG;14" zPosition="3" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Share ID" text="Share ID" position="540,152" font="priveG;15" zPosition="4" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Remote ID" text="Remote ID" position="640,152" font="priveG;16" zPosition="5" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Up" text="Up" position="740,152" font="priveG;15" zPosition="6" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Re" text="Re" position="770,152" font="priveG;15" zPosition="7" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Providers" text="Providers" position="800,152" font="priveG;15" zPosition="8" size="330,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="TypeCRD" text="Type" position="70,152" font="priveG;15" zPosition="1" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="CAIDcrd" text="CAID" position="165,152" font="priveG;15" zPosition="2" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="ProvID" text="ProvID" position="240,152" font="priveG;14" zPosition="3" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="ID" text="ID" position="340,152" font="priveG;15" zPosition="4" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Class" text="Class" position="540,152" font="priveG;16" zPosition="5" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Start Date" text="Start Date" position="690,152" font="priveG;15" zPosition="6" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Expire Date" text="Expire Date" position="845,152" font="priveG;15" zPosition="7" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Name" text="Name" position="1000,152" font="priveG;15" zPosition="7" size="300,20" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="entitlements_list" position="40,172" size="1200,418" zPosition="9" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,610" size="640,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="640,610" size="640,1" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,615" size="640,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="blue" font="priveG;20" position="640,615" size="640,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                        </screen>"""                         

Ecm_Info_scr = """<screen name="ECMInfo" position="center,center" size="350,357" title="ECM Informations" backgroundColor="#31000000" >                        
	               	<widget name="ecmlabels" font="priveG;16" position="20,15" zPosition="2" size="100,260" backgroundColor="#31000000" foregroundColor="#666666" transparent="1" />
                 	<widget name="ecmValues" font="priveG;16" position="116,15" zPosition="3" size="234,260" backgroundColor="#31000000" transparent="1" />
                  <widget name="piccode" position="95,260"  size="160,82" zPosition="4" alphatest="on" />                      
                  </screen>"""                        

OSD_ECM_Menu_scr = """<screen name="OSDECMMenu" position="center,center" size="1000,270" title="OSD Ecm Info setup" backgroundColor="#31000000" >
                      <widget name="config" position="10,0" size="980,170" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <widget name="info" position="20,180" size="960,50" font="priveG;16" valign="center" halign="center" foregroundColor="#888888" transparent="1" />
                      <eLabel position="0,230" size="500,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="500,230" size="500,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,235" size="500,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="500,235" size="500,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      </screen>"""

onScreenEcm_scr = """<screen name="OSDECMInfo" position="1030,70" size="204,34" title="..." flags="wfNoBorder" backgroundColor="#31000000" >
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/frame-1.png" position="0,0" size="204,34" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>                                      
	                 	<widget name="OSD_Ecm_info" font="priveG;18" position="2,5" halign="left" noWrap="1" zPosition="0" size="200,25" backgroundColor="#31000000" transparent="1" />                        
                    </screen>"""

onScreenEcmBig_scr = """<screen name="BigOSDECMInfo" position="1030,70" size="204,174" title="..." flags="wfNoBorder" backgroundColor="#31000000" >                   
                        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/icons/frame-2.png" position="0,0" size="204,174" zPosition="0" backgroundColor="#31000000" alphatest="blend"/>                                      
	                    	<widget name="ecm_items" font="priveG;16" position="10,12" zPosition="2" valign="top" halign="left" size="75,170" backgroundColor="#31000000" transparent="1" />
	                    	<widget name="OSD_Ecm_info" font="priveG;16" position="85,12" zPosition="3" valign="top" halign="left" size="110,170" backgroundColor="#31000000" transparent="1" />                         
                        </screen>"""
                    
mbox_Main = """<screen name="MboxMainScreen" position="center,center" size="960,397" title="Mbox Menu" backgroundColor="#31000000" >
               <widget name="server_name" font="priveG;16" position="0,0" zPosition="0" size="960,45" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />      
               <widget name="list" position="20,45" size="200,110" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,155" size="960,1" backgroundColor="#888888" zPosition="5" transparent="0" />
               <widget name="info" position="10,167" size="940,180" font="priveG;14" valign="center" halign="left" backgroundColor="#31000000" transparent="1" />
                     <eLabel position="0,357" size="480,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="480,357" size="480,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,362" size="480,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="480,362" size="480,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
               </screen>"""
                
mbox_pid_scr = """<screen name="MboxPidInfo" position="center,center" size="400,359" title="Pid Info" backgroundColor="#31000000" >
                  <widget name="list" position="20,20" size="360,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,228" size="400,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                  <widget name="status_labels_0" position="20,240" size="100,210" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                  <widget name="status_values_0" position="115,240" size="395,210" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="100,319" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,324" size="400,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                      
                  </screen>"""                
                
mbox_servers_scr = """<screen name="MboxServerInfo" position="center,center" size="400,359" title="Servers Info" backgroundColor="#31000000" >
                      <widget name="list" position="20,20" size="360,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,228" size="400,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                      <widget name="status_labels_0" position="20,240" size="100,210" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                      <widget name="status_values_0" position="115,240" size="395,210" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="100,319" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,324" size="400,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                      
                      </screen>"""                

mbox_netstat_scr = """<screen name="MboxNetState" position="center,center" size="600,399" title="Net Status" backgroundColor="#31000000" >
                      <widget name="list" position="20,20" size="560,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,228" size="600,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                      <widget name="status_labels_0" position="20,240" size="100,210" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                      <widget name="status_values_0" position="130,240" size="450,210" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="200,359" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,364" size="600,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                      
                      </screen>"""

mbox_share_scr = """<screen name="MboxShare" position="center,center" size="400,419" title="Share Info" backgroundColor="#31000000" >
                    <widget name="list" position="20,20" size="360,196" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,228" size="400,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                    <widget name="status_labels_0" position="20,240" size="100,210" font="priveG;16" halign="left" foregroundColor="#666666" transparent="1" />
                    <widget name="status_values_0" position="115,240" size="395,210" font="priveG;16" halign="left" transparent="1" />
                      <eLabel position="100,379" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,384" size="400,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                      
                    </screen>"""
                        
swap_info = """<screen name="Swap Summary Info" position="center,center" size="900,280" title="Swap info and delete" backgroundColor="#31000000" >
               <eLabel text="Filename:" font="priveG;16" position="20,20" size="250,20" backgroundColor="#31000000"/>
               <eLabel text="Type:" font="priveG;16" position="420,20" size="100,20" backgroundColor="#31000000"/>
               <eLabel text="Size:" font="priveG;16" position="510,20" size="100,20" backgroundColor="#31000000"/>
               <eLabel text="Used:" font="priveG;16" position="620,20" size="100,20" backgroundColor="#31000000"/>
               <eLabel text="Priority:" font="priveG;16" position="710,20" size="80,20" backgroundColor="#31000000"/>
               <widget name="list" position="20,40" size="760,100" scrollbarMode="showOnDemand" backgroundColor="#31000000" zPosition="2"  />
                     <eLabel position="0,240" size="300,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="300,240" size="300,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="600,240" size="300,1" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,245" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="300,245" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;20" position="600,245" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
               </screen>"""
                        
swap_create = """<screen name="Swap create" position="center,100" size="1000,180" title="Swap create" backgroundColor="#31000000" >
                 <widget name="config" position="10,20" size="980,90" zPosition="2" backgroundColor="#353e575e" transparent="1" />
                     <eLabel position="0,140" size="500,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="500,140" size="500,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,145" size="500,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="500,145" size="500,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                 </screen>"""                                                                                                                                                                                

devices_management_main = """<screen name="Devices Management" position="center,center" size="800,395" title="Devices Management" backgroundColor="#31000000" >
    <eLabel position="20,20" size="760,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                 <widget name="devices" position="20,20" size="760,321" scrollbarMode="showOnDemand" />
                      <eLabel position="0,355" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="200,355" size="200,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="400,355" size="200,1" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <eLabel position="600,355" size="200,1" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,360" size="200,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="200,360" size="200,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;20" position="400,360" size="200,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
                      <widget name="button_bg" font="priveG;20" position="600,360" size="200,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                 </screen>"""                            

usbhdd_management = """<screen name="Hdd Management" position="center,center" size="500,382" title="Hdd Management" backgroundColor="#31000000" >
                        <widget name="list" position="20,10" size="275,250" zPosition="2" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                        <ePixmap position="313,18" zPosition="-1" size="145,154" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/devices/hdd2.png" alphatest="off"/>     
    <eLabel position="0,267" size="500,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="info" position="20,269" size="460,75" font="priveG;16" zPosition="4" valign="center" halign="center" foregroundColor="#666666" transparent="1" />
                     <eLabel position="0,342" size="250,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="250,342" size="250,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,347" size="250,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="250,347" size="250,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                        </screen>"""
                        
select_Partition = """<screen name="Select Partition" position="center,center" size="1050,448" title="Select Partition" backgroundColor="#31000000" >
                        <widget name="part" position="40,10" font="priveG;20" zPosition="1" size="170,25" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="mnt" position="190,10" font="priveG;20" zPosition="2" size="200,25" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="start" position="430,10" font="priveG;20" zPosition="3" size="200,25" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="end" position="600,10" font="priveG;20" zPosition="4" size="200,25" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="size" position="770,10" font="priveG;20" zPosition="5" size="120,25" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="id" position="890,10" font="priveG;20" zPosition="6" size="50,25" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="fstype" position="940,10" font="priveG;20" zPosition="7" size="120,25" valign="center" halign="left" backgroundColor="#31000000" />                        
                        <widget name="list" position="0,40" size="1050,350" zPosition="0" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,399" size="262,1" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="262,399" size="263,1" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="525,399" size="262,1" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="787,399" size="263,1" backgroundColor="blue" zPosition="5" transparent="0" />
		<widget name="red" position="0,404" size="262,25" font="priveG;20" zPosition="1" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
		<widget name="green" position="262,404" size="263,25" font="priveG;20" zPosition="1" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
		<widget name="yellow" position="525,404" size="262,25" font="priveG;20" zPosition="4" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
		<widget name="blue" position="787,404" size="263,25" font="priveG;20" zPosition="4" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="blue" transparent="1" />
                        </screen>"""
                        
autoInst_cfg = """<screen name="AutoInstCfg" position="center,160" size="850,180" title="AutoInstall" backgroundColor="#31000000" >
	                  <widget name="config" position="5,20" size="840,90" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
		<widget name="white" position="0,100" size="850,25" font="priveG;20" zPosition="2" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="#888888" transparent="1"/>
    <eLabel position="0,140" size="212,1" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="212,140" size="213,1" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="425,140" size="212,1" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="638,140" size="213,1" backgroundColor="blue" zPosition="5" transparent="0" />
		<widget name="red" position="0,145" size="212,25" font="priveG;20" zPosition="1" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
		<widget name="green" position="212,145" size="213,25" font="priveG;20" zPosition="1" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
		<widget name="yellow" position="425,145" size="212,25" font="priveG;20" zPosition="4" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
		<widget name="blue" position="638,145" size="213,25" font="priveG;20" zPosition="4" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="blue" transparent="1" />
	                  </screen>"""
                                                                    
autoInstStatus_scr = """<screen name="AutoInstState" position="center,center" size="800,380" title="AutoInstall Status" backgroundColor="#31000000" >
                        <widget name="list" position="20,20" size="760,300" zPosition="0" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="300,340" size="200,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,345" size="800,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                      
                        </screen>"""
                        
settings_menu = """<screen name="SettingsMenu" position="center,center" size="600,284" title="Settings/satellites.xml menu" backgroundColor="#31000000" >
                        <widget name="list" position="20,10" size="560,165" zPosition="2" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,175" size="600,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="info" position="20,177" size="560,68" font="priveG;16" zPosition="4" valign="center" halign="center" foregroundColor="#666666" transparent="1" />
                     <eLabel position="0,244" size="300,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="300,244" size="300,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,249" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="300,249" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                        </screen>"""

settings_center_scr = """<screen name="SettingsCenter" position="center,center" size="900,350" title="Please, select zip/rar file with settings" backgroundColor="#31000000" >
                <widget name="list" position="20,20" size="860,270" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                     <eLabel position="0,310" size="450,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="450,310" size="450,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,315" size="450,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="450,315" size="450,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""  
                
cronMng_scr = """<screen position="center,center" size="1020,410" title="Cron Manager" backgroundColor="#31000000" >
                <widget name="list" position="10,4" size="1000,360" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,370" size="204,1" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="204,370" size="204,1" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="408,370" size="204,1" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="612,370" size="204,1" backgroundColor="blue" zPosition="5" transparent="0" />
    <eLabel position="816,370" size="204,1" backgroundColor="white" zPosition="5" transparent="0" />
    <widget name="key_red" position="0,375" zPosition="1" size="204,50" font="priveG;20" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1" />
    <widget name="key_green" position="204,375" zPosition="1" size="204,50" font="priveG;20" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1" />
    <widget name="key_yellow" position="408,375" zPosition="1" size="204,50" font="priveG;20" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
    <widget name="key_blue" position="612,375" zPosition="1" size="204,50" font="priveG;20" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1" />
    <widget name="key_ok" position="816,375" zPosition="1" size="204,50" font="priveG;20" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="white" transparent="1" />
    </screen>"""                

cfgScreen = """<screen name="GSUcfgScreen" position="center,center" size="1000,440" title="GSU configuration" backgroundColor="#31000000" >
    <widget name="config" position="5,10" size="990,380" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
                     <eLabel position="0,400" size="500,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="500,400" size="500,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,405" size="500,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="500,405" size="500,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
	  </screen>"""
	                  
ftpScr = """<screen name="FtpCenter" position="center,center" size="700,384" title="Download menu" backgroundColor="#31000000" >
            <widget name="list" position="20,20" size="660,254" zPosition="2" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,280" size="700,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                     <eLabel position="0,344" size="350,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="350,344" size="350,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,349" size="350,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="350,349" size="350,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
            </screen>"""

cifsNfsScr = """<screen name="createCifsNfs" position="center,100" size="900,280" title="Set parameters for CIFS/NFS" backgroundColor="#31000000" >
			<widget name="config" position="20,20" size="860,200" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
                      <eLabel position="0,240" size="300,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="300,240" size="300,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="600,240" size="300,1" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;20" position="0,245" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;20" position="300,245" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;20" position="600,245" size="300,30" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
	</screen>"""
	
cronScr = """<screen position="center,center" size="1000,560" title="Add Job:" backgroundColor="#31000000" >
	<widget name="config" position="5,5" size="990,400" scrollbarMode="showOnDemand" backgroundColor="#31000000"  />
    <eLabel position="0,520" size="333,1" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="333,520" size="334,1" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="667,520" size="333,1" backgroundColor="white" zPosition="5" transparent="0" />
	<widget name="key_green" position="333,525" zPosition="1" size="334,30" font="priveG;20" halign="center" valign="top" foregroundColor="green" backgroundColor="#31000000"  transparent="1" />
	<widget name="key_red" position="0,525" zPosition="1" size="333,30" font="priveG;20" halign="center" valign="top" foregroundColor="red" backgroundColor="#31000000"  transparent="1" />
		<widget name="key_txt" position="667,525" size="333,30" font="priveG;20" zPosition="4" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="white" transparent="1" />
	</screen>"""
  
txtEdScr = """<screen position="0,0" size="1280,720" title="Txt editor" flags="wfNoBorder" backgroundColor="#31000000" >
						<widget source="Title" render="Label" position="0,50" zPosition="1" size="1280,25" font="priveG;20" halign="center" valign="center" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
						<widget name="txt" position="50,85" size="1180,550" itemHeight="25" transparent="1" backgroundColor="#31000000" zPosition="2" />
                      <eLabel position="0,645" size="426,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="426,645" size="427,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="853,645" size="426,1" backgroundColor="yellow" zPosition="5" transparent="0" />
						<widget name="key_red" position="0,650" zPosition="1" size="426,25" font="priveG;20" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1" />
						<widget name="key_yellow" position="853,650" zPosition="1" size="427,25" font="priveG;20" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
						<widget name="key_green" position="426,650" zPosition="1" size="426,25" font="priveG;20" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1" />
						</screen>"""
            
filebrowser = """<screen name="DirBrowser" position="center,center" size="520,500" title="Dir Browser" backgroundColor="#31000000" >
			<widget name="filelist" position="10,10" size="500,440" scrollbarMode="showOnDemand" />
	<widget source="key_red" render="Label" position="0,465" size="260,33" zPosition="2" valign="top" halign="center" font="priveG;20" transparent="1" foregroundColor="red" />
	<widget source="key_green" render="Label" position="260,465" size="260,33" zPosition="2" valign="top" halign="center" font="priveG;20" transparent="1" foregroundColor="green" />
   <eLabel position="0,460" size="260,1" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="260,460" size="260,1" backgroundColor="green" zPosition="5" transparent="0" />
		</screen>"""               	
