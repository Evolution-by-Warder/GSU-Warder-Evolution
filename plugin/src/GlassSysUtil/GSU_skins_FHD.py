ok_plugin = """<screen name="GlassSysUtil" position="center,center" size="930,790" title="Glass System Utility" backgroundColor="#31000000" >
		<widget name="list" position="30,0" size="412,600" zPosition="2" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
		<ePixmap position="495,55" zPosition="1" size="340,480" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/sys_util.png" transparent="1"  alphatest="off"/>     
    <eLabel position="0,607" size="930,2" backgroundColor="#888888" zPosition="5" transparent="0" />
		<widget name="info" position="30,610" size="870,120" font="priveG;25" zPosition="4" valign="center" halign="center" foregroundColor="#666666" transparent="1" />                        
    <eLabel position="0,733" size="232,2" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="232,733" size="233,2" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="465,733" size="232,2" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="697,733" size="233,2" backgroundColor="blue" zPosition="5" transparent="0" />
		<widget name="red" position="0,743" size="232,37" font="priveG;30" zPosition="1" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
		<widget name="green" position="232,743" size="233,37" font="priveG;30" zPosition="1" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
		<widget name="yellow" position="465,743" size="232,37" font="priveG;30" zPosition="4" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
		<widget name="blue" position="697,743" size="233,37" font="priveG;30" zPosition="4" valign="center" halign="center" backgroundColor="#31000000" foregroundColor="blue" transparent="1" />
		</screen>"""

no_plugin = """<screen name="GlassSysUtil" position="0,0" size="1080,864" title="GlassSysUtil" backgroundColor="#31000000" flags="wfNoBorder" >                 
              <eLabel text="This plugin works only with HD,Full HD or Ultra HD skin" font="priveG;33" position="195,390" size="675,45" halign="center"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>            
      	      </screen>"""

GlassSysInfo = """<screen name="GlassSysInfo" position="0,0" size="1920,1080" title="GlassSysInfo" backgroundColor="#31000000" flags="wfNoBorder" >

                      <widget name="mem_labels" font="priveG;25" position="75,75" zPosition="0" size="150,150" valign="top" halign="left" backgroundColor="#31000000" foregroundColor="#666666" transparent="1" />
                      <widget name="ram" font="priveG;25" position="232,75" zPosition="3" size="135,150" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="swap" font="priveG;25" position="382,75" zPosition="3" size="135,150" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="mem_tot" font="priveG;25" position="532,75" zPosition="4" size="135,150" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />      
                      <widget name="root" font="priveG;25" position="682,75" zPosition="5" size="135,150" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="membar" position="217,105" size="7,112" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="swapbar" position="367,105" size="7,112" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="memtotalbar" position="517,105" size="7,112" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="rootbar" position="667,105" size="7,112" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar_back.png" position="217,105" size="7,112" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar_back.png" position="367,105" size="7,112" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar_back.png" position="517,105" size="7,112" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar_back.png" position="667,105" size="7,112" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/devices/mem.png" position="244,255" size="60,120" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/devices/swap.png" position="396,255" size="60,120" zPosition="2" backgroundColor="#31000000" alphatest="off"/>                      
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/devices/summ.png" position="538,255" size="60,120" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/devices/root.png" position="690,255" size="60,120" zPosition="2" backgroundColor="#31000000" alphatest="off"/>

                      <widget name="space_labels" font="priveG;25" position="75,375" zPosition="0" size="150,150" valign="top" halign="left" backgroundColor="#31000000" foregroundColor="#666666" transparent="1" />
                      <widget name="hdd" font="priveG;25" position="232,375" zPosition="3" size="135,150" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="usb" font="priveG;25" position="382,375" zPosition="4" size="135,150" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />      
                      <widget name="cf" font="priveG;25" position="532,375" zPosition="5" size="135,150" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />      
                      <widget name="sd" font="priveG;25" position="682,375" zPosition="5" size="135,150" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
                      <widget name="hddbar" position="217,405" size="7,112" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="usbbar" position="367,405" size="7,112" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="cfbar" position="517,405" size="7,112" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="sdbar" position="667,405" size="7,112" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar_back.png" position="217,405" size="7,112" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar_back.png" position="367,405" size="7,112" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar_back.png" position="517,405" size="7,112" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bar_back.png" position="667,405" size="7,112" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/devices/hdd.png" position="244,555" size="60,120" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/devices/usb.png" position="396,555" size="60,120" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/devices/cf.png" position="538,555" size="60,120" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/devices/sd.png" position="681,555" size="60,120" zPosition="2" backgroundColor="#31000000" alphatest="off"/>

                      <widget name="HDDCPULabels" noWrap="1" position="75,675" size="150,150" font="priveG;25" halign="left" valign="top" zPosition="0" foregroundColor="#666666" backgroundColor="#31000000" />
                      <widget name="HDDTemperature" noWrap="1" position="199,675" size="165,135" font="priveG;25" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" />
                      <widget name="hdddev" noWrap="1" position="343,675" size="165,135" font="priveG;25" halign="center" valign="top" backgroundColor="#31000000" />
                      <widget name="cpu" font="priveG;25" position="490,675" zPosition="2" size="165,135" valign="top" halign="center" backgroundColor="#31000000" transparent="1" />      
                      <widget name="sensors" font="priveG;25" position="634,675" zPosition="2" size="165,135" valign="top" halign="center" backgroundColor="#31000000" transparent="1" />      
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/devices/hdd_temp.png" position="244,750" size="60,120" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/devices/hdd.png" position="396,750" size="60,120" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/devices/cpu.png" position="538,750" size="60,120" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/devices/sensor.png" position="681,750" size="60,120" zPosition="2" backgroundColor="#31000000" alphatest="off"/>
                      <widget name="hddtempbar" position="217,735" size="7,66" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="hddstate" position="369,735" size="7,66" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="cpubar" position="511,735" size="7,66" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <widget name="tempDBbar" position="654,735" size="7,66" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/barm.png" orientation="orBottomToTop" zPosition="2" backgroundColor="#41000000" transparent="1" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/barm_back.png" position="217,735" size="7,66" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/barm_back.png" position="369,735" size="7,66" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/barm_back.png" position="511,735" size="7,66" zPosition="1" backgroundColor="#31000000" alphatest="on"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/barm_back.png" position="654,735" size="7,66" zPosition="1" backgroundColor="#31000000" alphatest="on"/>

                      <eLabel text="Protocols:" font="priveG;25" position="75,870" zPosition="1" size="150,150" valign="top" halign="left" backgroundColor="#31000000" foregroundColor="#666666" transparent="1" />
                      <eLabel text="FTP" noWrap="1" position="154,870" size="165,135" font="priveG;25" halign="center" valign="top" backgroundColor="#31000000" />
                      <eLabel text="Telnet" noWrap="1" position="283,870" size="165,135" font="priveG;25" halign="center" valign="top" backgroundColor="#31000000" />
                      <eLabel text="VPN" font="priveG;25" position="415,870" zPosition="2" size="165,135" valign="top" halign="center" backgroundColor="#31000000" transparent="1" />      
                      <eLabel text="Samba" font="priveG;25" position="544,870" zPosition="2" size="165,135" valign="top" halign="center" backgroundColor="#31000000" transparent="1" /> 
                      <eLabel text="NFS" font="priveG;25" position="676,870" zPosition="2" size="165,135" valign="top" halign="center" backgroundColor="#31000000" transparent="1" /> 
                      <widget name="ftp_on" position="222,911" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <widget name="telnet_on" position="351,911" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <widget name="vpn_on" position="483,911" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <widget name="smb_on" position="612,911" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <widget name="nfs_on" position="744,911" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/green.png" zPosition="2" alphatest="blend" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/red.png" position="222,911" size="30,30" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/red.png" position="351,911" size="30,30" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/red.png" position="483,911" size="30,30" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/red.png" position="612,911" size="30,30" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/red.png" position="744,911" size="30,30" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>
                      <eLabel position="0,975" size="640,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="640,975" size="640,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="1280,975" size="640,2" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,985" size="640,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="640,985" size="640,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;30" position="1280,985" size="640,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
                      <widget name="ProccessInfo" position="906,195" size="939,330" font="priveG;25" zPosition="2" halign="left" valign="top" backgroundColor="#31000000" />
                      <widget name="DmesgInfo" position="906,675" size="939,295" font="priveG;25" zPosition="2" halign="left" valign="top" backgroundColor="#31000000" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/lr.png" position="906,75" size="60,120" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/updown.png" position="906,555" size="60,120" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <eLabel text="Process Info" font="priveG;39" position="906,75" size="939,75" halign="center"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>
                      <eLabel text="Dmesg Info" font="priveG;39" position="906,555" size="939,75" halign="center"  backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1"/>
                      
                      </screen>""" 

