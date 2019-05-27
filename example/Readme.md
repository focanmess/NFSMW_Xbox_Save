# Example Files

| Save Game   | Description                                 |
|-------------|---------------------------------------------|
| JASON       | Save game with $9,718,000 in cash.          |
| JASON_10mil | Save game with cash changed to $10,000,000. |

Compare the files to note the modified HMAC-SHA1 and MD5 fields, in addition to the modified cash value.

```
Need for Speed: Most Wanted Xbox Save Game Editor / Fixer

Reading game save file "JASON" ...

Modified cash to 10000000 (was 9718000).

Updating hashes ...

Hashes:
  Game Save Data MD5:           505670117466457d4b339f7216e1076b          [UPDATED]
  Header Data HMAC-SHA1:        7c003b7d4ac5fcb110cd0618ee39c0befeece4fd
  Game Save Data HMAC-SHA1:     962d18ac24b8ba48eb01895b70c89673fadae603  [UPDATED]
  Header HMAC-SHA1:             782d69f5707932f8814cc609c0ca7933b76cb501  [UPDATED]

Writing new game save file "JASON_10mil" ...

Finished! Copy the save game to an Xbox.
```
