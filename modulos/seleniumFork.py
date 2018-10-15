import time
from functools import wraps
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.key_actions import KeyActions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import os



class SFork():
	def __init__(self):
		if(os.name == "nt"):
			self.driver_name = "drivers/chromedriverWindows.exe"
		elif(os.name == "posix"):
			self.driver_name = "drivers/chromedriverLinux64"
		else:
			print("SISTEMA DESCONOCIDO..")
			self.driver_name = None
		self.driver = None
		self.elementos = {}
		self.error = {
			1:"El navegador aun no ah sido iniciado.",
			2:"El navegador o el elemento no estan disponibles."
		}
		self.intentos = 0
		self.ultimoElemento = None #registro del ultimo elemento interactuado
		
	def IniciarDriver(self):#Inicializacion de driver
		print("Iniciando Chrome..")
		options1 = Options()
		options1.add_argument("start-maximized")
		options1.add_argument("--incognito")
		#options1.binary_location = "C:\\Program Files\\Hola\\app\\chromium\\"
		self.driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=options1)
		
	
	def completarFormulario(self, form):
		print("Completando formulario.")
		for e in form:
			self.buscarCompletar(e, form[e])
		print("Fin de completado.")
			
	def verificarDriver(func):
		#Decorador que verifica que el driver se este ejecutando antes de emplear una accion
		@wraps(func)
		def _exec_(self, *args, **kwargs):
			if(self.driver != None):
				func(self, *args, **kwargs)
			elif(args[1] != None or args[1] != False):
				func(self, *args, **kwargs)
			else:
				self.pError(1)
			return False
		return _exec_
	
	def Verificar(self, element=True):#Verificar elemento y driver encendido
		if(self.driver == None):
			self.pError(2)
			return False
		elif(element == None or element == False):
			self.pError(2)
			return False
		else:
			return True
			
	def pError(self,error_id=None):#Lanzar algun error
		if error_id in self.error:
			print(self.error[error_id])
		else:
			print("Error desconocido.")
			
	@verificarDriver
	def Cerrar(self):
		print("Saliendo de Google Chrome")
		self.driver.quit()
		
	@verificarDriver
	def Ir(self, pagina="google.com"):#Redirigir a una pagina
		print("Dirigiendose a %s"%(pagina))
		self.driver.get(pagina)

	@verificarDriver
	def irAtras(self):
		self.driver.back()
	
	@verificarDriver
	def irAdelante(self):
		self.driver.forward()
	
	def buscarCompletar(self, name, texto="notexto"):
		#Busca un elemento y escribe algo sobre el (TextBoxs)
		print("[+]Buscando y escribiendo en %s"%name)
		self.escribirEn(self.Buscar(name), texto)
		
	# def Buscar(self,nombre,tipo="id"):
	# 	#Buscar elemento en la pagna actual
	# 	elemento = None
	# 	if(nombre in self.elementos):
	# 		for i in self.elementos[nombre]:
	# 			elemento = self.BuscarPor(i, tipo)
	# 			if(elemento != False):
	# 				print("  [v]Se localizo el elemento %s correctamente."%nombre)
	# 				self.ultimoElemento = elemento
	# 				return elemento
	# 			time.sleep(1)
				
	# 		tipos_ = ["name","id"]
	# 		print("[+]Buscando elemento:\"%s\" por todos los tipos.."%(nombre))
	# 		for tipo in tipos_:
	# 			print("[+]Se encontro el elemento:\"%s\" con el tipo %s.."%(nombre, tipo))
	# 			for i in self.elementos[nombre]:
	# 				elemento = self.BuscarPor(i, tipo)
	# 				if(elemento):
	# 					self.ultimoElemento = elemento
	# 					return elemento
	# 		print("  [x]No se encontro el elemento \"%s\""%nombre)
	# 	return None

	def Buscar(self,nombre,tipo="id"):
		#Buscar elemento en la pagna actual
		elemento = None
		if(nombre in self.elementos):
			for i in self.elementos[nombre]:
				elemento = self.BuscarPor(i, tipo)
				if(elemento != False):
					print("  [v]Se localizo el elemento %s correctamente."%nombre)
					self.ultimoElemento = elemento
					return elemento
				time.sleep(1)
				
		tipos_ = ["name","id"]
		print("[+]Buscando elemento:\"%s\" por todos los tipos.."%(nombre))
		for tipo in tipos_:
			elemento = self.BuscarPor(nombre, tipo)
			if(elemento):
				print("  [v]Se localizo el elemento %s correctamente."%nombre)
				self.ultimoElemento = elemento
				return elemento
		print("  [x]No se encontro el elemento \"%s\""%nombre)
		return None
	
	def BuscarPor(self,name,tipoElemento="id"):#Buscar elemento por tipo especifico
		# print("[+]Buscando elemento:\"%s\" por %s"%(name,tipoElemento))
		try:
			if(tipoElemento == "id"):
				return self.driver.find_element_by_id(name)
			
			elif(tipoElemento == "name"):
				return self.driver.find_element_by_name(name)
			
			elif(tipoElemento == "link"):
				return self.driver.find_element_by_link_text(name)
				
			elif(tipoElemento == "css"):
				return self.driver.find_element_by_css_selector(name)
				
			elif(tipoElemento == "xlink"):
				return self.driver.find_element_by_partial_link_text(name)
			
			elif(tipoElemento == "class"):
				return self.driver.find_element_by_class_name(name)
			
			elif(tipoElemento == "tag"):
				return self.driver.find_element_by_tag_name(name)
			elif(tipoElemento == "xpath"):
				return self.driver.find_element_xpath(name)
			else:
				return self.driver.find_element_xpath("//input[@id='%s']"%name)
		except:
			return False
		
	@verificarDriver
	def vaciarCaja(self, element): #REVISAR
		#Vaciar caja o elemento
		try:
			element.clear()
			element.clear()
			print("Elemento vaciado.")
		except:
			print("Error al borrar el elemento.")
	
	@verificarDriver
	def escribirEn(self, element, text):
		#Tipea texto sobre elemento
		if(element != None and text != None):
			element.clear()
			element.send_keys(text)
			try:
				print("Se ah completado el campo %s con:\"%s\""%(str(element.get_attribute("name")),str(text)));
			except:
				# print(element)
				pass
	
	@verificarDriver
	def escribirEnTextBox(self, element, text):
		#Tipea texto sobre elemento pero no borra(para listabox)
		if(text != None):
			element.send_keys(text)
			print("Se ah completado el campo %s con:\"%s\""%(str(element.get_attribute("name")),str(text)));
	
	def Enter(self, element=None ):
		#Presiona la tecla enter sobre un elemento o el ultimo interactuado
		if(element is None):
			element = self.ultimoElemento
		if(self.Verificar(element)):
			print("Apretando enter..")
			element.send_keys(Keys.ENTER)
			
	@verificarDriver
	def sKey(self, KEY, element):
		print("Presionando ",KEY)
		element.send_keys(KEY)
	
	@verificarDriver	
	def Salir(self):
		print("Cerrando..")
		self.driver.close()
	
	@verificarDriver
	def Clickear(self, element):
		#Hacer click sobre elemento
		try:
			d = element.click()
			return True
		except:
			return False
		
	def ClickearObjeto(self, nombre, urlref=None):
		try:
			print("Clickeando objeto")
			self.Clickear(self.BuscarPor(nombre, "css"))
			if(self.driver.current_url == urlref):
				self.ClickearObjeto(nombre, urlref)
		except:
			print("Error al clickear")

	def PresionarObjeto(self, nombre):
		self.Enter(self.BuscarPor(nombre, "css"))
		
	@verificarDriver	
	def Esperar(self, segs=10):
		#Tiempo de espera en navegador
		print("Tiempo de espera re estrablecido a %s segundos"%segs)
		time.sleep(segs)
		
	def Pausa(self, segs=5):
		print("Esperando %s segundos en el script."%segs)
		time.sleep(5)
	
	def verificarErrorPassword(self, tiempo=5):#Esperar x tiempo hasta que se encuentre el elemento
		# print("Esperando a que el elemento \"%s\" sea cargado"%nombre_elemento)
		print("[+] Buscando si existe el mensaje de error de clave. #{} intentos disponible para detectar, antes de cerrar".format(tiempo))
		try:
			element = WebDriverWait(self.driver, 1).until(lambda driver: self.driver.find_elements_by_class_name("ui-message-contents"))
			if '/loginHelp' in element[0].get_attribute('innerHTML'):
				# print(element[0].get_attribute('innerHTML'))
				return True
		except:
			tiempo -= 1
			time.sleep(1)
			if tiempo > 1:
				self.verificarErrorPassword(tiempo)
			else:
				return False
	
	def verificarErrorExists(self, tiempo=5):#Esperar x tiempo hasta que se encuentre el elemento
		# print("Esperando a que el elemento \"%s\" sea cargado"%nombre_elemento)
		print("[+] Buscando si existe el mensaje de cuenta inexistente. #{} intentos disponible para detectar, antes de cerrar".format(tiempo))
		try:
			element = WebDriverWait(self.driver, 1).until(lambda driver: self.driver.find_elements_by_class_name("ui-message-contents"))
			# print(element[0].get_attribute('innerHTML'))
			if 'href="/"' in element[0].get_attribute('innerHTML'):
				# print(element[0].get_attribute('innerHTML'))
				return True
		except:
			tiempo -= 1
			time.sleep(1)
			if tiempo > 1:
				self.verificarErrorExists(tiempo)
			else:
				return False
	
	def verificarProfiles(self, tiempo=5):#Esperar x tiempo hasta que se encuentre el elemento
		# print("Esperando a que el elemento \"%s\" sea cargado"%nombre_elemento)
		print("[+] Buscando el url del perfil primario. #{} intentos disponible para detectar, antes de cerrar".format(tiempo))
		try:
			element = WebDriverWait(self.driver, 1).until(lambda driver: self.driver.find_elements_by_class_name("profile-link"))
			# print(element[0].get_attribute('innerHTML'))
			# profile = element[0].find_elements_by_xpath("//a[@class='profile-link']")[0]
			# print(profile.get_attribute('innerHTML'))
			# profile = profile.get_attribute("href")
			# print(profile)
			if '/SwitchProfile?' in element[0].get_attribute('href'):
				# print(element[0].get_attribute('href'))
				return element[0].get_attribute('href')
		except:
			tiempo -= 1
			time.sleep(1)
			if tiempo > 1:
				self.verificarProfiles(tiempo)
			else:
				return False
	
	def verificarPagoPerfil(self, tiempo=5):#Esperar x tiempo hasta que se encuentre el elemento
		# print("Esperando a que el elemento \"%s\" sea cargado"%nombre_elemento)
		print("[+] Buscando si se debe actualizar el metodo de pago. #{} intentos disponible para detectar, antes de cerrar".format(tiempo))
		try:
			element = WebDriverWait(self.driver, 1).until(lambda driver: self.driver.find_elements_by_class_name("payment-hold-body"))
			# print(element[0].get_attribute('innerHTML'))
			# profile = element[0].find_elements_by_xpath("//a[@class='profile-link']")[0]
			# print(profile.get_attribute('innerHTML'))
			# profile = profile.get_attribute("href")
			# print(profile)
			if 'payment-hold-body' in element[0].get_attribute('class'):
				return True
		except:
			tiempo -= 1
			time.sleep(1)
			if tiempo > 1:
				self.verificarPagoPerfil(tiempo)
			else:
				return False
	
	def verificarConfirmacionFail(self, tiempo=2):#Esperar x tiempo hasta que se encuentre el elemento
		# print("Esperando a que el elemento \"%s\" sea cargado"%nombre_elemento)
		print("[+] Buscando si existe el mensaje de error. #{} intentos disponible para detectar, antes de cerrar".format(tiempo))
		try:
			element = WebDriverWait(self.driver, 1).until(lambda driver: self.driver.find_elements_by_class_name("nf-message-warn"))
			# print(element[0].get_attribute('innerHTML'))
			# profile = element[0].find_elements_by_xpath("//a[@class='profile-link']")[0]
			# print(profile.get_attribute('innerHTML'))
			# profile = profile.get_attribute("href")
			# print(profile)
			if 'nf-message-warn' in element[0].get_attribute('class'):
				return True
		except:
			tiempo -= 1
			time.sleep(1)
			if tiempo > 1:
				self.verificarPagoPerfil(tiempo)
			else:
				return False
	
	@verificarDriver
	def mMouse(self, element):
		print("Moviendo mouse sobre el elemento \"%s\""%element.get_attribute("name"))
		ActionChains(self.driver).move_to_element(element)
	
	@verificarDriver
	def sSeleccionarElemento(self, element):#Seleccionar item en caja opciones
		ActionChains(self.driver).move_to_element(element).click(element).perform()

	def buscarEnCodigoFuente(self,strings):
		if type(strings) == list:
			for i in strings:
				if i in str(self.driver.page_source):
					return True
		if type(strings) == str:
			if i in str(self.driver.page_source):
				return True
		return False

			