channelInfo_Center = """<screen name="Channel Info Center" position="0,0" size="1920,1080" title="Channel Info Center" backgroundColor="#31000000" flags="wfNoBorder">
                      <eLabel text="ECM Info" font="priveG;39" position="165,120" size="300,120" halign="center" valign="center" foregroundColor="#ff9c00" backgroundColor="#31000000" transparent="1"/>                     
                      <widget name="ecmlabels" font="priveG;25" position="135,247" zPosition="2" size="150,345" foregroundColor="#666666" transparent="1" />
                      <widget name="ecmValues" font="priveG;25" position="277,247" zPosition="3" size="292,345" transparent="1" />

                      <eLabel text="Bitrate" font="priveG;39" position="180,619" size="300,120" halign="center" valign="center" foregroundColor="#ff9c00" backgroundColor="#31000000" transparent="1"/>                     
                      <widget name="bit_labels" font="priveG;25" position="132,747" zPosition="5" size="150,150" foregroundColor="#666666" transparent="1" />
                      <widget name="bit_min" font="priveG;25" position="244,747" zPosition="6" size="135,150" halign="left" transparent="1" />
                      <widget name="bit_max" font="priveG;25" position="331,747" zPosition="7" size="135,150" halign="left" transparent="1" />      
                      <widget name="bit_avg" font="priveG;25" position="418,747" zPosition="8" size="135,150" halign="left" transparent="1" />
                      <widget name="bit_act" font="priveG;25" position="505,747" zPosition="9" size="135,150" halign="left" transparent="1" />
                      <widget name="stream_btr" font="priveG;25" position="244,839" zPosition="10" size="450,30" halign="left" transparent="1" />

                      <eLabel text="Transporder" font="priveG;39" position="1297,120" size="450,120" halign="center" valign="center" foregroundColor="#ff9c00" backgroundColor="#31000000" transparent="1"/>                     
                      <widget name="tp_lab_sat" font="priveG;25" position="1300,247" zPosition="2" size="200,30" foregroundColor="#666666" transparent="1" />
                      <widget name="tp_sat" font="priveG;25" position="1485,247" zPosition="3" halign="left" size="335,60" transparent="1" />
                      <widget name="tp_lab_ref" font="priveG;25" position="1300,312" zPosition="2" size="200,30" foregroundColor="#666666" transparent="1" />
                      <widget name="tp_ref" font="priveG;25" position="1485,312" zPosition="3" halign="left" size="335,60" transparent="1" />
                      <widget name="tp_lab" font="priveG;25" position="1300,377" zPosition="2" size="200,840" foregroundColor="#666666" transparent="1" />
                      <widget name="tp_values" font="priveG;25" position="1485,377" zPosition="3" halign="left" size="335,840" transparent="1" />

                      <eLabel text="Signal" font="priveG;39" position="780,619" size="300,120" halign="center" valign="center" foregroundColor="#ff9c00" backgroundColor="#31000000" transparent="1"/>                     
                      <eLabel text="Snr:" font="priveG;25" position="799,774" zPosition="2" size="142,30" halign="left" foregroundColor="#666666" transparent="1" />
                      <widget source="session.FrontendStatus" render="Label" font="priveG;25" position="799,802" zPosition="5" size="105,30" halign="left" transparent="1" >
                      <convert type="FrontendInfo">SNR</convert>
                      </widget>
                      <widget source="session.FrontendStatus" render="Progress" position="777,775" size="7,49" zPosition="4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/barmm.png" orientation="orBottomToTop" transparent="1" >
                      <convert type="FrontendInfo">SNR</convert>
                      </widget>
                      <eLabel text="Agc:" font="priveG;25" position="912,774" zPosition="3" size="142,30" halign="left" foregroundColor="#666666" transparent="1"  />
                      <widget source="session.FrontendStatus" render="Label" font="priveG;25" position="912,802" zPosition="5" size="105,30" halign="left" transparent="1" >
                      <convert type="GSUAgcConv">AgcText</convert>
                      </widget>
                      <widget source="session.FrontendStatus" render="Progress" position="889,775" size="7,49" zPosition="4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/barmm.png" orientation="orBottomToTop" transparent="1" >
                      <convert type="GSUAgcConv">AgcNum</convert>
                      </widget>
                      <eLabel text="Ber:" font="priveG;25" position="1024,774" zPosition="4" size="142,30" halign="left" foregroundColor="#666666" transparent="1" />
                      <widget source="session.FrontendStatus" render="Label" font="priveG;25" position="1024,802" zPosition="5" size="105,30" halign="left" transparent="1"  >
                      <convert type="FrontendInfo">BER</convert> 
                      </widget>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/barmm_back.png" position="777,775" size="7,49" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/barmm_back.png" position="889,775" size="7,49" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/barmm_back.png" position="1002,775" size="7,49" zPosition="1" backgroundColor="#31000000" alphatest="off"/>

                      <widget position="0,30" size="1859,120" source="session.CurrentService" render="Label" font="priveG;57" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
                      <convert type="ServiceName">Name</convert>
                      </widget>
                      <widget source="session.CurrentService" render="Label" position="592,127" size="675,90" font="priveG;39" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="green" shadowOffset="-2,-1" transparent="1">
                       <convert type="ServiceName">Provider</convert>
                      </widget>
                      <widget name="picchannel" position="645,241" size="150,90" zPosition="2" alphatest="on" />
                      <widget name="picprov" position="855,241" size="150,90" zPosition="2" alphatest="on" />
                      <widget name="picsat" position="1065,241" size="150,90" zPosition="2" alphatest="on" />
                      <widget name="piccode" position="735,443" size="150,90" zPosition="2" alphatest="on" />
                      <widget name="piccam" position="975,443" size="150,90" zPosition="2" alphatest="on" />
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/frame.png" position="625,225" size="189,187" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/frame.png" position="835,225" size="189,187" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/frame.png" position="1045,225" size="189,187" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/frame.png" position="715,427" size="189,187" zPosition="0" backgroundColor="#31000000" alphatest="off"/> 
                      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/frame.png" position="955,427" size="189,187" zPosition="0" backgroundColor="#31000000" alphatest="off"/>
                      <eLabel position="810,975" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,985" size="1920,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                      </screen>"""

