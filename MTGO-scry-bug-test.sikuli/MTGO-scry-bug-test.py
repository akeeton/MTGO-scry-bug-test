import os
import shutil
import tempfile
import time

REGION_PLAY                              = Region(7,965,334,57)
REGION_MULLIGAN_KEEP                     = Region(0,13,175,154)
REGION_TEMPORARY_ZONE                    = Region(1150,195,130,37)
REGION_PUT_ON_THE_BOTTOM_OF_YOUR_LIBRARY = Region(921,181,459,166)
REGION_ON_THE_BOTTOM_OF_THE_LIBRARY      = Region(1726,664,180,37)
REGION_CONCEDE_MATCH_BUTTON              = Region(891,554,133,48)

TEMP_DIR_PREFIX = time.strftime("MTGO-scry-bug_%Y-%m-%d_%H-%M-%S", time.gmtime())
TEMP_PATH = tempfile.mkdtemp(prefix=TEMP_DIR_PREFIX)
print "TEMP_PATH:", TEMP_PATH

OUTPUT_PATH = os.path.join(TEMP_PATH, 'output')
print "OUTPUT_PATH:", OUTPUT_PATH

HITS_DIR = 'hits'
HITS_PATH = os.path.join(OUTPUT_PATH, HITS_DIR)
print "HITS_PATH:", HITS_PATH

MISSES_DIR = 'misses'
MISSES_PATH = os.path.join(OUTPUT_PATH, MISSES_DIR)
print "MISSES_PATH:", MISSES_PATH

os.mkdir(OUTPUT_PATH)
os.mkdir(HITS_PATH)
os.mkdir(MISSES_PATH)

iterations = 0
hits = 0

while True:
    REGION_PLAY.wait("play.png", 5)
    REGION_PLAY.click(Location(164, 993))

    REGION_MULLIGAN_KEEP.wait("mulligan_keep.png", 5)
    for i in range(0, 7):
        REGION_MULLIGAN_KEEP.wait("mulligan_highlighted_keep.png", 5)
        time.sleep(0.5)
        REGION_MULLIGAN_KEEP.click(Location(47, 142))

    REGION_TEMPORARY_ZONE.wait("temporary_zone.png", 5)
    time.sleep(0.1)
    card_sent_to_bottom = capture(Region(1209,283,102,63))

    click(Location(1242, 379)) # Click on the top card of the library.

    time.sleep(0.5)
    REGION_PUT_ON_THE_BOTTOM_OF_YOUR_LIBRARY.click(Location(1139, 424)) # Click on "Put on the bottom of your library."

    REGION_ON_THE_BOTTOM_OF_THE_LIBRARY.wait("card_on_the_bottom_of_the_library.png", 5)
    time.sleep(0.5)

    card_drawn_region = Region(Region(203,780,155,115))
    card_drawn = capture(card_drawn_region)

    copy_path = ""

    if card_drawn_region.exists(card_sent_to_bottom):
        hits += 1
        copy_path = HITS_PATH
    else:
        copy_path = MISSES_PATH

    iterations += 1
    print hits, "/", iterations

    shutil.move(card_sent_to_bottom, os.path.join(copy_path, str(iterations) + "_bottom.png"))
    shutil.move(card_drawn, os.path.join(copy_path, str(iterations) + "_drawn.png"))

    click(Location(1903, 13)) # Click on the "X" (close) button.

    region_concede_match_button.wait("concede_match.png", 5)
    time.sleep(0.5)
    region_concede_match_button.click("concede_match.png")
