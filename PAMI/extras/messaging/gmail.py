__copyright__ = """
Copyright (C)  2021 Rage Uday Kiran

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import smtplib, ssl


from email.message import EmailMessage

class gmail:

    def __init__(self, userName: str, password: str) -> None:
        self.userName = userName
        self.password = password


    def send(self, toAddress: str, subject: str, body: str) -> None:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        try:

            smtp_server.starttls()
            smtp_server.login(self.userName, self.password)

            message = EmailMessage()
            message.set_content(body)

            message['Subject'] = subject
            message['From'] = self.userName
            message['To'] = toAddress

            smtp_server.send_message(message)
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            smtp_server.quit()