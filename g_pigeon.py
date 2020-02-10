# g_pigeon.py
# Pigeon graphics

import upygame

bird00Pixels = b'\
\x00\x00\x00\
\x00\x11\x00\
\x00\x11\x00\
\x01\x11\x10\
\x01\x11\x10\
\x01\x11\x10\
'
bird00 = upygame.surface.Surface(6, 6, bird00Pixels)

bird01Pixels = b'\
\x00\x00\x00\
\x00\x11\x00\
\x01\x11\x10\
\x11\x11\x11\
\x10\x11\x01\
\x00\x11\x00\
'
bird01 = upygame.surface.Surface(6, 6, bird01Pixels)
bird02Pixels = b'\
\x00\x00\x00\
\x00\x11\x00\
\x01\x11\x10\
\x11\x11\x11\
\x00\x11\x00\
\x00\x11\x00\
'
bird02 = upygame.surface.Surface(6, 6, bird02Pixels)
bird03Pixels = b'\
\x00\x00\x00\
\x10\x11\x01\
\x11\x11\x11\
\x01\x11\x10\
\x00\x11\x00\
\x00\x11\x00\
'
bird03 = upygame.surface.Surface(6, 6, bird03Pixels)
bird04Pixels = b'\
\x00\x00\x00\
\x00\x11\x00\
\x11\x11\x11\
\x01\x11\x10\
\x00\x11\x00\
\x00\x11\x00\
'
bird04 = upygame.surface.Surface(6, 6, bird04Pixels)
