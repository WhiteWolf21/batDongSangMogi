class PostInfo:
    def __init__(self):
        self._info = {
            "group":                            None,
            "link":                             None,
            "title":                            None,
            "post_id":                          None,
            "message":                          None,
            "post_date":                        None,
            "crawled_date":                     None,
            "score":                            None,
            "post_owner_id":                    None,
            "post_comment_num":                 0,
            "post_reaction_num":                0,
            "post_share_num":                   0,
            "attr_addr_number":                 None,
            "attr_addr_street":                 None,
            "attr_addr_district":               None,
            "attr_addr_ward":                   None,
            "attr_addr_city":                   None,
            "attr_position":                    None,
            "attr_surrounding":                 None,
            "attr_surrounding_name":            None,
            "attr_surrounding_characteristics": None,
            "attr_transaction_type":            None,
            "attr_realestate_type":             None,
            "attr_potential":                   None,
            "attr_area":                        None,
            "attr_price":                       None,
            "attr_price_min":                   None,
            "attr_price_max":                   None,
            "attr_price_m2" :                   None,
            "attr_interior_floor":              None,
            "attr_interior_room":               None,
            "attr_orientation":                 None,
            "attr_project":                     None,
            "attr_legal":                       None,
            'location_lng':                     None,
            'location_lat':                     None,
            "source":                           "system",
            "post_comments":                    [],
            

            'address':                          None,
            'city':                             None,
            'bedroom':                          None,
            'bathroom':                         None,
        }


        

    def get_info(self, attribute):
        return self._info[attribute]

    def set_info(self, attribute, value):
        self._info[attribute] = value

    def get_info_for_pushing(self):
        '''Get an info to push to Database
        :Return:
         - an tmp
         - None: if this post is not informative (too few attributes have value)
        '''
        tmp = self._info.copy()

        tmp['attr_surrounding']                 = str(tmp["attr_surrounding"])
        tmp['attr_surrounding_name']            = str(tmp["attr_surrounding_name"])
        tmp['attr_surrounding_characteristics'] = str(tmp["attr_surrounding_characteristics"])

        if tmp['location_lng'] is not None:            
            tmp['location'] = {
                "type" : "Point",
                "coordinates" : [tmp['location_lng'], tmp['location_lat']]
            }
        else:
            tmp['location'] = {
                "type" : "Point",
                "coordinates" : [0 , 0]
            }
        
        for x in ['address', 'city', 'bedroom', 'bathroom', 'post_comment_num', 'post_reaction_num', 'post_share_num']:
            del tmp[x]

        # check if this post is informative or not
        n_item_none = 0
        for key, value in self._info.items():
            if value is None or value == "":
                n_item_none += 1

        if n_item_none > 22:
            return None
        else:
            return tmp



    def get_post_comments(self):
        return self._info['post_comments']

    def add_comment(self, comment_owner_id, comment_content, comment_tags, comment_replies):
        self._info['post_comments'].append({
            'comment_owner_id': comment_owner_id,
            'comment_content' : comment_content,
            'comment_tags'    : comment_tags,
            'comment_replies' : comment_replies
        })