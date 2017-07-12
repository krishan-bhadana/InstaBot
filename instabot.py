import requests, urllib

APP_ACCESS_TOKEN = '1475677391.44be0c0.bbef974724754bf59a7e631532443173'
#Token Owner : k_b.96
#Sandbox Users : insta.mriu.test.3

BASE_URL = 'https://api.instagram.com/v1/'

'''
Function to get your own info
'''

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function to get the ID of a user by username
'''


def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


'''
Function declaration to get the info of a user by username
'''


def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get your recent post
'''


def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get the recent post of a user by username
'''


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


def thepost(username):
    id = get_user_id(username)
    request_url = (BASE_URL + "users/%s/media/recent?access_token=%s") % (id, APP_ACCESS_TOKEN)
    media = requests.get(request_url).json()
    if media:
        media_ID = media['data'][0]['id']
        media_link = media['data'][0]['link']
        media_type = media['data'][0]['type']
        media_likes = media['data'][0]['likes']['count']
        media_user_like = media['data'][0]['user_has_liked']
        print "Media ID : " + str(media_ID)
        print "Media Link : " + str(media_link)
        print "Media type : " + media_type
        print "Total likes : " + str(media_likes)
        print "Liked by you : " + str(media_user_like)
        return media


def like_unlikefunction(username):

    media = thepost(username)
    media_id= media['data'][0]['id']
    media_likes = media['data'][0]['likes']['count']
    option = int(raw_input('Select what do you want to do:\n'
                          '1. Like post.\n'
                          '2. Unlike post\n'))
    if option == 1:
        print "likes: %s" % (media_likes)
        request_url = (BASE_URL + 'media/%s/likes') % media_id
        payload = {"access_token": APP_ACCESS_TOKEN}
        post_a_like = requests.post(request_url, payload).json()
        if post_a_like['meta']['code'] == 200:
            print 'Successfully liked'
    if option==2:
        request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
        payload = {"access_token": APP_ACCESS_TOKEN}
        delete_a_like = requests.delete(request_url).json()
        if delete_a_like['meta']['code'] == 200:
            print 'Successfully Unliked'

def get_like_list(username):
    media = thepost(username)
    media_likes = media['data'][0]['likes']['count']
    id = media['data'][0]['id']
    request_url = (BASE_URL + "media/%s/likes?access_token=%s") % (id, APP_ACCESS_TOKEN)
    likers = requests.get(request_url).json()
    i = 0
    while i < media_likes:
        print '\n'+likers['data'][i]['username']
        i=i+1



def post_comment(username):

    #quest = int(raw_input('Select what do you want to do:\n'
                         #'1. Comment on recent media.\n2. Delete a negative comment.\n')
    media = thepost(username)
    media_id = media['data'][0]['id']
    comment = raw_input("Enter 'comment' you want to post")
    payload = {"access_token": APP_ACCESS_TOKEN, 'text': comment}
    request_url = (BASE_URL + 'media/%s/comments') % media_id
    post_comment = requests.post(request_url, payload).json()
    if post_comment['meta']['code'] == 200:
        print 'Successfully commented'
    else:
        print 'Unable to comment: Try again'


def insta_tasks(username):
    choice='Z'
    while choice != 'H':
        print "\n-----------------------------------------------------------\nA. Get details\n"
        print "B. Get recent post\n"
        print "C. Get a list of people who have liked the recent post\n"
        print "D. Like_unlike the recent post\n"
        print "E. Get a list of comments on the recent post\n"
        print "F. Make a comment on the recent post\n"
        print "G. Delete negative comments from the recent post\n"
        print "H. Exit"

        choice = raw_input("Enter you choice: ").upper()
        if choice == "A":
            if username == 'k_b.96':
                self_info()
            else:
                get_user_info(username)
        elif choice == "B":
            if username == 'k_b.96':
                get_own_post()
            else:
                get_user_post(username)
        elif choice == "C":
            get_like_list(username)
        elif choice == "D":
            like_unlikefunction(username)
        elif choice == "E":
            get_comment_list(username)
        elif choice == "F":
            post_comment(username)
        elif choice == "G":
            delete_negative_comment(username)
        elif choice == "H":
            exit()
        else:
            print "wrong choice"


def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!\tSelect an option'
        input = raw_input("1. Go to your own profile\n2. Go to another user's profile\n3.Exit instabot")
        if input == '1':
            username = 'k_b.96'
            insta_tasks(username)
        elif input == '2':
            username = raw_input('Enter username')
            insta_tasks(username)
        elif input == '3':
            exit()

start_bot()
