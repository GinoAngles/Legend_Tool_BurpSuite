#!/usr/bin/jython
# -*- coding: utf-8 -*-

# This work is licensed under a {CC-BY} Creative Commons Attribution 4.0 International License.
# You are free to:
# - Share: copy and redistribute the material in any medium or format.
# - Adapt: remix, transform, and build upon the material for any purpose, even commercially. 
# Under the following terms:
# - Attribution: You must give appropriate credit, provide a link to the license, and indicate if changes were made. 
#	You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
# Notices:
# - You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable exception or limitation.
# - No warranties are given. The license may not give you all of the permissions necessary for your intended use. 
#   For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.

from burp import IBurpExtender
from burp import ITab
from burp import IHttpListener
from burp import IScannerCheck

from java.awt import Component, GridLayout, GridBagLayout, GridBagConstraints, Insets, Toolkit, Color, Font
from java.awt.datatransfer import Clipboard, StringSelection
from javax.swing import JButton, JTabbedPane, JPanel, JLabel, JTextField, JTextArea, JScrollPane, SwingConstants, JSeparator, JSlider, JSplitPane, JTable, JOptionPane, JCheckBox
from javax.swing.table import DefaultTableModel
from java.net import URL

class Masher():
	def __init__(self, minpwd, maxpwd, specchars, transfor_bool):
		# Anios para adherir
		self._years = ['2016', '2017', '2010']
		# Caracteres especiales
		self._chars = specchars
		# Longitud de la pwd (p.e. entre 6 y 12)
		self._wlfrom = minpwd
		self._wlto = maxpwd

		self._reverse_year = '7'
		self._threads = 50
		self._numfrom = 0
		self._numto = 20
		if transfor_bool:
			self._aa = '4'
			self._ee = '3'
			self._ii = '1'
			self._oo = '0'
			self._tt = '7'
			self._ss = '5'
			self._gg = '9'
			self._zz = '2'
		else:
			self._aa = 'a'
			self._ee = 'e'
			self._ii = 'i'
			self._oo = 'o'
			self._tt = 't'
			self._ss = 's'
			self._gg = 'g'
			self._zz = 'z'
			
	def concatenar(self, seq, start, stop):
		for str1 in seq:
			for num1 in xrange(start,stop):
				yield str1 + str(num1)
	def combinar(self, seq, start, schar = ""):
		for str1 in seq:
			for str2 in start:
				yield str1 + schar + str2
	def mashup(self, lista_palabras, FNacimiento):
		rdo_wpares = ['']
		rdo_schars = ['']
		rdo_xrepl = ['']		
		rdo_simp = ['']
		rdo_simpver = ['']

		# Concatenamos las palabras con una char especial en medio.
		for spec in self._chars:
			for w1 in lista_palabras:
				for w2 in lista_palabras:
					if lista_palabras.index(w1) != lista_palabras.index(w2):
						rdo_simp.append(w1+spec+w2)
		# Concatenamos las palabras en pares.
		for w1 in lista_palabras:
			for w2 in lista_palabras:
				if lista_palabras.index(w1) != lista_palabras.index(w2):
					rdo_wpares.append(w1+w2)
		# generamos combinaciones de los caracteres especiales.
		for w1 in self._chars:
			rdo_schars.append(w1)
			for w2 in self._chars:
				rdo_schars.append(w1+w2)
				for w3 in self._chars:
					rdo_schars.append(w1+w2+w3)
		# Distintas combinaciones para la Fecha nacimiento.
		if FNacimiento != "":
			FN_yy = FNacimiento[-2:]
			FN_yyy = FNacimiento[-3:]
			FN_yyyy = FNacimiento[-4:]
			FN_xd = FNacimiento[1:2]
			FN_xm = FNacimiento[3:4]
			FN_dd = FNacimiento[:2]
			FN_mm = FNacimiento[2:4]
			self._reverse_year = FN_yyyy[::-1]
			FNcompos = [FN_yy, FN_yyy, FN_yyyy, FN_xd, FN_xm, FN_dd, FN_mm, self._reverse_year]
			FNcombos = ['']
			for w1 in FNcompos:
				FNcombos.append(w1)
				for w2 in FNcompos:
					if FNcompos.index(w1) != FNcompos.index(w2):
						FNcombos.append(w1+w2)
						for w3 in FNcompos:
							if FNcompos.index(w1) != FNcompos.index(w2) and FNcompos.index(w2) != FNcompos.index(w3) and FNcompos.index(w1) != FNcompos.index(w3):
								FNcombos.append(w1+w2+w3)

		# Concatenamos las palabras con un char especial y año inverso.
		for spec in self._chars:
			for w1 in lista_palabras:
				rdo_simpver.append(w1+spec+self._reverse_year)

		# concatenaciones y combinaciones extras.
		combo1 = list(self.combinar(lista_palabras, self._years))
		combo2 = list(self.combinar(rdo_wpares, self._years))
		combo3 = list(self.combinar(lista_palabras, rdo_schars))
		combo4 = list(self.combinar(rdo_wpares, rdo_schars))
		combo5 = list(self.concatenar(lista_palabras, self._numfrom, self._numto))
		combo6 = list(self.concatenar(rdo_wpares, self._numfrom, self._numto))
		
		combo1_uniq = dict.fromkeys(combo1).keys()
		combo2_uniq = dict.fromkeys(combo2).keys()
		combo3_uniq = dict.fromkeys(combo3).keys()
		combo4_uniq = dict.fromkeys(combo4).keys()
		combo5_uniq = dict.fromkeys(combo5).keys()
		combo6_uniq = dict.fromkeys(combo6).keys()
		combo7_uniq = dict.fromkeys(lista_palabras).keys()
		combo8_uniq = dict.fromkeys(rdo_wpares).keys()
		combo20_uniq = dict.fromkeys(rdo_simp).keys()
		combo21_uniq = dict.fromkeys(rdo_simpver).keys()

		dict_temp = combo20_uniq+combo21_uniq+combo1_uniq+combo2_uniq+combo3_uniq+combo4_uniq+combo5_uniq+combo6_uniq+combo7_uniq+combo8_uniq

		if FNacimiento != "":
			combo9 = list(self.combinar(lista_palabras, FNcombos))
			combo10 = list(self.combinar(rdo_wpares, FNcombos))
			combo9_uniq = dict.fromkeys(combo9).keys()
			combo10_uniq = dict.fromkeys(combo10).keys()
			dict_temp += combo9_uniq+combo10_uniq

		dict_rem = dict.fromkeys(dict_temp).keys()

		# Remplazamos las letras por numeros en otra tanda.
		for wx in dict_rem:
			wx = wx.replace('a', self._aa)
			wx = wx.replace('e', self._ee)
			wx = wx.replace('i', self._ii)
			wx = wx.replace('o', self._oo)
			wx = wx.replace('t', self._tt)
			wx = wx.replace('s', self._ss)
			wx = wx.replace('g', self._gg)
			wx = wx.replace('z', self._zz)
			rdo_xrepl.append(wx)

		rdo = dict_rem + rdo_xrepl
		# Eliminamos blancos
		while "" in rdo: rdo.remove("")
		# Eliminamos combinaciones menores que wlfrom y mayores que wlto
		rdo_rdo = [x for x in rdo if len(x) >= self._wlfrom and len(x) <= self._wlto]
		return rdo_rdo

