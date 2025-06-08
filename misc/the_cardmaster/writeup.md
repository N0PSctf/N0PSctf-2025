## The Cardmaster

### Description

Remember Joe Dohn from last year ?
He is back with a new concept now: N0PS TCG.
Try to get in touch with him, he will tell you more about that !

**Author: algorab & Sto**

### Solution
We are facing a discord bot that generates amazing N0PS TCG cards. Each player can get their own personnalized card, how amazing!
But maybe there is a flaw somewhere...
By trying the `!help` command, we can see that there is a `!devlog` command. Here is the content we can get when entering `!devlog`:

- sensitive information stored in dotenv file
- card generation script (the final echo is used for the bot to get the image path!):
```bash
#!/bin/bash

#os.popen(f"/app/create_card.sh '{card_class}' '{display_name}' '{discord_tag}' '{', '.join(card_abilities)}' '{profile_picture}' '{id}' '{card_rarity_name}'")

find /tmp -iname *.pdf -delete 2>/dev/null
find /tmp -iname *.html -delete 2>/dev/null

uuid=$(cat /proc/sys/kernel/random/uuid)

cat /app/template.html \
| sed -e "s/card_class/${1}/g" \
| sed -e "s/display_name/${2}/g" \
| sed -e "s/discord_tag/${3}/g" \
| sed -e "s/abilities/${4}/g" \
| sed -e "s/profile_picture/${5}/g" \
| sed -e "s/card_id/${6}/g" \
| sed -e "s/card_rarity/${7}/g" \
> /tmp/$uuid.html

python3 -c "import weasyprint; weasyprint.HTML('/tmp/${uuid}.html').write_pdf('/tmp/${uuid}.pdf')"

pdftoppm -singlefile -jpeg -r 300 /tmp/$uuid.pdf /tmp/$uuid

echo /tmp/$uuid.jpg

```
- TODO: remove devlog from bot commands (but who will look at it anyway)
- TODO: implement powerful AI to play N0PStopia - TCG 

It gives us precious insight: the card is generated through a script, using the `os.popen` function, and the bot can get the path of the image by reading the output of the command. Therefore, if we can find a way to change the output of the command, we can possibly read any file (including the juicy `.env` file mentioned!).
For that, we can change our discord nickname on the server to perform a command injection. Here is a username that does the job: `'>/dev/null; echo '.env' #`.
Then, the bot sends us the `.env` file and we can enjoy our flag.

### Flag
`N0PS{w0ulD_U_7r4D3_y0ur_c4rDz_w1tH_m3?}`
