import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst, GObject
import numpy as np

Gst.init(None)

pipeline = Gst.Pipeline()

filesrc = Gst.ElementFactory.make("filesrc", "filesrc")
filesrc.set_property("location", "video.mp4")

decodebin = Gst.ElementFactory.make("decodebin", "decodebin")

audioconvert = Gst.ElementFactory.make("audioconvert", "audioconvert")

audioresample = Gst.ElementFactory.make("audioresample", "audioresample")

appsink = Gst.ElementFactory.make("appsink", "appsink")
appsink.set_property("emit-signals", True)
appsink.set_property("max-buffers", 1)
appsink.set_property("drop", True)

pipeline.add(filesrc)
pipeline.add(decodebin)
pipeline.add(audioconvert)
pipeline.add(audioresample)
pipeline.add(appsink)

filesrc.link(decodebin)
decodebin.connect(
    "pad-added", lambda dbin, pad: pad.link(audioconvert.get_static_pad("sink"))
)
audioconvert.link(audioresample)
audioresample.link(appsink)

pipeline.set_state(Gst.State.PLAYING)

data = None
while True:
    sample = appsink.emit("pull-sample")
    if sample:
        buf = sample.get_buffer()
        caps = sample.get_caps()
        if caps.get_structure(0).get_name() == "audio/x-raw":
            arr = np.ndarray(
                (caps.get_structure(0).get_value("channels"), -1),
                buffer=buf.extract_dup(0, buf.get_size()),
                dtype=np.float32,
            )
            data = arr.T
            break

pipeline.set_state(Gst.State.NULL)




