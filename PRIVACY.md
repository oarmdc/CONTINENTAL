# Privacy Policy — CONTINENTAL

**Last updated: July 19, 2026**

This policy explains what data the CONTINENTAL Discord bot ("the bot") collects and how it is used.

## 1. Data we store

The bot stores the following data persistently in a private database:

| Data | Purpose | Stored until |
|---|---|---|
| Discord user ID + server ID | Leveling system (XP, level) | You leave or data is reset/deleted |
| Discord user ID + birthday (day and month only — no year) | Birthday reminders | You remove it via `/removebirthday` or request deletion |

We never store your birth year, real name, email address, or any payment information. We do not use cookies or tracking technologies.

## 2. Data processed temporarily

- **Deleted/edited messages**: the most recently deleted or edited message per channel is kept **in memory only** to power the snipe commands. This data is never written to disk and is erased whenever the bot restarts or a newer message replaces it.
- **Message activity**: messages are counted for XP purposes; the content of your messages is not stored.
- **Music queries**: search terms and links you submit to music commands are passed to our audio server and third-party sources (SoundCloud, Spotify, YouTube) to find tracks. They are not stored by us.
- **Voice state**: the bot reads voice channel membership to manage music playback. It cannot and does not listen to or record voice audio.

## 3. What we do NOT do

- We do **not** sell, rent, or share your data with third parties.
- We do **not** use your data for advertising or profiling.
- We do **not** read or store your message content beyond the temporary snipe feature described above.

## 4. Data storage & security

Data is stored in a database on private infrastructure accessible only to the developers. Access is protected by authentication. As a hobby project, no absolute security guarantee can be given — please do not submit sensitive information through bot commands.

## 5. Third-party services

Music features rely on SoundCloud, Spotify, and YouTube. Your search queries are transmitted to these services to fulfil requests; their own privacy policies apply to their processing.

The bot itself operates on Discord — [Discord's Privacy Policy](https://discord.com/privacy) applies to all data handled by the Discord platform.

## 6. Your rights

You can at any time:

- **View** your stored birthday with the bot's commands
- **Delete** your birthday via `/removebirthday`
- **Request full deletion** of all data linked to your user ID (levels, birthday) by contacting us — we will comply within a reasonable time

Users in the EU/EEA additionally have the rights granted by the GDPR (access, rectification, erasure, restriction). Contact us to exercise them.

## 7. Children

The bot is intended for users who meet Discord's minimum age requirement (13, or higher depending on your country). We do not knowingly collect data from users below that age.

## 8. Changes

This policy may be updated at any time. The current version is always available at this page.

## 9. Contact

For any privacy request or question, open an issue on our GitHub repository: [github.com/oarmdc/CONTINENTAL](https://github.com/oarmdc/CONTINENTAL)
