from sikuli import *

import tempfile

if __name__ == '__main__':
    print "Do not run as __main__!  Intended for import only."
    exit()

REGION_PLAY                                         = Region(88,791,154,48)
REGION_MULLIGAN_KEEP                                = Region(14,110,121,50)
REGION_TEMPORARY_ZONE                               = Region(875,252,175,44)
REGION_PUT_ON_THE_BOTTOM_OF_YOUR_LIBRARY            = Region(1066,471,223,30)
REGION_CHAT_PUT_A_CARD_ON_THE_BOTTOM_OF_THE_LIBRARY = Region(1255,523,313,61)
REGION_CARD_PREVIEW_CAPTURE                         = Region(1317,82,92,21)
REGION_CONCEDE_MATCH_BUTTON                         = Region(739,469,127,42)

LOCATION_PLAY                                       = Location(167, 814)
LOCATION_MULLIGAN                                   = Location(45, 140)
LOCATION_TEMPORARY_ZONE_CARD                        = Location(1067, 445)
LOCATION_PUT_ON_THE_BOTTOM_OF_YOUR_LIBRARY          = Location(1164, 486)
LOCATION_FIRST_CARD_IN_HAND                         = Location(341, 746)
LOCATION_X_CLOSE                                    = Location(1581, 14)
LOCATION_CONCEDE_MATCH                              = Location(793, 488)

AUTO_WAIT_TIMEOUT_SECONDS                           = 10
TIMES_TO_BEEP_ON_FIND_FAIlED                        = 5

HITS_DIR                                            = 'hits'
MISSES_DIR                                          = 'misses'

print "Loaded", __name__
