from miscellaneous.regex_operation import get_postid

old_id = set(open('../old_id.txt', 'r').readlines())


def post_matching(post_data):
    """
        Check whether the id of post is matched with the crawled ones
    :param post_data: instance of class PostInfo
    :return: False: if the id not matched
             True: otherwise
    """

    post_id = get_postid(post_data['post_id'])

    if post_id is None:
        return True

    if post_id in old_id:
        return True
    else:
        return False
