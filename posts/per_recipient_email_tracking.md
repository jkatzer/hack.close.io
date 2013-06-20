---
Title: Building Per-Recipient Email Tracking
Date: June 21, 2013
Published: True
---

Building Per-recipient tracking pixels
-----------------------------
By utilizing SMTPs RCPT TO command, we can send unique message content to each recipient of an email while still having recipients believe they are receiving the same message. Modifying an example from [Wikipedia's SMTP article](http://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol#SMTP_transport_example), we can illustrate how this would work in practice:

```text
S: 220 smtp.example.com ESMTP Postfix
C: HELO relay.example.org
S: 250 Hello relay.example.org, I am glad to meet you
C: MAIL FROM:<anthony@close.io>
S: 250 Ok
C: RCPT TO:<alice@example.com>
S: 250 Ok
C: DATA
S: 354 End data with <CR><LF>.<CR><LF>
C: From: "Anthony" <anthony@close.io>
C: To: "Alice" <alice@example.com>, "Bob" <bob@example.com>
C: Date: Thurs, 23 May 2013 16:02:43 -0500
C: Subject: Test message
C:
C: Hello Alice!
C: .
S: 250 Ok: queued as 1234
C: MAIL FROM:<anthony@close.io>
S: 250 Ok
C: RCPT TO:<bob@example.com>
S: 250 Ok
C: DATA
S: 354 End data with <CR><LF>.<CR><LF>
C: From: "Anthony" <anthony@close.io>
C: To: "Alice" <alice@example.com>, "Bob" <bob@example.com>
C: Date: Thurs, 23 May 2013 16:02:43 -0500
C: Subject: Test message
C:
C: Hello Bob!
C: .
S: 250 Ok: queued as 1235
C: QUIT
S: 221 Bye
```

Notice how we're sending 2 different messages (Hello Alice! vs Hello Bob!) with the same To/From/Cc/Date/Subject. This provides the basis to add unique tracking pixel to every email sent and maintain normal email behavior for our senders.

To generate our tracking pixels we encode both the Email.id and email address for every recipient in the TO/CC/BCC of the email. By base64 encoding the unique data (email_id and recipient_email) we're able to have a unique pixel_url for every recipient and still be able to correlate it back to the original message.

```python
for recipient in email_to + email_cc + email_bcc:
    pixel_url = "/email_opened/%s/tracking.png" 
                    % base64.b64encode(json.dumps({'email_id': 'emai_123ABC', 
                                                    'email_address': recipient'}))
```

Every time a tracking image URL is requested from an email client, our app responds with the [smallest transparent 1x1 PNG](http://garethrees.org/2007/11/14/pngcrush/) representation and asynchronously creates an EmailOpen(datetime_opened, email_id, email_address) event in our database.

-anemitz
