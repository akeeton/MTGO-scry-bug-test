import os
import shutil
import tempfile
import time

region_play = Region(7,965,334,57)
region_mulligan_keep = Region(0,13,175,154)
region_temporary_zone = Region(1150,195,130,37)
region_put_on_the_bottom_of_your_library = Region(921,181,459,166)
region_on_the_bottom_of_the_library = Region(1726,664,180,37)
region_concede_match_button = Region(891,554,133,48)

TEMP_PATH = tempfile.mkdtemp()
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
    region_play.wait("1508227924297.png", 5)
    region_play.click("1508227924297.png")
    
    for i in range(0, 7):
        region_mulligan_keep.wait("1508227031905.png", 5)
        region_mulligan_keep.click("1508228072640.png")
        time.sleep(0.2)
    
    region_temporary_zone.wait("1508222653397.png", 5)
    
    card_sent_to_bottom = capture(Region(1202,271,118,159))
    
    click(Location(1207, 271))
    
    region_put_on_the_bottom_of_your_library.click("scry-to-bottom.png")

    region_on_the_bottom_of_the_library.wait("1508225941575.png", 5)

    time.sleep(0.2)
    
    card_drawn_region = Region(Region(169,735,224,299))

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

    click(Location(1903, 13))

    region_concede_match_button.wait("1508227869176.png", 5)
    region_concede_match_button.click("1508227869176.png")
    