cccam_Info = """<screen name="CCCamMainScreen" position="center,center" size="660,510" title="CCCam Menu" backgroundColor="#31000000" >
                <widget name="server_name" font="priveG;25" position="0,0" zPosition="0" size="660,90" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />      
                <widget name="list" position="30,90" size="600,480" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,450" size="330,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="330,450" size="330,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,460" size="330,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="330,460" size="330,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""

cccam_InfoChoiseServer = """<screen name="CCCamChoiseServer" position="center,center" size="900,582" title="CCCam Server Selection" backgroundColor="#31000000" >
                            <widget name="list" position="30,30" size="840,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
     <eLabel position="0,342" size="900,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                            <widget name="server_detailed_labels" position="30,360" size="150,345" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                            <widget name="server_detailed_values" position="172,360" size="592,345" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="0,522" size="450,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="450,522" size="450,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,532" size="450,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="450,532" size="450,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                            </screen>"""
                            
cccam_servers_Info = """<screen name="ServersInfo" position="center,center" size="900,588" title="Servers Status" backgroundColor="#31000000" >
                        <widget name="list" position="30,30" size="840,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,342" size="900,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="server_detailed_labels" position="30,360" size="150,345" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="server_detailed_values" position="172,360" size="592,345" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="0,528" size="225,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="225,528" size="225,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="450,528" size="225,2" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <eLabel position="675,528" size="225,2" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,538" size="225,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="enaButton" font="priveG;30" position="225,538" size="225,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;30" position="450,538" size="225,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
                      <widget name="disButton" font="priveG;30" position="675,538" size="225,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>                        
                        </screen>"""

cccam_providers_Info = """<screen name="ProvidersInfo" position="center,center" size="900,538" title="Providers Info" backgroundColor="#31000000" >
                          <widget name="list" position="30,30" size="840,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,342" size="900,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                          <widget name="prov_detailed_labels" position="30,360" size="150,315" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                          <widget name="prov_detailed_values" position="172,360" size="592,315" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="300,478" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,488" size="900,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                          </screen>"""                        

cccam_shares_Info = """<screen name="SharesInfo" position="center,center" size="900,582" title="Shares Info" backgroundColor="#31000000" >
                        <widget name="list" position="30,30" size="840,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,342" size="900,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="shares_detailed_labels" position="30,360" size="150,345" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="shares_detailed_values" position="172,360" size="592,345" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="300,522" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,532" size="900,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                        </screen>"""

cccam_clients_Info = """<screen name="ClientsInfo" position="center,center" size="900,607" title="Clients Info" backgroundColor="#31000000" >
                        <widget name="list" position="30,30" size="840,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,342" size="900,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="client_detailed_labels" position="30,360" size="150,345" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="client_detailed_values" position="180,360" size="592,345" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="0,547" size="225,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="225,547" size="225,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="450,547" size="225,2" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <eLabel position="675,547" size="225,2" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,557" size="225,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="enaButton" font="priveG;30" position="225,557" size="225,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;30" position="450,557" size="225,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
                      <widget name="disButton" font="priveG;30" position="675,557" size="225,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>                        
                        </screen>"""

cccam_activeClients_Info = """<screen name="ActiveClientsInfo" position="center,center" size="900,600" title="Active Clients Info" backgroundColor="#31000000" >
                        <widget name="list" position="30,30" size="840,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,342" size="900,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="active_client_detailed_labels" position="30,360" size="150,345" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="active_client_detailed_values" position="172,360" size="592,345" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="300,540" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,550" size="900,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                        </screen>"""

cccam_entitlements = """<screen name="Entitlements" position="center,center" size="900,720" title="Local Card(s) Info" backgroundColor="#31000000" >
                        <widget name="entitlements_info"  noWrap="1" position="15,15" size="870,630" font="priveG;25" zPosition="2" halign="left" valign="top" backgroundColor="#31000000" />
                      <eLabel position="300,660" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,670" size="900,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                        </screen>"""

cccam_summary_Info = """<screen name="CccamSumaryInfo" position="center,center" size="705,430" title="Summary information" backgroundColor="#31000000" >
                        <widget name="summary_labels" font="priveG;25" position="45,45" zPosition="1" size="375,390" foregroundColor="#666666" transparent="1" />
                        <widget name="summary_values" font="priveG;25" position="397,45" zPosition="1" size="300,390" transparent="1" />
                      <eLabel position="302,370" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,380" size="705,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                        </screen>"""                        

