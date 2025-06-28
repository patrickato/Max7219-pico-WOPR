# Max7219-pico-WOPR
A code for max7219 led matrix with a pi pico to act like the WOPR from WarGames.
I saw a post on Reddit some time ago for a WOPR type light bar using a pi pico and a couple max7219 led matrix's. 
I fell in love with what I saw and since the poster kindly gave his code out for free, I couldn't pass up the opportunity to try it for myself.
From there I decided to add to that code relying heavily on help from ChatGPT. As such I am due ZERO credit for any of this.
Everyone else who's ever made a WOPR project before 6/27/25 deserves full credit. Also, I didn't code not a single line of code by myself. I let AI do that and just tweaked and massaged until I was satisfied.
there is still tons of room to grow this project and I very much welcome everyone to either add your ideas, write additional code and share it, take the sound files and integrate them as part of the routine. Take the whole code and run with it.....it's free use. I just ask that you keep passing it along as free for everyone to enjoy also. This is the way. :)
I will be tweaking the steps as I get better at this. Please forgive, its my first Repo.

You need a Raspberry Pi Pico with headers.
this particular project utilizes 2 max7219 led matrix's with 4 panels per board for a total of 8 panel or 8 x 64 LED's
There are 5 pinned connections to make. the how-to for that is easily found through Google....I will try to add that part later. I used Dupont connectors.
I used Thonny for running the codes, adding the pico, and adding software to the pico. I dont know any other way yet, but surely they are numerous.
press BOOTSEL on the pi while youre plugging the usb from the pico into your pc. If the pc doesnt make a noise, check the cable, ensure you are using one that supplies power AND data transfer. not just power.
add the max7219 library from the github repo.
press stop at the top and make sure you see its connected in the window at the bottom ( red letters = bad ) 
the copy the code into a new template or whatever and save it as main.py to your pico.
Done and Done!

