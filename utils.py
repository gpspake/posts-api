import json


def get_tags_from_string(tags_string):
    """
    takes a json string of single and grouped tag names and returns a dict
    with a flattened list of single tags and a list of grouped tags

    Ex: [["stuff"],["customer","hello"],["table"], "time"]
    -> {'single_tags': ['stuff', 'table', 'time'], 'grouped_tags': [['customer', 'hello']]}

    :param tags_string: str
    :return: {'single_tags': List[str], 'grouped_tags': List[List[str]]}
    """

    # deserialize json
    tag_list = json.loads(tags_string)

    def is_single_tag(tag):
        """
        check if argument is a single tag
        returns true if string or list with one item

        :param tag: Union[str, List[str]]
        :return: bool
        """
        if isinstance(tag, str) or (isinstance(tag, list) and len(tag) == 1):
            return True
        else:
            return False

    def flatten_single_tags(single_tags_list):
        """
        flatten mixed single tags in to list of strings

        :param single_tags_list: List[Union[str, List[str]]]
        :return: List[str]
        """
        single_tags = []
        for tag in single_tags_list:
            if isinstance(tag, str):
                single_tags.append(tag)
            else:
                single_tags.append(tag[0])
        return single_tags

    return dict({
        'single_tags': flatten_single_tags(list(filter(is_single_tag, tag_list))),
        'grouped_tags': list(filter(lambda t: not is_single_tag(t), tag_list))
    })
