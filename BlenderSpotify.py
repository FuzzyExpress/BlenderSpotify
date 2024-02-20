import bpy, threading, time, subprocess

bl_info = {
    "name": "Blender Spotify",
    "author": "FuzzyExpress",
    "version": (0, 0, 1, 25),
    "description": """Automatically Pause or Play Spotify based on Blender Viewport Playback
    !! Requires playerctl to be installed !!""",
    "blender": (4, 1, 0),
    "category": "Interface",
}

PlayerName = 'spotify' # change this to what ever media player you prefer

global BlenderSpotifyMC
BlenderSpotifyMC = None

def PlayerPlaying(action = None):
    """
    Returns wether or not the player is playing audio.\n
    If provided with a Boolean, it will set playing instead.
    """

    if action == None:
        r = subprocess.run(f'playerctl -p {PlayerName} status', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()
    else:
        send = 'play' if action else 'pause';
        r = subprocess.run(f'playerctl -p {PlayerName} {send}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()


    if 'No players found' in r:
        raise Exception( f"{PlayerName} was not found by playerctl!:\nERROR: {r}" )
    elif 'playerctl: not found' in r:
        raise FileNotFoundError( f"playerctl was not found!:\nERROR: {r}\nPlease Install it!" )
    
    if action == None: return 'Playing' in r
    else: return not action 
    

class MusicController:
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Controller Start Stop | Modal Timer Operator"

    def __init__(self):
        self.Playing         = False
        self.SetPlaying      = False
        self.MusicWasPlaying = PlayerPlaying()
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
            if True: #// the sound in VSE check was here, but had to be moved due to it being called before regitration was complete
                LastPlaying = self.Playing
                self.Playing = self.SetPlaying > 0 #get play state(boolean) 
                self.SetPlaying -= 1;

                if LastPlaying != self.Playing: 
                    print('Blender Playing Changed:', self.Playing)
                    if self.Playing:
                        self.MusicWasPlaying = PlayerPlaying()
                        print('Was Playing:', self.MusicWasPlaying)
                        PlayerPlaying(False)

                    elif self.MusicWasPlaying:
                        PlayerPlaying(True)

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