cccam_providerCardView_Info = """<screen name="Extend view" position="center,center" size="1350,630" title="Extend view" backgroundColor="#31000000" >
                                 <widget name="count" font="priveG;30" position="15,7" zPosition="1" size="300,390" transparent="1" />
                                 <widget name="list" position="30,60" size="1290,480" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="625,570" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,580" size="1350,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                                 </screen>""" 

UCM = """
			<screen name="Glass Cams Manager" position="center,center" size="1530,895" title="UCM" backgroundColor="#31000000" >
			<widget name="config" font="priveG;30" position="60,7" size="1410,82" itemHeight="40" zPosition="2" backgroundColor="#353e575e" transparent="1" />
			<ePixmap position="30,9" size="15,27" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/left.png" zPosition="3" alphatest="blend" />
			<ePixmap position="1485,9" size="15,27" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/right.png" zPosition="3" alphatest="blend" />
			<ePixmap position="30,54" size="15,27" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/left.png" zPosition="3" alphatest="blend" />
			<ePixmap position="1485,54" size="15,27" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/right.png" zPosition="3" alphatest="blend" />
   <eLabel position="25,96" size="1480,2" backgroundColor="#bbbbbb" zPosition="5" transparent="0" />
			<widget name="commPic" position="30,109" size="22,23" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/white.png" alphatest="blend" />
			<widget name="statPic" position="30,156" size="22,23" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/white.png" alphatest="blend" />
			<widget name="statCamSrvcmd" position="60,105" size="746,35" zPosition="1" font="priveG;30" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
			<widget name="statCamSrvbin" position="60,150" size="746,35" zPosition="1" font="priveG;30" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
   <eLabel position="25,193" size="777,2" backgroundColor="#bbbbbb" zPosition="5" transparent="0" />
			<widget name="CamPic" position="30,216" size="22,23" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/white.png" alphatest="blend" />
			<widget name="SrvPic" position="30,254" size="22,23" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/white.png" alphatest="blend" />
			<widget name="activCam" position="60,212" size="746,35" zPosition="1" font="priveG;30" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
			<widget name="activSrv" position="60,254" size="746,35" zPosition="1" font="priveG;30" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
   <eLabel position="25,296" size="777,2" backgroundColor="#bbbbbb" zPosition="5" transparent="0" />
			<widget name="fullEcmLine" position="21,455" size="785,140" zPosition="1" font="priveG;30" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/frame_hd.png" position="415,322" size="189,123" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/frame_hd.png" position="612,322" size="189,123" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/frame_hd.png" position="21,322" size="189,123" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/frame_hd.png" position="218,322" size="189,123" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
			<widget name="picECM" position="41,339"  size="150,90" zPosition="2" alphatest="on" />
      <widget name="picchannel" position="238,339" size="150,90" zPosition="2" alphatest="on" />
      <widget name="picprov" position="435,339" size="150,90" zPosition="2" alphatest="on" />
      <widget name="picsat" position="632,339" size="150,90" zPosition="2" alphatest="on" />
			<widget name="CAID_info" position="21,605" size="785,230" zPosition="1" font="priveG;30" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
      <widget name="txt0" position="891,105" size="666,35" font="priveG;30" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
      <widget name="txt1" position="891,143" size="666,35" font="priveG;30" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt2" position="891,182" size="666,35" zPosition="5" font="priveG;30" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt3" position="891,220" size="666,35" zPosition="5" font="priveG;30" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt4" position="891,259" size="666,35" zPosition="5" font="priveG;30" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt5" position="891,297" size="666,35" zPosition="5" font="priveG;30" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
			<widget name="txt6" position="891,336" size="666,35" zPosition="5" font="priveG;30" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
      <widget name="txt7" position="891,374" size="666,35" font="priveG;30" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
      <widget name="txt8" position="891,413" size="666,35" font="priveG;30" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />
      <widget name="txt9" position="891,451" size="666,35" font="priveG;30" zPosition="4" valign="center" halign="left" foregroundColor="#ffffff" backgroundColor="#31000000" transparent="1" />

			<widget name="select_pict" position="846,105" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/arrow.png" zPosition="8" alphatest="blend" />
   <eLabel position="891,510" size="624,2" backgroundColor="#bbbbbb" zPosition="5" transparent="0" />
			<widget name="helpTXT" position="891,520" size="624,315" zPosition="1" font="priveG;30" halign="center" valign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-1,-1" transparent="1" />
    <eLabel position="0,840" size="382,2" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="382,840" size="383,2" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="765,840" size="382,2" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="1147,840" size="382,2" backgroundColor="blue" zPosition="5" transparent="0" />            			  
			<widget name="red" position="0,850" size="382,35" font="priveG;30" valign="top" halign="center" zPosition="1" foregroundColor="red" backgroundColor="#31000000" transparent="1"/>
			<widget name="green" position="382,850" size="383,35" font="priveG;30" valign="top" halign="center" zPosition="1" foregroundColor="green" backgroundColor="#31000000" transparent="1"/>
			<widget name="yellow" position="765,850" size="382,35" font="priveG;30" valign="top" halign="center" zPosition="1" foregroundColor="yellow" backgroundColor="#31000000" transparent="1"/>
			<widget name="blue" position="1147,850" size="383,35" font="priveG;30" valign="top" halign="center" zPosition="1" foregroundColor="blue" backgroundColor="#31000000" transparent="1"/>
 			</screen>"""

oscam_start = """<screen name="OscamStartCfg" position="center,120" size="1350,900" title="Oscam start cfg" backgroundColor="#31000000" >
	                  <widget name="config" font="priveG;30" itemHeight="40" position="30,15" size="1290,750" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
		<widget name="white" position="0,780" size="1275,37" font="priveG;30" zPosition="2" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="#888888" transparent="1"/>
                      <eLabel position="0,840" size="675,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="675,840" size="675,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,850" size="675,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="675,850" size="675,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
	                  </screen>"""
                
ipkScript_center = """<screen name="GlassIpkScriptCenter" position="center,center" size="750,530" title="Ipk and Script Manager" backgroundColor="#31000000" >
                        <widget name="list" position="30,30" size="690,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,339" size="750,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="descriptions" position="30,342" size="690,117" font="priveG;25" valign="center" halign="center" foregroundColor="#666666" transparent="1" />
                      <eLabel position="0,470" size="375,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="375,470" size="375,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,480" size="375,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="375,480" size="375,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                        </screen>"""
                 
