class PostInfo:
    def __init__(self):
        self.group_id          = ""
        self.post_id           = ""
        self.post_owner_id     = ""
        self.post_images        = []
        '''
        the structure of comment:
        {
            comment_owner_id:       a string
            comment_content:        a string
            comment_tags:           a list of tagged users
            comment_replies: [
                {
                    reply_user: 
                    reply_comment:
                    reply_tag:
                }
            ]
        }
        '''


    def get_group_id(self):
        return self.group_id

    def get_post_id(self):
        return self.post_id

    def get_post_owner_id(self):
        return self.post_owner_id

    def get_post_images(self):
        return self.post_images


    def set_post_image(self, post_images):
        self.post_images = post_images

    def set_group_id(self, group_id):
        self.group_id = group_id

    def set_post_id(self, post_id):
        self.post_id = post_id

    def set_post_owner_id(self, post_owner_id):
        self.post_owner_id = post_owner_id