class Mi_Extension(IHttpListener, IScannerCheck):

	def __init__(self, extender):
		self._callbacks = extender._callbacks
		self._helpers = extender._callbacks.getHelpers()
		self._callbacks.registerScannerCheck(self)
		# Creamos el contenedor de paneles.
		self.contenedor = JTabbedPane()

		# Campos del sub-tab 1 (mash up)
		self._tab1_nombre = JTextField()
		self._tab1_apellido = JTextField()
		self._tab1_FNacimiento = JTextField()
		self._tab1_mascota = JTextField()
		self._tab1_otro = JTextField()

		self._tab1_feedback_ta = JTextArea('This may take a while . . .')
		self._tab1_feedback_ta.setEditable(False)
		self._tab1_feedback_sp = JScrollPane(self._tab1_feedback_ta)

		self._tab1_minsize = JSlider(4,16,6)
		self._tab1_minsize.setMajorTickSpacing(1)
		self._tab1_minsize.setPaintLabels(True)

		self._tab1_maxsize = JSlider(4,16,10)
		self._tab1_maxsize.setMajorTickSpacing(1)
		self._tab1_maxsize.setPaintLabels(True)

		self._tab1_specialchars = JTextField('!,@,#,$,&,*')
		self._tab1_transformations = JCheckBox('1337 mode')
		self._tab1_firstcapital = JCheckBox('first capital letter')

		# Campos del sub-tab 2 (redirect)
		self._tab2_JTFa = JTextField()
		self._tab2_JTFaa = JTextField()
		self._tab2_JTFb = JTextField()
		self._tab2_JTFbb = JTextField()
		self._tab2_boton = JButton(' Redirect is Off ', actionPerformed=self.switch_redirect)
		self._tab2_boton.background = Color.lightGray
		self._tab2_encendido = False

		# Campos del sub-tab 3 (loader)
		self._tab3_urls_ta = JTextArea(15, 5)
		self._tab3_urls_sp = JScrollPane(self._tab3_urls_ta)

		# Campos del sub-tab 4 (headers)
		self._tab4_tabla_model = DefaultTableModel()
		self._tab4_headers_dict = {}

		# Campos del sub-tab 5 (reverse ip)
		self._tab5_target = JTextArea(15, 5)
		self._tab5_target_sp = JScrollPane(self._tab5_target)

	def create(self):

		# Estilo general para todas las sub-tab.
		gBC = GridBagConstraints()
		gBC.fill = GridBagConstraints.BOTH
		gBC.ipadx = 5
		gBC.ipady = 5
		gBC.insets = Insets(0,5,5,5)
		gBC.weightx = 0.5
		#gBC.weighty = 0.7

		#######################################
		###   Creamos la primera sub-tab. (MASHUP)
		#######################################
		tab_1 = JPanel(GridBagLayout())
		tab_1_jlabelAyuda = JLabel('<html><i>&#8226Tip: This Mashup receive one or more keywords in order to generate a list of possible passwords</i></html>')
		tab_1_jlabelAyuda.setFont(Font("Serif", 0, 12))
		
		gBC.gridx = 0
		gBC.gridy = 0
		tab_1.add(JLabel('<html><font color=green><i>Income:</i></font></html>'), gBC)

		gBC.gridy = 1
		tab_1.add(JLabel('<html><b>&#8226 Name:</b></html>'), gBC)
		gBC.gridy = 2
		tab_1.add(self._tab1_nombre, gBC)

		gBC.gridy = 3
		tab_1.add(JLabel('<html><b>&#8226 Surname:</b></html>'), gBC)
		gBC.gridy = 4
		tab_1.add(self._tab1_apellido, gBC)

		gBC.gridy = 5
		tab_1.add(JLabel('<html><b>&#8226 Birthdate: (DDMMYYYY)</b></html>'), gBC)
		gBC.gridy = 6
		tab_1.add(self._tab1_FNacimiento, gBC)

		gBC.gridy = 7
		tab_1.add(JLabel('<html><b>&#8226 Pet:</b></html>'), gBC)
		gBC.gridy = 8
		tab_1.add(self._tab1_mascota, gBC)

		gBC.gridy = 9
		tab_1.add(JLabel('<html><b>&#8226 Anyother:</b></html>'), gBC)
		gBC.gridy = 10
		tab_1.add(self._tab1_otro, gBC)

		gBC.gridy = 11
		tab_1.add(JLabel('<html><b>&#8226 Passwd Min Size:</b></html>'), gBC)
		gBC.gridy = 12
		tab_1.add(self._tab1_minsize, gBC)

		gBC.gridy = 13
		tab_1.add(JLabel('<html><b>&#8226 Passwd Max Size:</b></html>'), gBC)
		gBC.gridy = 14
		tab_1.add(self._tab1_maxsize, gBC)

		gBC.gridy = 15
		tab_1.add(JLabel('<html><b>&#8226 Especial Chars: (comma separated)</b></html>'), gBC)
		gBC.gridy = 16
		tab_1.add(self._tab1_specialchars, gBC)

		gBC.gridy = 17
		tab_1.add(self._tab1_transformations, gBC)
		
		gBC.gridy = 18
		tab_1.add(self._tab1_firstcapital, gBC)

		gBC.gridy = 19
		tab_1.add(JButton('Mashup!', actionPerformed=self.mashup), gBC)
		
		gBC.gridy = 20
		gBC.gridwidth = 3
		tab_1.add(JSeparator(), gBC)
		gBC.gridwidth = 1

		gBC.gridy = 21
		gBC.gridwidth = 3
		tab_1.add(tab_1_jlabelAyuda, gBC)
		gBC.gridwidth = 1

		gBC.gridx = 1
		gBC.gridy = 0
		gBC.gridheight = 20
		gBC.weightx = 0
		tab_1.add(JSeparator(SwingConstants.VERTICAL), gBC)
		gBC.gridheight = 1
		gBC.weightx = 0.5
		
		gBC.gridx = 2
		gBC.gridy = 0
		tab_1.add(JLabel('<html><font color=green><i>Outcome:</i></font></html>'), gBC)

		gBC.gridy = 1
		gBC.gridwidth = 2
		gBC.gridheight = 18
		tab_1.add(self._tab1_feedback_sp, gBC)
		gBC.gridwidth = 1
		gBC.gridheight = 1

		gBC.gridy = 19
		tab_1.add(JButton('Copy to clipboard!', actionPerformed=self.cpy_clipboard), gBC)

		#######################################
		###   Creamos la segunda sub-tab. (REDIRECT)
		#######################################
		tab_2 = JPanel(GridBagLayout())
		tab_2_jlabelAyuda = JLabel('<html><i>&#8226Tip: This Redirect receive a pair of hosts x,y in order to redirect from x to y.</i></html>')
		tab_2_jlabelAyuda.setFont(Font("Serif", 0, 12))

		gBC.gridx = 0
		gBC.gridy = 0
		tab_2.add(JLabel('<html><b>&#8226 From: (i.e. www.facebook.com)</b></html>'), gBC)
		gBC.gridx = 1
		gBC.gridy = 0
		tab_2.add(self._tab2_JTFa, gBC)

		gBC.gridx = 2
		gBC.gridy = 0
		tab_2.add(JLabel('<html><b>&#8226 To: (i.e. www.myhomepage.es)</b></html>'), gBC)
		gBC.gridx = 3
		gBC.gridy = 0
		tab_2.add(self._tab2_JTFaa, gBC)

		gBC.gridx = 0
		gBC.gridy = 1
		gBC.gridwidth = 4
		tab_2.add(JSeparator(), gBC)
		gBC.gridwidth = 1

		gBC.gridx = 0
		gBC.gridy = 2
		tab_2.add(JLabel('<html><b>&#8226 From:</b></html>'), gBC)
		gBC.gridx = 1
		gBC.gridy = 2
		tab_2.add(self._tab2_JTFb, gBC)

		gBC.gridx = 2
		gBC.gridy = 2
		tab_2.add(JLabel('<html><b>&#8226 To:</b></html>'), gBC)
		gBC.gridx = 3
		gBC.gridy = 2
		tab_2.add(self._tab2_JTFbb, gBC)

		gBC.gridx = 0
		gBC.gridy = 3
		gBC.gridwidth = 4
		tab_2.add(self._tab2_boton, gBC)
		gBC.gridwidth = 1

		gBC.gridx = 0
		gBC.gridy = 4
		gBC.gridwidth = 4
		gBC.insets = Insets(100,10,5,10)
		tab_2.add(JSeparator(), gBC)
		gBC.gridwidth = 1
		gBC.insets = Insets(5,10,5,10)

		gBC.gridx = 0
		gBC.gridy = 5
		gBC.gridwidth = 4
		tab_2.add(tab_2_jlabelAyuda, gBC)
		gBC.gridwidth = 1

		#######################################
		###   Creamos la tercera sub-tab. (LOADER)
		#######################################
		tab_3 = JPanel(GridBagLayout())
		tab_3_jlabelAyuda = JLabel('<html><i>&#8226Tip: This Loader receive a list of Hosts or IPs that will be added to the Burp Scope.</i></html>')
		tab_3_jlabelAyuda.setFont(Font("Serif", 0, 12))
		
		gBC.gridx = 0
		gBC.gridy = 0
		tab_3.add(JLabel('<html><font color=green><i>List of targets: (i.e. http://www.mytargetweb.com)</i></font></html>'), gBC)
		gBC.gridy = 1
		gBC.gridheight = 10
		gBC.weighty = 0.5
		tab_3.add(self._tab3_urls_sp, gBC)
		gBC.gridheight = 1
		gBC.weighty = 0
		gBC.gridy = 11
		tab_3.add(JButton('Load Into Target => Scope!', actionPerformed=self.loader), gBC)

		gBC.gridy = 12
		gBC.gridwidth = 5
		gBC.insets = Insets(100,10,5,10)
		tab_3.add(JSeparator(), gBC)
		gBC.gridwidth = 1
		gBC.insets = Insets(5,10,5,10)

		gBC.gridy = 13
		tab_3.add(tab_3_jlabelAyuda, gBC)

		#######################################
		###   Creamos la cuarta sub-tab. (HEADERS)
		#######################################	
		tab_4_jlabelAyuda = JLabel("<html><i>&#8226Tip: This Headers records all unique headers that appear in every host, check out the security headers.</i></html>")
		tab_4_jlabelAyuda.setFont(Font("Serif", 0, 12))

		tab_4_jLabelRecomendacion = JLabel("<html>&#8226<b>Server</b>: Don't give away much information.<br> &#8226<b>Content-Security-Policy</b>: Protect your site from XSS attacks by whitelisting sources of approved content.<br> &#8226<b>Strict-Transport-Security</b>: Enforce the browser to use HTTPS.<br> &#8226<b>Public-Key-Pins</b>: Protect your site from MITM attacks.<br> &#8226<b>X-Content-Type-Options</b>: the valid value is -> nosniff .<br> &#8226<b>X-Frame-Options</b>: tells the browser whether you want to allow your site to be framed or not.<br> &#8226<b>X-XSS-Protection</b>: the best value is -> 1; mode=block .</html>")
		tab_4_jLabelRecomendacion.setFont(Font("Dialog", 0, 13))
	
		tab_4 = JPanel(GridBagLayout())
		splitpane = JSplitPane(JSplitPane.VERTICAL_SPLIT)
		tab_4_top = JPanel(GridBagLayout())
		tab_4_bottom = JPanel(GridBagLayout())

		gBC_table = GridBagConstraints()
		gBC_table.fill = GridBagConstraints.BOTH
		gBC_table.ipadx = 5
		gBC_table.ipady = 5
		gBC_table.insets = Insets(5,10,5,10)
		gBC_table.weightx = 1
		gBC_table.weighty = 1

		tabla_datos = []
		tabla_headers = ('Severity','Header','Value','Host')
		self._tab4_tabla_model = DefaultTableModel(tabla_datos, tabla_headers)
		tabla_ej = JTable(self._tab4_tabla_model)
		tabla_example = JScrollPane(tabla_ej, JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED, JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED)

		gBC_table.gridx = 0
		gBC_table.gridy = 0
		gBC_table.gridheight = 5
		tab_4_top.add(tabla_example, gBC_table)
		gBC_table.gridheight = 1

		gBC_table.weightx = 0.5
		gBC_table.weighty = 0
		gBC_table.gridwidth = 2
		gBC_table.gridx = 0
		gBC_table.gridy = 0
		tab_4_bottom.add(JSeparator(), gBC_table)
		gBC_table.gridy = 1
		tab_4_bottom.add(tab_4_jlabelAyuda, gBC_table)
		gBC_table.gridy = 2
		tab_4_bottom.add(tab_4_jLabelRecomendacion, gBC_table)

		splitpane.setTopComponent(tab_4_top)
		splitpane.setBottomComponent(tab_4_bottom)
		gBC_table.weightx = 1
		gBC_table.weighty = 1
		gBC_table.gridx = 0
		gBC_table.gridy = 0
		tab_4.add(splitpane,gBC_table)

		#######################################
		###   Creamos la quinta sub-tab. (ACTIVE SCAN)
		#######################################			
		tab_5 = JPanel(GridBagLayout())
		tab_5_jlabelAyuda = JLabel('<html><i>&#8226Tip: This Quick Scan receive a list of targets and launch an active scan.</i></html>')
		tab_5_jlabelAyuda.setFont(Font("Serif", 0, 12))
		tab_5_jlabelWarning = JLabel('<html><font color=red><i>&#8226Warning: Active scanning generates large numbers of requests which are malicious in form and which may result in compromise of the application. You should use this scanning mode with caution, only with the explicit permission of the application owner. For more information, read the documentation of active scan, Burp Suite.</font></i></html>')
		tab_5_jlabelWarning.setFont(Font("Dialog", 0, 13))
		
		gBC.gridx = 0
		gBC.gridy = 0
		tab_5.add(JLabel('<html><font color=green><i>List of targets: (i.e. http://192.168.1.1/index.html)</i></font></html>'), gBC)
		gBC.gridy = 1
		gBC.gridheight = 8
		gBC.weighty = 0.5
		tab_5.add(self._tab5_target_sp, gBC)
		gBC.gridheight = 1
		gBC.weighty = 0
		gBC.gridy = 9
		tab_5.add(JButton('Launch Scan!', actionPerformed=self.do_active_scan), gBC)

		gBC.gridy = 10
		gBC.gridwidth = 5
		gBC.insets = Insets(100,10,5,10)
		tab_5.add(JSeparator(), gBC)
		gBC.gridwidth = 1
		gBC.insets = Insets(5,10,5,10)

		gBC.gridy = 11
		tab_5.add(tab_5_jlabelAyuda, gBC)
		gBC.gridy = 12
		tab_5.add(tab_5_jlabelWarning, gBC)

		#######################################
		###   Creamos la ultima sub-tab.
		#######################################
		tab_about = JPanel(GridBagLayout())

		gBC_about = GridBagConstraints()
		gBC_about.fill = GridBagConstraints.HORIZONTAL
		gBC_about.ipadx = 5
		gBC_about.ipady = 5
		gBC_about.insets = Insets(5,10,5,10)
		gBC_about.weightx = 1
		gBC_about.weighty = 1

		Jlabel1 = JLabel('<html><b>Plug-in L-Tools</b></html>')
		Jlabel1.setFont(Font("Dialog", 1, 18))
		jlabel2 = JLabel('<html>This Plug-in provides utilities for pentesters, researchers and developers, in order to support their work.</html>')
		jlabel3 = JLabel('<html><b>CC-BY 4.0, 2017. Gino Angles</b></html>')
		jlabel3.setFont(Font("Dialog", 1, 14))
		jlabel4 = JLabel('<html><b>License</b></html>')
		jlabel4.setFont(Font("Dialog", 1, 14))
		jlabel5 = JLabel('<html><img alt="Licensed under a Creative Commons BY" style="border-width:0" src="https://licensebuttons.net/l/by/4.0/88x31.png"></html>')
		jlabel6 = JLabel('<html>This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.</html>')
		jlabel7 = JLabel('<html><b>Dependencies</b></html>')
		jlabel7.setFont(Font("Dialog", 1, 14))
		jlabel8 = JLabel('Jython +2.7')
		jlabel9 = JLabel('http://www.jython.org')

		gBC_about.gridx = 0
		gBC_about.gridy = 0
		tab_about.add(Jlabel1, gBC_about)
		gBC_about.gridy = 1
		tab_about.add(jlabel2, gBC_about)
		gBC_about.gridy = 2
		tab_about.add(jlabel3, gBC_about)

		gBC_about.gridy = 3
		gBC_about.gridwidth = 5
		tab_about.add(JSeparator(), gBC_about)
		gBC_about.gridwidth = 1

		gBC_about.gridy = 4
		tab_about.add(jlabel4, gBC_about)
		gBC_about.gridy = 5
		tab_about.add(jlabel5, gBC_about)
		gBC_about.gridy = 6
		tab_about.add(jlabel6, gBC_about)

		gBC_about.gridy = 7
		gBC_about.gridwidth = 5
		tab_about.add(JSeparator(), gBC_about)
		gBC_about.gridwidth = 1

		gBC_about.gridy = 8
		tab_about.add(jlabel7, gBC_about)
		gBC_about.gridy = 9
		tab_about.add(jlabel8, gBC_about)
		gBC_about.gridy = 10
		tab_about.add(jlabel9, gBC_about)

		# Añadimos los sub-tab al contenedor y lo devolvemos.
		self.contenedor.addTab('Mashup', tab_1)
		self.contenedor.addTab('Redirect', tab_2)
		self.contenedor.addTab('Loader', tab_3)
		self.contenedor.addTab('Headers', tab_4)
		self.contenedor.addTab('Quick Scan', tab_5)
		self.contenedor.addTab('About', tab_about)

		return self.contenedor

	# Funcion que copia el contenido de texto al clipboard.
	def cpy_clipboard(self, event):
		toolkit = Toolkit.getDefaultToolkit()
		clipboard = toolkit.getSystemClipboard()
		clipboard.setContents(StringSelection(self._tab1_feedback_ta.text), None)
		JOptionPane.showMessageDialog(self.contenedor, "Output copied to clipboard", "Information", JOptionPane.INFORMATION_MESSAGE)
		return

	# Funcion que instancia la clase Masher() y hace el mashup del sub-tab1 (mashup).
	def mashup(self, event):
		if self._tab1_minsize.value > self._tab1_maxsize.value:
			self._callbacks.issueAlert('Mashup=> min size have to be bigger than max size.')
		else:
			estado_JCH_trans = self._tab1_transformations.isSelected()
			especial_chars = self._tab1_specialchars.text.split(",")
			mymash = Masher(self._tab1_minsize.value, self._tab1_maxsize.value, especial_chars, estado_JCH_trans)
			reverse_name = self._tab1_nombre.text[::-1]
			if self._tab1_firstcapital.isSelected():
				lista_palabras = [self._tab1_nombre.text.title(), self._tab1_apellido.text.title(), self._tab1_FNacimiento.text, self._tab1_mascota.text.title(), self._tab1_otro.text.title(), reverse_name.title()]
			else:
				lista_palabras = [self._tab1_nombre.text, self._tab1_apellido.text, self._tab1_FNacimiento.text, self._tab1_mascota.text, self._tab1_otro.text, reverse_name]

			while "" in lista_palabras: lista_palabras.remove("")
			rdo_rdo = mymash.mashup(lista_palabras, self._tab1_FNacimiento.text)
			self._tab1_feedback_ta.text = "\n".join(rdo_rdo)
		return

	# Funcion que activa/desactiva el redirect.
	def switch_redirect(self, event):
		if not self._tab2_encendido:
			self._tab2_boton.text = ' Redirect is On '
			self._tab2_boton.background = Color.gray
			self._tab2_encendido = True
			# Registramos la instancia del escuchador http.
			self._callbacks.registerHttpListener(self)
		else:
			self._tab2_boton.text = ' Redirect is Off '
			self._tab2_boton.background = Color.lightGray
			self._tab2_encendido = False
			# Borramos la instancia del escuchador http.
			self._callbacks.removeHttpListener(self)
		return

	# @override
	def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
		if messageIsRequest and self._tab2_encendido:
			serviceHttp = messageInfo.getHttpService()
			if messageInfo.getHttpService().getHost() == self._tab2_JTFa.text:
				if self._tab2_JTFaa.text == '': self._tab2_JTFaa.text = 'localhost'
				messageInfo.setHttpService(self._helpers.buildHttpService(self._tab2_JTFaa.text, serviceHttp.getPort(), serviceHttp.getProtocol()))
			elif messageInfo.getHttpService().getHost() == self._tab2_JTFb.text:
				if self._tab2_JTFbb.text == '': self._tab2_JTFbb.text = 'localhost'
				messageInfo.setHttpService(self._helpers.buildHttpService(self._tab2_JTFbb.text, serviceHttp.getPort(), serviceHttp.getProtocol()))
		return

	# Funcion que carga el textArea de URL a Scope.
	def loader(self, event):
		lista_url = self._tab3_urls_ta.text.split("\n")
		for newUrl in lista_url:
			self._callbacks.includeInScope(URL(newUrl))
		return

	# @override
	def doPassiveScan(self, request_response):
		_response = request_response.getResponse()
		_request = request_response.getRequest()
		_httpService = request_response.getHttpService()
		_url = request_response.getHttpService().getHost()
		info_response = self._helpers.analyzeResponse(_response)
		info_request = self._helpers.analyzeRequest(_httpService, _request)
		headers = info_response.getHeaders()
		_fullUrl = info_request.getUrl().toString()

		for head in headers:
			head_w1 = head.split("\n")
			for head_w2 in head_w1:
				head_w3 = head_w2.split(":")
				if len(head_w3) > 1:
					head_w3[0].encode('ascii','ignore')
					head_w3[1].encode('ascii','ignore')

					key = "%s-%s" % (_url, head_w3[0])

					if key not in self._tab4_headers_dict:
						critical = self.analizeHeader(head_w3[0])

						fila_tabla = [critical,head_w3[0],head_w3[1],_fullUrl]

						self._tab4_headers_dict[key] = fila_tabla
						self._tab4_tabla_model.addRow(fila_tabla)
		return

	# devuelve cuan importante es la cabecera HTTP.
	def analizeHeader(self, header):
		if header == "Content-Security-Policy":
			return "High"
		elif header == "X-Content-Type-Options":
			return "High"
		elif header == "X-Frame-Options":
			return "High"
		elif header == "X-XSS-Protection":
			return "High"
		elif header == "Strict-Transport-Security":
			return "High"
		elif header == "Public-Key-Pins":
			return "High"
		elif header == "Access-Control-Allow-Origin":
			return "High"
		elif header == "X-Permitted-Cross-Domain-Policies":
			return "High"
		elif header == "X-Powered-By":
			return "Information"
		elif header == "Server":
			return "Information"
		elif header == "Referrer-Policy":
			return "Medium"
		else:
			return " "

	# realiza un escaner al host/s apuntado.
	def do_active_scan(self, event):
		_lista_urls = self._tab5_target.text.split("\n")
		for _x_url in _lista_urls:
			_target_url = URL(_x_url)
			_target_request = self._helpers.buildHttpRequest(_target_url)	
		
			_host = _target_url.getHost()
			_port = _target_url.getDefaultPort()
			_isHttps = True if _target_url.getProtocol()=="https" else False
			
			try:
				self._callbacks.doActiveScan(_host, _port, _isHttps, _target_request)
			except:
				pass
		return

class BurpNewTab(ITab):

	def __init__(self, extender):
		self._callbacks = extender._callbacks

	# @override
	def getUiComponent(self):
		#Creamos el contenido de la extension
		contenedor = Mi_Extension(self).create()
		#Le damos el aspecto propio de la GUI de BurpSuite
		self._callbacks.customizeUiComponent(contenedor)
		return contenedor

	# @override
	def getTabCaption(self):
		return "L-Tools"

class BurpExtender(IBurpExtender):

	# @override
	def registerExtenderCallbacks(self, callbacks):

		# keep a reference to our callbacks object
		self._callbacks = callbacks

		# obtain an extension helpers object
		self._helpers = callbacks.getHelpers()

		# Damos nombre a la extensión
		callbacks.setExtensionName("L-Tools")

		# Instanciamos la clase BurpNewTab para incluirla
		tab = BurpNewTab(self)
		callbacks.addSuiteTab(tab)
		print 'Plug-in L-Tools v1.0  Loaded!'

		return