Script_center_scr = """<screen name="GlassScriptCenter" position="center,center" size="1350,525" title="Script Center" backgroundColor="#31000000" >
                        <widget name="list" position="30,30" size="1290,330" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,375" size="1350,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="descriptions" position="30,378" size="1290,87" font="priveG;25" valign="center" halign="center" foregroundColor="#666666" transparent="1" />
                      <eLabel position="0,465" size="675,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="675,465" size="675,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,472" size="675,45" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="675,472" size="675,45" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""
                                
ipk_center_scr = """<screen name="GlassIpkCenter" position="center,center" size="1350,525" title="Ipk Install Center" backgroundColor="#31000000" >
                <widget name="list" position="30,30" size="1290,405" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,465" size="675,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="675,465" size="675,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,475" size="675,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="675,475" size="675,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""               

ipk_uninstall_scr = """<screen name="GlassIpkUninstallCenter" position="center,center" size="1350,525" title="Ipk Uninstall Center" backgroundColor="#31000000" >
                <widget name="list" position="30,30" size="1290,405" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,465" size="675,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="675,465" size="675,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,475" size="675,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="675,475" size="675,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""
                
tar_center_scr = """<screen name="GlassTarCenter" position="center,center" size="1350,525" title="Tar Install Center" backgroundColor="#31000000" >
                <widget name="list" position="30,30" size="1290,405" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,465" size="675,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="675,465" size="675,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,475" size="675,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="675,475" size="675,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""                
                
oscam_Info = """<screen name="OScamMainScreen" position="center,center" size="810,645" title="OScam Menu" backgroundColor="#31000000" >
                <widget name="server_name" font="priveG;27" position="0,0" zPosition="0" size="810,240" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />      
                <widget name="list" position="30,240" zPosition="1" size="600,285" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                <widget name="info" font="priveG;25" position="225,435" zPosition="3" size="570,150" valign="center" halign="center" backgroundColor="#31000000" transparent="1" />      
                <widget name="logo" position="15,447" zPosition="2" size="150,90" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/bp_icons/ca_small/oscam.png" backgroundColor="#31000000" alphatest="on" />
                      <eLabel position="0,585" size="405,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="405,585" size="405,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,595" size="405,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="405,595" size="405,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""

oscam_Files_scr = """<screen name="OscamFilesMenu" position="center,center" size="660,652" title="OScam Select Files " backgroundColor="#31000000" >
                <widget name="list" position="30,30" size="600,675" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,592" size="330,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="330,592" size="330,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,602" size="330,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="330,602" size="330,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""

oscam_Files_scr2 = """<screen name="OscamFileShow" position="center,center" size="1650,712" title="Oscam File" backgroundColor="#31000000" >
                        <widget name="file_info" position="15,15" size="1635,622" font="priveG;24" valign="top" backgroundColor="#31000000" halign="left" />
                      <eLabel position="675,652" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,662" size="1650,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                        </screen>"""

oscam_InfoChoiseServer = """<screen name="OScamChoiseServer" position="center,center" size="900,582" title="OScam Server Selection" backgroundColor="#31000000" >
                            <widget name="list" position="30,30" size="840,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
     <eLabel position="0,342" size="900,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                             <widget name="server_detailed_labels" position="30,360" size="150,345" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                            <widget name="server_detailed_values" position="172,360" size="592,345" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="0,522" size="450,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="450,522" size="450,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,532" size="450,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="450,532" size="450,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                            </screen>"""
                            
oscam_Summary_scr = """<screen name="OscamSummary" position="center,center" size="1440,862" title="Oscam Summary Info" backgroundColor="#31000000" >
                        <widget name="list" position="30,19" size="1380,561" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,597" size="1440,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="status_labels_0" position="15,615" size="135,345" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_0" position="150,615" size="600,345" font="priveG;25" halign="left" transparent="1" />
                        <widget name="status_labels_1" position="435,615" size="165,345" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_1" position="585,615" size="600,345" font="priveG;25" halign="left" transparent="1" />
                        <widget name="status_labels_2" position="892,615" size="180,345" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_2" position="1042,615" size="600,345" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="0,802" size="720,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="720,802" size="720,2" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,812" size="720,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="blue" font="priveG;30" position="720,812" size="720,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                        </screen>"""
                            
oscam_logInfo_scr = """<screen name="OscamLogInfo" position="center,center" size="1920,1080" title="Oscam Log Info" backgroundColor="#31000000" flags="wfNoBorder" >
                        <widget name="log_info" position="75,75" size="1770,930" scrollbarMode="showOnDemand" backgroundColor="#31000000" />                                                
                        </screen>"""

oscam_Readers_scr = """<screen name="OscamReaders" position="center,center" size="1350,525" title="Oscam Readers Info" backgroundColor="#31000000" >
                        <widget name="list" position="30,30" size="1290,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,342" size="1350,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="status_labels_0" position="15,360" size="405,360" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_0" position="420,360" size="255,360" font="priveG;25" halign="left" transparent="1" />
                        <widget name="status_labels_1" position="690,360" size="405,360" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_1" position="1095,360" size="255,360" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="0,465" size="450,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="450,465" size="450,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="900,465" size="450,2" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,475" size="450,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="450,475" size="450,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="blue_button" font="priveG;30" position="900,475" size="450,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>                        
                        </screen>"""
                        
oscam_Users_scr = """<screen name="OscamUsers" position="center,center" size="1440,615" title="Oscam Users Info" backgroundColor="#31000000" >
                        <widget name="list" position="30,30" size="1380,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,342" size="1440,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="status_labels_0" position="15,360" size="135,345" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_0" position="150,360" size="300,345" font="priveG;25" halign="left" transparent="1" />
                        <widget name="status_labels_1" position="465,360" size="165,345" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_1" position="630,360" size="300,345" font="priveG;25" halign="left" transparent="1" />
                        <widget name="status_labels_2" position="945,360" size="180,345" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                        <widget name="status_values_2" position="1125,360" size="300,345" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="0,555" size="720,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="720,555" size="720,2" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,565" size="720,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="blue_button" font="priveG;30" position="720,565" size="720,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>                        
                        </screen>"""
                        
