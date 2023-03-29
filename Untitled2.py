#!/usr/bin/env python
# coding: utf-8


import numpy as np
import matplotlib.pyplot as plt
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')

from gi.repository import GLib, Gst



def bus_call(bus, message, loop, pipe):
    t = message.type
    if t == Gst.MessageType.EOS:
        pipe.set_state(Gst.State.NULL)
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f'{err}: {debug}')
        pipe.set_state(Gst.State.NULL)
        loop.quit()
    return Gst.FlowReturn.OK



i = 0
sample = None



sample



def handle_sample(sink):
    global i
    sample = sink.emit('pull-sample')
    buffer = sample.get_buffer()
    
    success, map_info = buffer.map(Gst.MapFlags.READ)
    
    if not success:
        raise RuntimeError("Could not map buffer data!")
    
    if i == 0:
        sample = map_info.data
        i += 1
    
    arr = np.ndarray((buffer.get_size(), 1), buffer=buffer.extract_dup(0, buffer.get_size()), dtype=np.int8)
    
    data_list.append(arr)
    buffer.unmap(map_info)
    return Gst.FlowReturn.OK



def pipe_init(source, on_new_sample):
    Gst.init(None)
    pipe = Gst.Pipeline.new('dynamic')

    src = Gst.ElementFactory.make('filesrc')
    # demux = Gst.ElementFactory.make('qtdemux')
    decode = Gst.ElementFactory.make('decodebin')
    convert = Gst.ElementFactory.make('audioconvert')
    encode = Gst.ElementFactory.make("wavenc")
    sink = Gst.ElementFactory.make('appsink')

    for item in (
        src, 
        # demux,
        decode, 
        convert, 
        encode, 
        sink
    ):
        pipe.add(item)

    src.link(decode)
    # demux.link(decode)
    decode.connect('pad-added', lambda el, pad: pad.link(convert.get_static_pad('sink')))

    convert.link(encode)
    encode.link(sink)
    
    
    src.set_property('location', source)

    sink.set_property("emit-signals", True)
    sink.set_property("max-buffers", 1)
    sink.set_property("drop", True)
    sink.set_property("wait-on-eos", True)
    sink.set_property('sync', False)

    sink.connect("new-sample", on_new_sample)
    
    return pipe



def run(source, sink_callback):
    loop = GLib.MainLoop()
    pipe = pipe_init(source, sink_callback)

    bus = pipe.get_bus()
    bus.add_signal_watch()
    bus.enable_sync_message_emission()
    bus.connect('message', bus_call, loop, pipe)

    pipe.set_state(Gst.State.PLAYING)
    loop.run()



data_list = []



run('video.mp4', handle_sample)



data = [item[0] for sublist in data_list for item in sublist]



len(data)



time = np.linspace(
    0,
    len(data) / 44100,
    num = len(data)
)

plt.figure(1, figsize=(24, 2))

plt.title("Sound Wave")
plt.xlabel("Time")

plt.plot(time, data)

plt.show()









from scipy.io.wavfile import write
# 32767
rate = 44100*8
scaled = np.int16(data / np.max(np.abs(data)) * 32767)
write('test.wav', rate, scaled)







