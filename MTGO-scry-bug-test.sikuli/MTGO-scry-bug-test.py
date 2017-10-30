# Make your image, region, and location changes then change the from-import
# to match.
from configurables_akeeton_laptop import *

import hashlib
import java.awt.Toolkit
import json
import os
import shutil
import time

Settings.ActionLogs      = True
Settings.InfoLogs        = True
Settings.DebugLogs       = True
Settings.LogTime         = True
Settings.AutoWaitTimeout = AUTO_WAIT_TIMEOUT_SECONDS

TEMP_DIR_PREFIX = time.strftime("MTGO-scry-bug_%Y-%m-%d_%H-%M-%S", time.gmtime())
TEMP_PATH       = tempfile.mkdtemp(prefix=TEMP_DIR_PREFIX)

attempts = 0

def main():
    global attempts
    attempts += 1

    ATTEMPT_NUM_PATH = get_attempt_number_path(attempts)
    HITS_PATH        = os.path.join(ATTEMPT_NUM_PATH, HITS_DIR)
    MISSES_PATH      = os.path.join(ATTEMPT_NUM_PATH, MISSES_DIR)

    print "TEMP_PATH:",       TEMP_PATH
    print "ATTEMPT_NUM_PATH", ATTEMPT_NUM_PATH
    print "HITS_PATH:",       HITS_PATH
    print "MISSES_PATH:",     MISSES_PATH

    os.mkdir(ATTEMPT_NUM_PATH)
    os.mkdir(HITS_PATH)
    os.mkdir(MISSES_PATH)

    iterations = 0
    hits       = 0
    card_hash_to_times_card_sent_to_bottom           = ['card_hash_to_times_card_sent_to_bottom', ZeroValueDict()]
    card_hash_to_times_card_sent_to_bottom_and_drawn = ['card_hash_to_times_card_sent_to_bottom_and_drawn', ZeroValueDict()]
    card_hash_to_times_card_drawn                    = ['card_hash_to_times_card_drawn', ZeroValueDict()]
    card_hash_to_capture                             = ['card_hash_to_capture', {}]

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

        card_hash_to_times_card_sent_to_bottom[1][card_sent_to_bottom_hash]           += 1
        card_hash_to_times_card_drawn[1][card_drawn_hash]                             += 1

        if card_sent_to_bottom_hash == card_drawn_hash:
            hits += 1
            card_hash_to_times_card_sent_to_bottom_and_drawn[1][card_sent_to_bottom_hash] += 1
            copy_path = HITS_PATH
        else:
            copy_path = MISSES_PATH

        iterations += 1
        print "{0}/{1}".format(hits, iterations)

        card_sent_to_bottom_capture_dest_path = os.path.join(copy_path, str(iterations) + "_bottom.png")
        card_drawn_capture_dest_path          = os.path.join(copy_path, str(iterations) + "_drawn.png")

        shutil.move(card_sent_to_bottom_capture, card_sent_to_bottom_capture_dest_path)
        shutil.move(card_drawn_capture, card_drawn_capture_dest_path)

        card_hash_to_capture[1][card_sent_to_bottom_hash] = card_sent_to_bottom_capture_dest_path
        card_hash_to_capture[1][card_drawn_hash]          = card_drawn_capture_dest_path

        with open(os.path.join(ATTEMPT_NUM_PATH, 'stats.json'), 'w') as stats_file:
            json.dump(card_hash_to_times_card_sent_to_bottom_and_drawn, stats_file, sort_keys=True, indent=4)
            stats_file.write('\n')
            json.dump(card_hash_to_times_card_sent_to_bottom, stats_file, sort_keys=True, indent=4)
            stats_file.write('\n')
            json.dump(card_hash_to_times_card_drawn, stats_file, sort_keys=True, indent=4)
            stats_file.write('\n')
            json.dump(card_hash_to_capture, stats_file, sort_keys=True, indent=4)
            stats_file.write('\n')
            stats_file.write('{0}/{1}'.format(hits, iterations))

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

def get_attempt_number_path(attempts):
    return os.path.join(TEMP_PATH, 'attempt_{0}'.format(attempts))

if __name__ == '__main__':
    while True:
        try:
            main()
        except FindFailed as e:
            for i in range(0, TIMES_TO_BEEP_ON_FIND_FAIlED):
                java.awt.Toolkit.getDefaultToolkit().beep()
                time.sleep(1.0)

            print e
            with open(os.path.join(get_attempt_number_path(attempts), 'error.log'), 'w') as errorlog:
                errorlog.write(str(e))
            raise e # Replace this with a way to reset MTGO to a starting state so we can try again.