oscam_Entitlements_scr = """<screen name="Entitlements" position="center,center" size="1920,1080" title="Reader Entitlements" flags="wfNoBorder" backgroundColor="#31000000" >
                        <widget name="Crd_info" position="345,74" font="priveG;30" zPosition="1" size="1620,123" valign="center" halign="left" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />
                 	      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/frame_hd.png" position="70,74" size="189,123" zPosition="1" backgroundColor="#31000000" alphatest="off"/>
                        <widget name="Crd_system" position="90,90" zPosition="2" size="150,90" backgroundColor="#31000000" alphatest="on" />
                        <widget name="Host" text="Host" position="90,228" font="priveG;22" zPosition="0" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="CAID" text="CAID" position="510,228" font="priveG;22" zPosition="1" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="System" text="System" position="585,228" font="priveG;22" zPosition="2" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Type" text="Type" position="750,228" font="priveG;21" zPosition="3" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Share ID" text="Share ID" position="810,228" font="priveG;22" zPosition="4" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Remote ID" text="Remote ID" position="960,228" font="priveG;25" zPosition="5" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Up" text="Up" position="1110,228" font="priveG;22" zPosition="6" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Re" text="Re" position="1155,228" font="priveG;22" zPosition="7" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Providers" text="Providers" position="1200,228" font="priveG;22" zPosition="8" size="495,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="TypeCRD" text="Type" position="105,228" font="priveG;22" zPosition="1" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="CAIDcrd" text="CAID" position="247,228" font="priveG;22" zPosition="2" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="ProvID" text="ProvID" position="360,228" font="priveG;21" zPosition="3" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="ID" text="ID" position="510,228" font="priveG;22" zPosition="4" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Class" text="Class" position="810,228" font="priveG;25" zPosition="5" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Start Date" text="Start Date" position="1035,228" font="priveG;22" zPosition="6" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Expire Date" text="Expire Date" position="1267,228" font="priveG;22" zPosition="7" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="Name" text="Name" position="1500,228" font="priveG;22" zPosition="7" size="450,30" halign="left" foregroundColor="yellow" backgroundColor="#31000000" />
                        <widget name="entitlements_list" position="60,258" size="1800,627" zPosition="9" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,915" size="960,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="960,915" size="960,2" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,925" size="960,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="blue" font="priveG;30" position="960,925" size="960,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>
                        </screen>""" 
                        
Ecm_Info_scr = """<screen name="ECMInfo" position="center,center" size="525,573" title="ECM Informations" backgroundColor="#31000000" >              
	               	<widget name="ecmlabels" font="priveG;24" position="30,22" zPosition="1" size="150,390" backgroundColor="#31000000" foregroundColor="#666666" transparent="1" />
                 	<widget name="ecmValues" font="priveG;24" position="174,22" zPosition="2" size="351,390" backgroundColor="#31000000" transparent="1" />
                 	<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/frame_hd.png" position="168,430" size="189,123" zPosition="3" backgroundColor="#31000000" alphatest="off"/>
                  <widget name="piccode" position="188,446" size="150,90" zPosition="4" alphatest="on" />                        
                  </screen>"""                        

OSD_ECM_Menu_scr = """<screen name="OSDECMMenu" position="center,center" size="1500,405" title="OSD Ecm Info setup" backgroundColor="#31000000" >
                      <widget name="config" font="priveG;30" itemHeight="40" position="10,0" size="1480,240" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <widget name="info" position="30,270" size="1440,75" font="priveG;25" valign="center" halign="center" foregroundColor="#888888" transparent="1" />
                      <eLabel position="0,345" size="750,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="750,345" size="750,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,355" size="750,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="750,355" size="750,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      </screen>"""

onScreenEcm_scr = """<screen name="OSDECMInfo" position="1545,105" size="306,51" title="..." flags="wfNoBorder" backgroundColor="#31000000" >
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/frame-1.png" position="0,0" size="306,51" zPosition="1" backgroundColor="#31000000" alphatest="blend"/>                                      
	                 	<widget name="OSD_Ecm_info" font="priveG;27" position="3,7" halign="left" noWrap="1" zPosition="0" size="300,37" backgroundColor="#31000000" transparent="1" />                         
                    </screen>"""

onScreenEcmBig_scr = """<screen name="BigOSDECMInfo" position="1545,105" size="306,261" title="..." flags="wfNoBorder" backgroundColor="#31000000" >                   
                        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/frame-2.png" position="0,0" size="306,261" zPosition="0" backgroundColor="#31000000" alphatest="blend"/>                                      
	                    	<widget name="ecm_items" font="priveG;24" position="15,18" zPosition="2" valign="top" halign="left" size="112,255" backgroundColor="#31000000" transparent="1" />
	                    	<widget name="OSD_Ecm_info" font="priveG;24" position="127,18" zPosition="3" valign="top" halign="left" size="165,255" backgroundColor="#31000000" transparent="1" />                         
                        </screen>"""
                    
mbox_Main = """<screen name="MboxMainScreen" position="center,center" size="1440,595" title="Mbox Menu" backgroundColor="#31000000" >
               <widget name="server_name" font="priveG;25" position="0,0" zPosition="0" size="1440,67" valign="center" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1" />      
               <widget name="list" position="30,67" size="300,165" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,232" size="1440,2" backgroundColor="#888888" zPosition="5" transparent="0" />
               <widget name="info" position="15,250" size="1410,270" font="priveG;21" valign="center" halign="left" backgroundColor="#31000000" transparent="1" />
                      <eLabel position="0,535" size="720,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="720,535" size="720,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,545" size="720,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="720,545" size="720,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
               </screen>"""
                
mbox_pid_scr = """<screen name="MboxPidInfo" position="center,center" size="600,538" title="Pid Info" backgroundColor="#31000000" >
                  <widget name="list" position="30,30" size="540,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,342" size="600,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                  <widget name="status_labels_0" position="30,360" size="150,315" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                  <widget name="status_values_0" position="172,360" size="592,315" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="150,478" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,488" size="600,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                  </screen>"""                
                
mbox_servers_scr = """<screen name="MboxServerInfo" position="center,center" size="600,538" title="Servers Info" backgroundColor="#31000000" >
                      <widget name="list" position="30,30" size="540,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,342" size="600,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                      <widget name="status_labels_0" position="30,360" size="150,315" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                      <widget name="status_values_0" position="172,360" size="592,315" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="150,478" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,488" size="600,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                      </screen>"""                

mbox_netstat_scr = """<screen name="MboxNetState" position="center,center" size="900,598" title="Net Status" backgroundColor="#31000000" >
                      <widget name="list" position="30,30" size="840,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,342" size="900,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                      <widget name="status_labels_0" position="30,360" size="150,315" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                      <widget name="status_values_0" position="195,360" size="675,315" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="300,538" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,548" size="900,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                      </screen>"""

