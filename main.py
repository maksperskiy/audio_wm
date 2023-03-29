import numpy as np
import os
import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

Gst.init(None)

pipeline = Gst.Pipeline.new("audio_extractor")
bus = pipeline.get_bus()

# msg = bus.timed_pop_filtered(
#     Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS
# )
filesrc = Gst.ElementFactory.make("filesrc", "filesrc")
filesrc.set_property("location", "video.mp4")

decode = Gst.ElementFactory.make("decodebin", "decode")
convert = Gst.ElementFactory.make("audioconvert", "convert")
resample = Gst.ElementFactory.make("audioresample", "resample")
sink = Gst.ElementFactory.make("autoaudiosink", "sink")

pipeline.add(filesrc)
pipeline.add(decode)
pipeline.add(convert)
pipeline.add(resample) 
pipeline.add(sink)

filesrc.link(decode)

def on_pad_added(element, pad):
    # pad.link(sink_pad)
    print("Pad added")
    print("Pad name:", pad.get_name())
    print("Pad type:", pad.query_caps(None).to_string())
    print("Pad direction:", pad.get_direction())
    print("Pad template:", pad.get_pad_template())
    print("Pad message type:", pad.get_property("message-type"))

decode.connect("pad-added", on_pad_added, convert)
convert.link(resample)
resample.link(sink)
pipeline.set_state(Gst.State.PLAYING)
# pipeline.get_state(Gst.CLOCK_TIME_NONE)
pipeline.set_state(Gst.State.NULL)







