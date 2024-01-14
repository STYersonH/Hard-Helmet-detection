import yagmail
from datetime import datetime

# Get the current date in the format YYYY-MM-DD
current_date = datetime.now().strftime('%Y-%m-%d')

# Define the responsible person and the shift
persona_encargada = "SEGURIDAD PUERTA 6 - AREA DE PREVENCION"
turno = "Mañana"

# Rest of your code
email = "edward.melendez.mendigure@gmail.com"
password = "mpjccskhhqupkzhh"
yag = yagmail.SMTP(user=email, password=password)
senders = ['192666@unsaac.edu.pe']
head = "Reporte de incidentes - CONSTRUCTORA"
body = ""
file_report = 'report.html'
image_filename = 'report.jpeg'

# Read the content of the HTML file
with open(file_report, 'r') as file:
    html_content = file.read()

# Replace the placeholders with the current values
html_content = html_content.replace('%fecha_actual%', current_date)
html_content = html_content.replace('%persona_encargada%', persona_encargada)
html_content = html_content.replace('%turno%', turno)

# Save the modified HTML to a new file (optional)
with open('modified_report.html', 'w') as modified_file:
    modified_file.write(html_content)

# Send the email with the attached report
yag.send(senders, head, [body], attachments=['modified_report.html', image_filename])