mbox_share_scr = """<screen name="MboxShare" position="center,center" size="600,628" title="Share Info" backgroundColor="#31000000" >
                    <widget name="list" position="30,30" size="540,294" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,342" size="628,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                    <widget name="status_labels_0" position="30,360" size="150,315" font="priveG;25" halign="left" foregroundColor="#666666" transparent="1" />
                    <widget name="status_values_0" position="172,360" size="592,315" font="priveG;25" halign="left" transparent="1" />
                      <eLabel position="150,568" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,578" size="600,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                    </screen>"""  
                        
swap_info = """<screen name="Swap Summary Info" position="center,center" size="1200,420" title="Swap info and delete" backgroundColor="#31000000" >
               <eLabel text="Filename:" font="priveG;25" position="30,30" size="375,30" backgroundColor="#31000000"/>
               <eLabel text="Type:" font="priveG;25" position="630,30" size="150,30" backgroundColor="#31000000"/>
               <eLabel text="Size:" font="priveG;25" position="765,30" size="150,30" backgroundColor="#31000000"/>
               <eLabel text="Used:" font="priveG;25" position="930,30" size="150,30" backgroundColor="#31000000"/>
               <eLabel text="Priority:" font="priveG;25" position="1065,30" size="120,30" backgroundColor="#31000000"/>
               <widget name="list" position="30,60" size="1140,150" scrollbarMode="showOnDemand" backgroundColor="#31000000" zPosition="2"  />
                      <eLabel position="0,360" size="400,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="400,360" size="400,2" backgroundColor="green" zPosition="5" transparent="0" /> 
                      <eLabel position="800,360" size="400,2" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,370" size="400,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="400,370" size="400,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;30" position="800,370" size="400,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
               </screen>"""
                        
swap_create = """<screen name="Swap create" position="center,190" size="1500,270" title="Swap create" backgroundColor="#31000000" >
                 <widget name="config" font="priveG;30" itemHeight="40" position="10,30" size="1480,120" zPosition="2" backgroundColor="#353e575e" transparent="1" />
                      <eLabel position="0,210" size="900,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="900,210" size="900,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,220" size="900,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="900,220" size="900,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                 </screen>"""                                                                                                                                                                                

devices_management_main = """<screen name="Devices Management" position="center,center" size="1200,592" title="Devices Management" backgroundColor="#31000000" >
    <eLabel position="15,30" size="1170,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                 <widget name="devices" position="15,30" size="1170,481" scrollbarMode="showOnDemand" />
                      <eLabel position="0,532" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="300,532" size="300,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="600,532" size="300,2" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <eLabel position="900,532" size="300,2" backgroundColor="blue" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,542" size="300,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="300,542" size="300,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;30" position="600,542" size="300,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
                      <widget name="button_bg" font="priveG;30" position="900,542" size="300,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1"/>                        
                 </screen>"""
                 
usbhdd_management = """<screen name="Hdd Management" position="center,center" size="750,568" title="Hdd Management" backgroundColor="#31000000" >
                        <widget name="list" position="30,15" size="412,375" zPosition="2" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                        <ePixmap position="469,27" zPosition="-1" size="217,231" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/fhd/devices/hdd2.png" alphatest="off"/>     
    <eLabel position="0,395" size="750,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                      <widget name="info" position="30,398" size="690,112" font="priveG;25" zPosition="4" valign="center" halign="center" foregroundColor="#666666" transparent="1" />
                      <eLabel position="0,508" size="375,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="375,508" size="375,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,518" size="375,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="375,518" size="375,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                        </screen>"""
                        
select_Partition = """<screen name="Select Partition" position="center,center" size="1575,672" title="Select Partition" backgroundColor="#31000000" >
                        <widget name="part" position="60,15" font="priveG;30" zPosition="1" size="255,37" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="mnt" position="285,15" font="priveG;30" zPosition="2" size="300,37" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="start" position="645,15" font="priveG;30" zPosition="3" size="300,37" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="end" position="900,15" font="priveG;30" zPosition="4" size="300,37" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="size" position="1155,15" font="priveG;30" zPosition="5" size="180,37" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="id" position="1335,15" font="priveG;30" zPosition="6" size="75,37" valign="center" halign="left" backgroundColor="#31000000" />
                        <widget name="fstype" position="1410,15" font="priveG;30" zPosition="7" size="180,37" valign="center" halign="left" backgroundColor="#31000000" />                        
                        <widget name="list" position="0,60" size="1575,525" zPosition="0" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,598" size="393,1" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="393,598" size="394,1" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="787,598" size="393,1" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="1180,598" size="394,1" backgroundColor="blue" zPosition="5" transparent="0" />
		<widget name="red" position="0,606" size="393,37" font="priveG;30" zPosition="1" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
		<widget name="green" position="393,606" size="394,37" font="priveG;30" zPosition="1" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
		<widget name="yellow" position="787,606" size="393,37" font="priveG;30" zPosition="4" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
		<widget name="blue" position="1180,606" size="394,37" font="priveG;30" zPosition="4" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="blue" transparent="1" />
                        </screen>"""
                        
autoInst_cfg = """<screen name="AutoInstCfg" position="center,240" size="1275,270" title="AutoInstall" backgroundColor="#31000000" >
	                  <widget name="config" font="priveG;30" itemHeight="40" position="10,30" size="1255,135" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
		<widget name="white" position="0,150" size="1275,37" font="priveG;30" zPosition="2" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="#888888" transparent="1"/>
    <eLabel position="0,210" size="318,2" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="318,210" size="319,2" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="637,210" size="318,2" backgroundColor="yellow" zPosition="5" transparent="0" />
    <eLabel position="955,210" size="319,2" backgroundColor="blue" zPosition="5" transparent="0" />
		<widget name="red" position="0,220" size="318,37" font="priveG;30" zPosition="1" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
		<widget name="green" position="318,220" size="319,37" font="priveG;30" zPosition="1" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
		<widget name="yellow" position="637,220" size="318,37" font="priveG;30" zPosition="4" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
		<widget name="blue" position="955,220" size="319,37" font="priveG;30" zPosition="4" valign="top" halign="center" backgroundColor="#31000000" foregroundColor="blue" transparent="1" />
	                  </screen>"""
                                                                    
autoInstStatus_scr = """<screen name="AutoInstState" position="center,center" size="1200,570" title="AutoInstall Status" backgroundColor="#31000000" >
                        <widget name="list" position="30,30" size="1140,450" zPosition="0" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="450,510" size="300,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,520" size="1200,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>                     
                        </screen>"""
                        
