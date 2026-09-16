# -*- coding: utf-8 -*-
"""PyS60 Sound contract using independent pygame buffers and one active player."""
import numbers
import os
import subprocess
import sys
import e32

ENotReady, EOpen, EPlaying, ERecording = 0, 1, 2, 3
KMdaRepeatForever = -1
TTS_PREFIX = '(tts)'
_active = None


def _mixer():
    try:
        import pygame
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
        return pygame.mixer
    except (ImportError, RuntimeError) as exc:
        raise e32.SymbianError(-5, str(exc))


class Sound(object):
    def __init__(self):
        self._state = ENotReady
        self._sound = None
        self._channel = None
        self._timer = e32.Ao_timer()
        self._position = 0
        self._volume = 100
        self._callback = None
        self._started = None

    @staticmethod
    def open(filename):
        player = Sound()
        mixer = _mixer()
        try:
            player._sound = mixer.Sound(filename)
        except Exception as exc:
            raise e32.SymbianError(-1 if not os.path.exists(filename) else -5, str(exc))
        player._state = EOpen
        return player

    def _require_open(self):
        if self._state != EOpen:
            raise RuntimeError('Sound not in correct state, state: %d' % self._state)

    def play(self, times=1, interval=0, callback=None):
        global _active
        self._require_open()
        if not isinstance(times, numbers.Integral) or not isinstance(interval, numbers.Integral):
            raise TypeError('times and interval must be integers')
        if times != KMdaRepeatForever and times < 1 or interval < 0:
            raise ValueError('invalid repetition count or interval')
        if callback is not None and not callable(callback):
            raise TypeError('callback must be callable')
        if _active is not None and _active is not self:
            _active.stop()
        self._callback, self._remaining, self._interval = callback, times, interval
        self._start_segment()
        self._state = EPlaying
        _active = self
        if callback is not None:
            callback(EOpen, EPlaying, 0)

    def _start_segment(self):
        mixer = _mixer()
        segment = self._sound
        if self._position:
            frequency, sample_format, channels = mixer.get_init()
            frame_size = abs(sample_format)//8 * channels
            frame = int(self._position*frequency/1000000.0)
            raw = self._sound.get_raw()[frame*frame_size:]
            if not raw:
                raw = b'\x00' * frame_size
            segment = mixer.Sound(buffer=raw)
        segment.set_volume(1.0)
        self._channel = mixer.find_channel(True)
        self._channel.set_volume(self._volume/100.0)
        self._channel.play(segment)
        self._segment = segment
        self._started = e32._clock()
        self._timer.after(.01, self._poll)

    def _poll(self):
        global _active
        if self._state != EPlaying:
            return
        if self._channel.get_busy():
            self._timer.after(.01, self._poll)
            return
        if self._remaining == KMdaRepeatForever or self._remaining > 1:
            if self._remaining != KMdaRepeatForever:
                self._remaining -= 1
            self._position = 0
            self._started = None
            self._timer.after(self._interval/1000000.0, self._start_segment)
        else:
            self._position = 0
            self._started = None
            self._state = EOpen
            if _active is self:
                _active = None
            if self._callback is not None:
                self._callback(EPlaying, EOpen, 0)

    def stop(self):
        global _active
        if self._state in (EPlaying, ERecording):
            self._position = self.current_position()
            if self._channel is not None:
                self._channel.stop()
            self._timer.cancel()
            self._started = None
            self._state = EOpen
        if _active is self:
            _active = None

    def close(self):
        self.stop()
        self._sound = None
        self._state = ENotReady
        self._position = 0

    def record(self):
        self._require_open()
        raise e32.SymbianError(-5, 'The pygame backend does not support recording')

    def state(self):
        return self._state

    def max_volume(self):
        return 100

    def set_volume(self, volume):
        if not isinstance(volume, numbers.Integral):
            raise TypeError('integer expected')
        self._volume = max(0, min(self.max_volume(), volume))
        if self._sound is not None:
            self._sound.set_volume(1.0)
        if self._channel is not None:
            self._channel.set_volume(self._volume/100.0)

    def current_volume(self):
        return self._volume

    def duration(self):
        return int(round(self._sound.get_length()*1000000)) if self._sound is not None else 0

    def set_position(self, position):
        if not isinstance(position, numbers.Integral):
            raise TypeError('integer expected')
        self._position = max(0, min(self.duration(), position))
        if self._state == EPlaying:
            self._channel.stop()
            self._timer.cancel()
            self._start_segment()

    def current_position(self):
        if self._state == EPlaying and self._started is not None:
            return min(self.duration(), self._position+int((e32._clock()-self._started)*1000000))
        return self._position

    @staticmethod
    def _say(text):
        return say(text[len(TTS_PREFIX):] if text.startswith(TTS_PREFIX) else text)


def say(text, prefix=TTS_PREFIX):
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    if sys.platform != 'darwin':
        raise e32.SymbianError(-5, 'No text-to-speech backend configured for this platform')
    # Send text via stdin so leading '-' is never interpreted as a CLI option.
    process = subprocess.Popen(['say'], stdin=subprocess.PIPE)
    process.communicate(text.encode('utf-8'))
    if process.returncode:
        raise e32.SymbianError(-2, 'Text-to-speech failed')
