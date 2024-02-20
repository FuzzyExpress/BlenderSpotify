# Blender Spotify
Always haveing to start and stop Blender and my Music player indipendantly is annoying.
That's why I wrote Blender Spotify: automaticly start and stop Spotify so it does not overlap viewport playback.
The premis is simple: If blender has audio enabled, and a sound track is present, and Spotify is playing audio: stop Spotify when Viewport Playback is started, and resume it when Viewport Playback is stopped. 

## Important Notes:
- only Linux or other MPRIS systems are supported.
- `PyQt5` and `playerctl` are reqired. (I relized I could just use `playerctl`, I will do this later)
- The addon is for Blender 4.1, though anything 4.0+ should work (untested)
