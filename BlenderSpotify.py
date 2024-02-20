import bpy, sys, threading, time, subprocess
sys.path.append('/home/fexp/.local/lib/python3.11/site-packages')
from PyQt5 import QtDBus

bl_info = {
    "name": "Blender Spotify",
    "author": "FuzzyExpress",
    "version": (0, 0, 1, 20),
    "description": """Automatically Pause or Play Spotify based on Blender Viewport Playback
    !! REQUIRES `PyQt5` and `playerctl` !!""",
    "blender": (4, 1, 0),
    "category": "Interface",
}

PlayerName = 'spotify' # change this to what ever media player you prefer

global BlenderSpotifyMC
BlenderSpotifyMC = None

class MusicController:
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Controller Start Stop | Modal Timer Operator"

    def __init__(self):
        self.service = f'org.mpris.MediaPlayer2.{PlayerName}'
        self.path    = '/org/mpris/MediaPlayer2'
        self.iface   = 'org.mpris.MediaPlayer2.Player'
        self.props   = 'org.freedesktop.DBus.Properties'
        
        try:
            self.smp = QtDBus.QDBusInterface(self.service, self.path, self.props)
        except AttributeError:
            print("Failed to create D-Bus interface. Make sure you have PyQt5 installed.")

        self.Playing         = False
        self.SetPlaying      = False
        playing = True if 'Playing' in self.smp.call('Get', self.iface, 'PlaybackStatus').arguments()[0] else False
        self.MusicPlaying    = playing
        self.MusicWasPlaying = playing
        self.Frame = -1

        # Create the thread object but don't start it yet
        self.MC_Thread = threading.Thread(target=self.TimerLoop, daemon=True)

        # Start the thread
        self.Running = True
        self.MC_Thread.start()

    def IsRunning(self):
        return self.Running;

    def setBlenderPlaying(self, p):
      #  print(f'set playing to {p}')
        self.SetPlaying = 1 if p else 0
        
    def Close(self):
        # Join the thread to wait for it to finish
        self.Running = False
        self.MC_Thread.join()

    def TimerLoop(self):
        while self.Running:
            if True:

              #  LastFrame = self.Frame
              #  self.Frame = bpy.data.scenes["Scene"].frame_current
                                
                LastPlaying = self.Playing
                self.Playing = self.SetPlaying > 0 #get play state(boolean) 
                self.SetPlaying -= 1;

                msg = self.smp.call('Get', self.iface, 'PlaybackStatus')

                LastMusicPlaying = self.MusicPlaying
                self.MusicPlaying = True if 'Playing' in msg.arguments()[0] else False

                if LastPlaying != self.Playing: 
                  #  print('Blender Playing Changed:', self.Playing)
                    if self.Playing:
                        self.MusicWasPlaying = self.MusicPlaying;
                    #  print('Was Playing:', self.MusicPlaying)
                    

                if LastMusicPlaying != self.MusicPlaying: ...
                  #  print(PlayerName, 'Playing Changed:', self.MusicPlaying)

                if self.Playing and self.MusicPlaying:
                  #  self.MusicWasPlying = True;

                    ## put stop playing here
                  #  print('Try Pause')
                    subprocess.run(f'playerctl -p {PlayerName} pause', shell=True)

                if not self.Playing and self.MusicWasPlaying:
                    self.MusicWasPlaying = False;

                    ## put start playing here
                  #  print('Try Play')
                    subprocess.run(f'playerctl -p {PlayerName} play', shell=True)
                
              #  print(self.Playing, self.MusicPlaying, self.MusicPlaying)

                time.sleep(1/2)

            else:
                time.sleep(10)


class UnregisterOperator(bpy.types.Operator):
    """Operator to unregister Modal Timer Operator"""
    bl_idname = "wm.unregister_operator"
    bl_label = "MusicController Unregister Operator"

    def execute(self, context):
        global BlenderSpotifyMC
        BlenderSpotifyMC.Close()
        unregister()
        return {'FINISHED'}


def is_sound_strip_present():
    # Get the active sequence editor
    seq_editor = bpy.context.scene.sequence_editor

    # Check if the sequence editor exists and has strips
    if seq_editor is not None and seq_editor.sequences:
        # Iterate through all sequences
        for seq in seq_editor.sequences:
            # Check if the sequence is a sound strip
            if seq.type == 'SOUND':
                return True
    return False



def menu_func(self, context):
    self.layout.operator(MusicController.bl_idname, text=MusicController.bl_label)
    self.layout.operator("wm.unregister_operator", text="Unregister Operator")



def register():
    global BlenderSpotifyMC
    BlenderSpotifyMC = MusicController()
    
    bpy.utils.register_class(UnregisterOperator)
    bpy.types.VIEW3D_MT_view.append(menu_func) 

    bpy.app.handlers.frame_change_post.append(frame_change_handler)
    

# Register and add to the "view" menu (required to also use F3 search "Modal Timer Operator" for quick access).
def unregister():
    bpy.utils.unregister_class(UnregisterOperator)
    bpy.types.VIEW3D_MT_view.remove(menu_func)
    
    bpy.app.handlers.frame_change_post.remove(frame_change_handler)


def frame_change_handler(scene):
    # Call setBlenderPlaying method with the updated play state
    if bpy.data.scenes["Scene"].use_audio:
        if is_sound_strip_present():
            BlenderSpotifyMC.setBlenderPlaying(bpy.context.screen.is_animation_playing)


if __name__ == "__main__":
    register()
