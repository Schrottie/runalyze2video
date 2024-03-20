# runalyze2video

Python tool that reads the data from the public athlete page at runalyze.com and processes the running activities in a video (e.g. for the Instagram story). The video has a bar chart at the bottom that shows the evaluated activities, while the individual runs and then a summary are shown at the top.

## Running on Raspi

I use the script with a Raspberry Pi. It is always started at the end of the month. It is important to do this before the end of the month, as the next month already appears on the public athlete page on the following day (first of the month).

The following crontab entry is recommended for this: 

`0 23 L * * /home/user/runalyze2video/python.py`

The path to the script must of course be adapted. A brief explanation of the entry:

**Minute:** 0 - The minute in which the command is executed. In this case 59 minutes after the 23rd hour.
**Hour:** 23 - The hour in which the command is executed. In this case 11 pm.
**Day:** L - The day of the month on which the command is executed. In this case L for the last day of the month.
**Month:** * - The month in which the command is executed. In this case * for each month.
**Day of the week:** * - The day of the week on which the command is executed. In this case * for each day of the week.
**Command:** /home/user/runalyze2video/python.py - The path to the Python script to be executed.

## Wishlist

* Intro and individual clips could also be faded in or - even better - cross-faded.
* It would be extremely cool if the diagram were built up analogously to the individual data record clips and did not appear complete right from the start.
* Until the runalyze API also offers read access, this variant is the only practicable way to access the data. You can now also go directly to the JSON endpoint, but this requires you to authenticate yourself to runalyze.com. Again, this is not entirely trivial, so if anyone has an idea for this, please let me know.
Then I would use a local database for data storage and the creation of the video would be much more convenient (certain time periods, certain sports, etc.).

## Biking?

Currently, only running activities are processed. If you want to use the script for cycling activities, you must adjust the detection in the `extract_activity_data` function. Currently, the script searches for `icons8-Running`. With `icons8-Regular-Biking` you would then find bike rides. But hey, if you want to do something like that, you can find out for yourself.
