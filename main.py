#!/usr/bin/env python3

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

class RTSPServer(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        super(RTSPServer, self).__init__()
        self.launch_string = (
            'libcamerasrc ! video/x-raw,width=1280,height=720,framerate=30/1 ! '
            'videoconvert ! x264enc ! '
            'rtph264pay name=pay0 pt=96'
        )
        
    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

def main():
    Gst.init(None)
    server = GstRtspServer.RTSPServer()
    
    factory = RTSPServer()
    factory.set_shared(True)

    mount_points = server.get_mount_points()
    mount_points.add_factory("/camera_preview", factory)

    server.attach(None)

    loop = GObject.MainLoop()
    loop.run()

if __name__ == '__main__':
    main()