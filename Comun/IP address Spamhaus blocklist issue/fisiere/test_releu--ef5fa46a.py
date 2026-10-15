#!/usr/bin/env python3
# Test releu hosterion: trimite office@eva-org.com -> admin@eva-org.com prin mail.cesiro.ro:465, apoi citeste antetele din INBOX admin@.
import smtplib, ssl, sys, uuid, time, imaplib, re
pw, apw = sys.argv[1], sys.argv[2]
tag = uuid.uuid4().hex[:10]
msg = ("From: Office EVA <office@eva-org.com>\r\nTo: admin@eva-org.com\r\nSubject: Test releu hosterion %s\r\n"
       "Date: %s\r\nMessage-ID: <%s@eva-org.com>\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nTest releu %s\r\n"
       % (tag, time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime()), tag, tag))
s = smtplib.SMTP_SSL('mail.cesiro.ro', 465, timeout=30); s.ehlo('mx.eva-org.com'); s.login('noreply@cesiro.ro', pw)
print('sendmail:', s.sendmail('office@eva-org.com', ['admin@eva-org.com'], msg.encode())); s.quit()
print('tag', tag)
c = ssl._create_unverified_context()
for i in range(30):
    time.sleep(3)
    m = imaplib.IMAP4_SSL('127.0.0.1', 4993, ssl_context=c); m.login('admin@eva-org.com%admin', apw); m.select('INBOX', readonly=True)
    t, d = m.search(None, 'SUBJECT', '"%s"' % tag)
    if d[0]:
        raw = m.fetch(d[0].split()[-1], '(BODY.PEEK[HEADER])')[1][0][1].decode(errors='replace'); m.logout()
        print('SOSIT dupa', (i + 1) * 3, 's')
        for l in re.split(r'\r\n(?!\s)', raw):
            if l.lower().startswith(('received:', 'from:', 'sender:', 'return-path:', 'authentication-results:', 'x-spam', 'dkim-signature', 'x-sender', 'x-authenticated')):
                print(' ', l.replace('\r\n', ' ')[:400])
        break
    m.logout()
else:
    print('NU a sosit in 90s')
