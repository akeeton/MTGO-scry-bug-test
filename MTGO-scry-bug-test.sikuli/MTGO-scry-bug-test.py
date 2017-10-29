import hashlib
import json
import os
import shutil
import tempfile
import time

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

TEMP_DIR_PREFIX   = time.strftime("MTGO-scry-bug_%Y-%m-%d_%H-%M-%S", time.gmtime())
TEMP_PATH         = tempfile.mkdtemp(prefix=TEMP_DIR_PREFIX)
HITS_DIR          = 'hits'
MISSES_DIR        = 'misses'

attempts = 0

def main():
    global attempts
    attempts += 1

    HITS_PATH         = os.path.join(get_number_of_attempts_path(attempts), HITS_DIR)
    MISSES_PATH       = os.path.join(get_number_of_attempts_path(attempts), MISSES_DIR)

    print "TEMP_PATH:",                             TEMP_PATH
    print "get_number_of_attempts_path(attempts):", get_number_of_attempts_path(attempts)
    print "HITS_PATH:",                             HITS_PATH
    print "MISSES_PATH:",                           MISSES_PATH

    print get_number_of_attempts_path(attempts)
    os.mkdir(get_number_of_attempts_path(attempts))
    os.mkdir(HITS_PATH)
    os.mkdir(MISSES_PATH)

    Settings.AutoWaitTimeout = AUTO_WAIT_TIMEOUT_SECONDS

    iterations = 0
    hits       = 0
    card_hash_to_times_card_sent_to_bottom           = ZeroValueDict({'name': 'card_hash_to_times_card_sent_to_bottom'})
    card_hash_to_times_card_sent_to_bottom_and_drawn = ZeroValueDict({'name': 'card_hash_to_times_card_sent_to_bottom_and_drawn'})
    card_hash_to_times_card_drawn                    = ZeroValueDict({'name': 'card_hash_to_times_card_drawn'})
    card_hash_to_capture                             = {'name': 'card_hash_to_capture'}

    while True:
        REGION_PLAY.wait("play.png")
        time.sleep(0.5)
        REGION_PLAY.click(LOCATION_PLAY)

        time.sleep(0.5)

        REGION_MULLIGAN_KEEP.wait("mulligan_keep.png")
        for i in range(0, 7):
            REGION_MULLIGAN_KEEP.wait("mulligan_highlighted_keep.png")
            time.sleep(1.0)
            REGION_MULLIGAN_KEEP.click(LOCATION_MULLIGAN)

        REGION_TEMPORARY_ZONE.wait("temporary_zone.png")
        time.sleep(0.1)
        click(LOCATION_TEMPORARY_ZONE_CARD)
        time.sleep(0.5)

        REGION_PUT_ON_THE_BOTTOM_OF_YOUR_LIBRARY.click(LOCATION_PUT_ON_THE_BOTTOM_OF_YOUR_LIBRARY)

        REGION_CHAT_PUT_A_CARD_ON_THE_BOTTOM_OF_THE_LIBRARY.wait("chat_put_a_card_on_the_bottom_of_the_library.png")
        time.sleep(0.1)

        card_sent_to_bottom_capture = capture(REGION_CARD_PREVIEW_CAPTURE)
        hover(LOCATION_FIRST_CARD_IN_HAND) # Update the preview with the drawn card.
        time.sleep(0.5)
        card_drawn_capture = capture(REGION_CARD_PREVIEW_CAPTURE)

        copy_path = ""

        card_sent_to_bottom_hash = hash_file(card_sent_to_bottom_capture)
        card_drawn_hash          = hash_file(card_drawn_capture)

        bottom_and_top_the_same = False
        if card_sent_to_bottom_hash == card_drawn_hash:
            hits += 1
            bottom_and_top_the_same = True
            copy_path = HITS_PATH
        else:
            copy_path = MISSES_PATH

        iterations += 1
        print hits, "/", iterations

        card_sent_to_bottom_capture_dest_path = os.path.join(copy_path, str(iterations) + "_bottom.png")
        card_drawn_capture_dest_path          = os.path.join(copy_path, str(iterations) + "_drawn.png")

        shutil.move(card_sent_to_bottom_capture, card_sent_to_bottom_capture_dest_path)
        shutil.move(card_drawn_capture, card_drawn_capture_dest_path)

        card_hash_to_times_card_sent_to_bottom[card_sent_to_bottom_hash]           += 1
        card_hash_to_times_card_sent_to_bottom_and_drawn[card_sent_to_bottom_hash] += 1
        card_hash_to_times_card_drawn[card_drawn_hash]                             += 1
        card_hash_to_capture[card_sent_to_bottom_hash] = card_sent_to_bottom_capture_dest_path
        card_hash_to_capture[card_drawn_hash]          = card_drawn_capture_dest_path

        print "hashes of captures of cards that were sent to the bottom and how many times that happened:", card_hash_to_times_card_sent_to_bottom
        print
        print "hashes of captures of cards that were drawn after scrying and how many times that happened:", card_hash_to_times_card_drawn
        print
        print card_hash_to_capture

        with open(os.path.join(ATTEMPT_NO_PATH, 'stats.json'), 'w') as stats_file:
            print json.dump(card_hash_to_times_card_sent_to_bottom_and_drawn[card_sent_to_bottom_hash], stats_file)
            print
            print json.dump(card_hash_to_times_card_sent_to_bottom, stats_file)
            print
            print json.dump(card_hash_to_times_card_drawn, stats_file)
            print
            print json.dump(card_hash_to_capture, stats_file)
            print
            print hits, '/', iterations

        click(LOCATION_X_CLOSE)

        REGION_CONCEDE_MATCH_BUTTON.wait("concede_match.png")
        time.sleep(0.1)
        type('\n')

class ZeroValueDict(dict):
    def __missing__(self, key):
        return 0

def hash_file(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as opened_file:
        buf = opened_file.read()
        hasher.update(buf)

    return hasher.hexdigest()

def get_number_of_attempts_path(attempts):
    return os.path.join(TEMP_PATH, 'attempt_{0}'.format(attempts))

if __name__ == '__main__':
    try:
        main()
    except FindFailed as e:
        print e
        with open(os.path.join(get_number_of_attempts_path(attempts), 'error.log'), 'w') as errorlog:
            errorlog.write(str(e))
