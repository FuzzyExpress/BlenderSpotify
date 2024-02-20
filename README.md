# Blender Spotify
Always having to start and stop Blender and my Music player independently is annoying. 
That's why I wrote Blender Spotify: automatically start and stop Spotify so it does not overlap viewport playback.
The premise is simple: If blender has audio enabled, and a sound track is present, and Spotify is playing audio: stop Spotify when viewport playback is started, and resume it when viewport Playback is stopped. 

## Important Notes:
- only Linux or other systems with playerctl are supported.
- `playerctl` is reqired and should be in PATH.
- The addon is for Blender 4.1, ~~though anything 4.0+ should work (untested)~~ Nope. (Tested 3.6.8 & 4.0.2, neither did anything)
- Also my code is trash and it seems to just not work half the time, I'll see if I can get that fixed.
- *Note that it does not currently acount for muted or blank sound strips


## Demo:
https://github.com/FuzzyExpress/BlenderSpotify/assets/127012288/2809cbd0-8dfd-482e-919a-0622bc2ed1e6

**Demo Credits:**

[What's up with Furball? - Move or Die - by Jacob Lincke - Spotify](https://open.spotify.com/track/2pxWLBzFBOZQMgufBIbSgg?si=d7a51488ae624d77)

[The Minecraft Mod: VS Clockwork](https://www.valkyrienskies.org/clockwork)
