from sikuli import *

import tempfile
import time

if __name__ == '__main__':
    print "Do not run as __main__!  Intended for import only."
    exit()

REGION_PLAY                                         = Region(7,965,334,57)
REGION_MULLIGAN_KEEP                                = Region(0,13,175,154)
REGION_CARD_SENT_TO_BOTTOM                          = Region(1209,283,102,63)
REGION_TEMPORARY_ZONE                               = Region(1017,199,124,29)
REGION_PUT_ON_THE_BOTTOM_OF_YOUR_LIBRARY            = Region(921,181,459,166)
REGION_CHAT_PUT_A_CARD_ON_THE_BOTTOM_OF_THE_LIBRARY = Region(1501,671,398,51)
REGION_CARD_PREVIEW_CAPTURE                         = Region(1553,110,138,25)
REGION_CONCEDE_MATCH_BUTTON                         = Region(891,554,133,48)

LOCATION_PLAY                                       = Location(169, 995)
LOCATION_MULLIGAN                                   = Location(47, 141)
LOCATION_TEMPORARY_ZONE_CARD                        = Location(1195, 382)
LOCATION_PUT_ON_THE_BOTTOM_OF_YOUR_LIBRARY          = Location(1118, 430)
LOCATION_FIRST_CARD_IN_HAND                         = Location(282, 910)
LOCATION_X_CLOSE                                    = Location(1902, 16)
LOCATION_CONCEDE_MATCH                              = Location(961, 579)

AUTO_WAIT_TIMEOUT_SECONDS                           = 10

TEMP_DIR_PREFIX                                     = time.strftime("MTGO-scry-bug_%Y-%m-%d_%H-%M-%S", time.gmtime())
TEMP_PATH                                           = tempfile.mkdtemp(prefix=TEMP_DIR_PREFIX)
HITS_DIR                                            = 'hits'
MISSES_DIR                                          = 'misses'

print "Loaded", __name__