settings_menu = """<screen name="SettingsMenu" position="center,center" size="900,426" title="Settings/satellites.xml menu" backgroundColor="#31000000" >
                        <widget name="list" position="30,15" size="840,247" zPosition="2" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,262" size="900,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="info" position="30,265" size="840,102" font="priveG;25" zPosition="4" valign="center" halign="center" foregroundColor="#666666" transparent="1" />
                      <eLabel position="0,366" size="450,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="450,366" size="450,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,376" size="450,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="450,376" size="450,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                        </screen>"""

settings_center_scr = """<screen name="SettingsCenter" position="center,center" size="1350,525" title="Please, select zip/rar file with settings" backgroundColor="#31000000" >
                <widget name="list" position="30,30" size="1290,405" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,465" size="675,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="675,465" size="675,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,475" size="675,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="675,475" size="675,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                </screen>"""  
                
cronMng_scr = """<screen position="center,center" size="1530,615" title="Cron Manager" backgroundColor="#31000000" >
                <widget name="list" position="15,6" size="1500,540" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
                      <eLabel position="0,555" size="306,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="306,555" size="306,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="612,555" size="306,2" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <eLabel position="918,555" size="306,2" backgroundColor="blue" zPosition="5" transparent="0" />
                      <eLabel position="1224,555" size="306,2" backgroundColor="white" zPosition="5" transparent="0" />                                          
    <widget name="key_red" position="0,565" zPosition="1" size="306,70" font="priveG;30" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1" />
    <widget name="key_green" position="306,565" zPosition="1" size="306,70" font="priveG;30" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1" />
    <widget name="key_yellow" position="612,565" zPosition="1" size="306,70" font="priveG;30" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
    <widget name="key_blue" position="918,565" zPosition="1" size="306,70" font="priveG;30" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="blue" transparent="1" />
    <widget name="key_ok" position="1224,565" zPosition="1" size="306,70" font="priveG;30" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="white" transparent="1" />
    </screen>"""                

cfgScreen = """<screen name="GSUcfgScreen" position="center,center" size="1500,660" title="GSU configuration" backgroundColor="#31000000" >
    <widget name="config" font="priveG;30" itemHeight="40" position="10,10" size="1480,560" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
                      <eLabel position="0,600" size="750,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="750,600" size="750,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,610" size="750,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="750,610" size="750,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
	  </screen>"""
	                  
ftpScr = """<screen name="FtpCenter" position="center,center" size="1050,576" title="Download menu" backgroundColor="#31000000" >
            <widget name="list" position="30,30" size="990,381" zPosition="2" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
    <eLabel position="0,420" size="1050,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                      <eLabel position="0,516" size="525,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="525,516" size="525,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,526" size="525,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="525,526" size="525,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
            </screen>"""

cifsNfsScr = """<screen name="createCifsNfs" position="center,center" size="1500,620" title="Set parameters for CIFS/NFS" backgroundColor="#31000000" >
			<widget name="config" font="priveG;30" itemHeight="40" position="30,30" size="1440,500" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
                      <eLabel position="0,560" size="500,2" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="500,560" size="500,2" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="1000,560" size="500,2" backgroundColor="yellow" zPosition="5" transparent="0" />
                      <widget name="red" font="priveG;30" position="0,570" size="500,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1"/>
                      <widget name="green" font="priveG;30" position="500,570" size="500,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1"/>
                      <widget name="yellow" font="priveG;30" position="1000,570" size="500,40" zPosition="1" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1"/>
	</screen>"""
	
cronScr = """<screen position="center,center" size="1500,835" title="Add Job:" backgroundColor="#31000000" >
	<widget name="config" font="priveG;30" itemHeight="40" position="10,10" size="1480,600" scrollbarMode="showOnDemand" backgroundColor="#31000000"  />
    <eLabel position="0,775" size="500,2" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="500,775" size="500,2" backgroundColor="green" zPosition="5" transparent="0" />
    <eLabel position="1000,775" size="500,2" backgroundColor="white" zPosition="5" transparent="0" />
	<widget name="key_red" position="0,785" zPosition="1" size="500,40" font="priveG;30" halign="center" valign="top" foregroundColor="red" backgroundColor="#31000000"  transparent="1" />
	<widget name="key_green" position="500,785" zPosition="1" size="500,40" font="priveG;30" halign="center" valign="top" foregroundColor="green" backgroundColor="#31000000"  transparent="1" />
		<widget name="key_txt" position="1000,785" size="500,40" font="priveG;30" zPosition="4" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="white" transparent="1" />
	</screen>"""
  
txtEdScr = """<screen position="0,0" size="1920,1080" title="Txt editor" flags="wfNoBorder" backgroundColor="#31000000" >
						<widget source="Title" render="Label" position="0,75" zPosition="1" size="1920,37" font="priveG;30" halign="center" valign="center" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
						<widget name="txt" font="priveG;30" position="75,127" size="1770,825" itemHeight="40" transparent="1" backgroundColor="#31000000" zPosition="2" />
                      <eLabel position="0,967" size="639,1" backgroundColor="red" zPosition="5" transparent="0" />
                      <eLabel position="639,967" size="640,1" backgroundColor="green" zPosition="5" transparent="0" />
                      <eLabel position="1279,967" size="639,1" backgroundColor="yellow" zPosition="5" transparent="0" />
						<widget name="key_red" position="0,975" zPosition="1" size="639,37" font="priveG;30" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="red" transparent="1" />
						<widget name="key_yellow" position="1279,975" zPosition="1" size="640,37" font="priveG;30" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="yellow" transparent="1" />
						<widget name="key_green" position="639,975" zPosition="1" size="639,37" font="priveG;30" halign="center" valign="top" backgroundColor="#31000000" foregroundColor="green" transparent="1" />
						</screen>"""
            
filebrowser = """<screen name="DirBrowser" position="center,center" size="780,750" title="Dir Browser" backgroundColor="#31000000" >
			<widget name="filelist" position="15,15" size="750,660" scrollbarMode="showOnDemand" />
	<widget source="key_red" render="Label" position="0,700" size="390,50" zPosition="2" valign="top" halign="center" font="priveG;30" transparent="1" foregroundColor="red" />
	<widget source="key_green" render="Label" position="390,700" size="390,50" zPosition="2" valign="top" halign="center" font="priveG;30" transparent="1" foregroundColor="green" />
   <eLabel position="0,690" size="390,2" backgroundColor="red" zPosition="5" transparent="0" />
    <eLabel position="390,690" size="390,2" backgroundColor="green" zPosition="5" transparent="0" />
		</screen>"""              	
