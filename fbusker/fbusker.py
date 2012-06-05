import sys
import time
import os
import urllib2
import fbconsole

class FBusker(object):

    def __init__(self, user_id, destination=None):
        if destination is None:
            destination = os.getcwd()
        elif (destination[-1] != '/'):
            destination += '/'
        self.target = user_id
        self.destination = destination

    def run(self):
        fbconsole.AUTH_SCOPE = ['user_photos', 'friends_photos', 'user_videos']
        fbconsole.authenticate()

        try:
            print "Getting mutual friends"
            mutual_friends = fbconsole.get('/me/mutualfriends/%s' % \
                self.target)
            friendlist = "(%s)" % ','.join(
                ["'%s'" % user['id'] for user in mutual_friends['data']]
            )
            time.sleep(1)
            print "Getting albums"
            albums = fbconsole.fql("""
                SELECT aid, name, owner FROM album WHERE owner IN %s
                """ % friendlist)
            for album in albums:
                time.sleep(1)
                sys.stdout.write('.')
                sys.stdout.flush()
                photos = fbconsole.fql("""
                    SELECT src_big, link, caption, images, pid, created
                    FROM photo 
                    WHERE pid IN (
                        SELECT pid 
                        FROM photo_tag 
                        WHERE pid IN (
                            SELECT pid 
                            FROM photo 
                            WHERE aid = '%s'
                        )
                        AND subject = '%s'
                    )
                    """ % (album['aid'], self.target)
                    )
                if len(photos) > 0:
                    print "\nIn: '%s' by %d:" % (album['name'], album['owner'])
                    for photo in photos:
                        biggest_image = 0
                        biggest_dim = 0
                        for i, image in enumerate(photo['images']):
                            if biggest_dim < image['height']:
                                biggest_dim = image['height']
                                biggest_image = i
                        image_url = photo['images'][biggest_image]['source']
                        file_part = image_url.split('/')[-1]
                        file_path = "%s/%s" % (self.destination, "%s_%s_%s" % \
                            (album['owner'], album['aid'], file_part))                            
                        print "Retrieving %s" % image_url
                        try:
                            # Grab the photo.
                            response = urllib2.urlopen(image_url)
                            image_data = response.read()
                            newfile = open(file_path, 'w')
                            newfile.write(image_data)
                            newfile.flush()
                            newfile.close()
                            # Set file modification/creation time to the original 
                            # upload date.
                            if photo['created'] > 666666:
                                print "creation date is %d" % photo['created']
                                os.utime(file_path, 
                                    (photo['created'], photo['created']))
                        except urllib2.HTTPError as (e):
                            print "Error received during image grab: %s" % e.read()
        except urllib2.HTTPError as (e):
            print e.read()
            exit(1)            


def main():
    """
        fbusker.py
        AUTHOR: magnate/r82x
        USAGE: python fbusker.py facebookuserid (destinationpath)

        Facebook hides photo tags from you while searching plainly for them --
        So you have to grab the albums of your mutual friends and then search
        for tags within.

        This automates this via the API. Filenames are saved in the format 
        userid_albumid_sourcefile in a directory specified by the second
        argument, the first being the user ID of the user you are targeting.
        If the destination path is not provided, the files will be saved in the
        current directory.
    """
    if len(sys.argv) < 2:
        print "Requires a UID of a facebook user to find in photos"
        exit(1)

    target = sys.argv[1]
    if len(sys.argv) >= 3:
        # provided a directory
        destination = sys.argv[2]
        if destination[-1] != '/':
            destination += '/'
    else:
        destination = os.getcwd()

    fbusker = FBusker(target, destination)
    fbusker.run()

if __name__ == "__main__":
    main()        