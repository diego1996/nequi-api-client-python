# nequi-api-client-python #

### Ejemplo para el consumo del API de Nequi en Python  ###

El propósito de este ejemplo es ilustrativo para aquellos interesados en la integración con el API de Nequi. Con este ejemplo podrá consumir algunos de los recursos ofrecidos por el API,y si lo desea podrá utilizar este código como base para el consumo del resto de recursos expuestos en el API. Para más información visite nuestro portal para desarrolladores [https://conecta.nequi.com.co](https://conecta.nequi.com.co "Nequi Conecta").

## 1. Preparación del ambiente

### Credenciales de acceso

Asegúrese de tener las credenciales necesarias para hacer el consumo del API, los datos mínimos que debe tener son:
- Client Id
- Client Secret
- API Key

Los anteriores datos los podrá encontrar en la sección **Credenciales** en el siguiente enlace [https://conecta.nequi.com/content/consultas](https://conecta.nequi.com/content/consultas "Nequi Conecta").

### Archivo de configuración

En el archivo ```/app.example.env``` podrá encontrar un ejemplo de las credenciales que debe proveer. Además también encontrará algunas definiciones adicionales que se usan en los ejemplos.

*Tenga en cuenta que los ejemplos toman como premisa que las credenciales y las definiciones adicionales están almacenadas en **variables de entorno**.*

### Librería 'requests'

Todos los ejemplos aquí proporcionados usan la librería [requests](https://pypi.org/project/requests/) para hacer el consumo de los endpoints. Usted y su equipo de desarrollo es libre de usar cualquier librería que le provea una abstracción para el consumo de APIs Restful o de crear su propio código para dicha integración.

## 2. Ejemplos de integración

Recuerde que podrá encontrar el detalle de los recursos ofrecidos por el API en el siguiente enlace [https://docs.conecta.nequi.com.co/](https://docs.conecta.nequi.com.co/).


--------

### Autenticación en Nequi Conecta

En el archivo ```/src/auth.py``` podrá encontrar el código necesario para autenticarse, el cual le permite obtener un token de acceso que deberá usar en las integraciones del API.

### Depósitos y Retiros

Esta sección cuenta con 3 ejemplos que podrá encontrar alojados en la carpeta ```/src/deposit_withdrawal/```.

- **Validar una cuenta**: En el archivo ```/src/deposit_withdrawal/validate_client.py``` podrá encontrar el código para validar una cuenta.

- **Recargar una cuenta**: En el archivo ```/src/deposit_withdrawal/charge_accpunt.py``` podrá encontrar el código para recargar una cuenta.

- **Verificar una solicitud de retiro**: En el archivo ```/src/deposit_withdrawal/check_withdrawal.py``` podrá encontrar el código para validar una cuenta.

### Pagos con QR code

Esta sección cuenta con 3 ejemplos que podrá encontrar alojados en la carpeta ```/src/payment/```.

- **Generar pago**: En el archivo ```/src/payment/generate_qr.py``` podrá encontrar el código para generar un pago con código QR.

- **Consultar estado del pago**: En el archivo ```/src/payment/get_status_payment.py``` podrá encontrar el código para consultar el estaddo un pago con código QR.

- **Reversar la transacción**: En el archivo ```/src/payment/reverse_transaction.py``` podrá encontrar el código para reversar una transacción.

### Pagos con notificación

Esta sección cuenta con 1 ejemplo que podrá encontrar alojados en la carpeta ```/src/payment_push/```.

- **Solicitud de pago**: En el archivo ```/src/payment_push/unregistered_payment.py``` podrá encontrar el código para solicitar un pago mediante notificación push.

## 3. Ejecutar los ejemplos

Para ver en funcionamiento de los ejemplos, descargue los fuentes, desplieguelos en cualquier servidor donde corra Python, puede ser Apache, y acceda al archivo ```/src/main.py``` desde una consola o terminal.

Si lo desea también puede desplegar estos ejemplos usando [docker](https://www.docker.com/) y [docker-compose](https://docs.docker.com/compose/), ejecutando el siguiente comando en la raíz del proyecto:
- ```docker-compose up```: Este comando puede tomar unos minutos mientras se descargan los recursos necesarios, al final quedará la terminal de comandos en modo activo, lo cual le permitirá detener el despliegue presionando ```Ctrl + c```.

## 4. Información adicional

- Carpeta ```/src/utils/```: Aquí podrá encontrar funciones que se reusan en los ejemplos de integración, y constantes para validar resultados del API.

----------
*Made with ♥ by Diego A Asencio C*
