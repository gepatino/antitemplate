# antitemplate
A python proof of concept to convert two similar mails to a template, and then
extract fields from other similar mails



What the test.py file does:

1. loads three similar mails (mail_01.txt, mail_02.txt and mail_03.txt)
2. does some prettifying of the html content
3. gets the diff from mail_01 and mail_02
4. display each diff lines compared, and ask for a field name
5. creates a template using the first mail as a base, replacing the lines for
   the field names.
6. compares each mail against the created template
7. now the diff should show the field names replaced in the template from one
   side, and the field values on the other side.
8. store the fields and values, and print them


This is just a proof of concept, the difficult part would be to decide which
template to use when a new mail is processed.
 
A big drawback is that it doesn't detect useful values that are the same in the
two mails used to create the template (example: credit card info, user name,
user profile, etc)
