#!/usr/bin/env python3
# Test cap-coada: admin@eva-org.com -> covaciu.gnm@gmail.com prin submission Stalwart (4587 STARTTLS); ruta de iesire trebuie sa fie releul hosterion.
import smtplib, ssl, sys, uuid, time, os
sys.path.insert(0, '/home/saga-server/server-mail-stalwart/scripts'); from parole import parola
tag = uuid.uuid4().hex[:10]
msg = ("From: Admin EVA <admin@eva-org.com>\r\nTo: covaciu.gnm@gmail.com\r\nSubject: Test iesire prin releu hosterion %s\r\n"
       "Date: %s\r\nMessage-ID: <%s@eva-org.com>\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n"
       "Test tehnic 13.10.2026: mail trimis din Stalwart (mx.eva-org.com) prin releul mail.cesiro.ro, dupa listarea Spamhaus a IP-ului 5.15.130.140. Marcaj %s.\r\n"
       % (tag, time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime()), tag, tag))
c = ssl._create_unverified_context()
s = smtplib.SMTP('127.0.0.1', 4587, timeout=30); s.starttls(context=c); s.login('admin@eva-org.com', parola('admin@eva-org.com'))
print('submit:', s.sendmail('admin@eva-org.com', ['covaciu.gnm@gmail.com'], msg.encode())); s.quit()
print('tag', tag)
