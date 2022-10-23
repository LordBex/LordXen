
import requests
from requests.auth import HTTPBasicAuth

from LordXen.exceptions import *


class XenThread:
    def __init__(self, xforo, thread_id, title=None, tags=None, prefix_id=None, prefix=None):
        xforo: XenForo
        self.xforo = xforo
        self.thread_id = thread_id
        self.title = title
        self.tags = tags
        self.prefix = prefix
        self.prefix_id = prefix_id

    def info(self) -> dict:
        """
        get info from api
        @return: raw data from api
        """
        r = self.xforo.send_get_request(endpoint=f'threads/{self.thread_id}/')
        if r.status_code == 200:
            data = r.json()
            self.title = data['thread']['title']
            self.tags = data['thread']['tags']
            self.prefix = data['thread']['prefix']
            self.prefix_id = data['thread']['prefix_id']
            return data['thread']
        else:
            raise XenThreadNotExists(self.thread_id, response=r)

    def exists(self):
        """
        check if exists
        @return: bool
        """
        try:
            self.info()
            return True
        except XenThreadNotExists:
            return False

    def create_post(self, post):
        """
        Create Post
        @param post: post message 
        @return: bool | None
        """""
        payload = {
            'thread_id': int(self.thread_id),
            'message': post
        }
        x = self.xforo.send_post_request('posts/', payload)
        j = x.json()

        if "errors" in j.keys():
            xen_raise_error(error_key=j['errors'][0]['code'], message={j['errors'][0]['message']})

        return True

    def edit(self,
             prefix_id: int | None = None,
             title: str | None = None,
             discussion_open=None,
             sticky: bool | None = None,
             add_tags: list | None = None,
             remove_tags: list | None = None
             ):
        """
        Edit Thread data
        @param prefix_id: prefix as id
        @param title: Title of the thread.
        @param discussion_open:
        @param sticky:
        @param add_tags: add tags from Thread
        @param remove_tags: remove tags from Thread
        @return:
        """
        # TODO add custom_fields[<name>]: str
        data = {
            "prefix_id": prefix_id,
            "title": title,
            "discussion_open": discussion_open,
            "sticky": sticky,
            "add_tags[]": add_tags,
            "remove_tags[]": remove_tags
        }
        data = {k: v for k, v in data.items() if v is not None}

        # Generate post
        x = self.xforo.send_post_request(f'threads/{str(self.thread_id)}/', data)
        j = x.json()
        if "errors" in j.keys():
            xen_raise_error(error_key=j['errors'][0]['code'], message={j['errors'][0]['message']})
        return True


class XenNode:
    def __init__(self, xf, node_id, name=None):
        self.xforo = xf
        self.node_id = int(node_id)
        self.name = name

    def create_thread(self, title, message, tags=None, prefix_id=None) -> XenThread:
        if tags is None:
            tags = []

        payload = {
            'node_id': self.node_id,
            'title': title,
            'message': message,
            'tags[]': tags
        }
        if prefix_id is not None:
            payload['prefix_id'] = prefix_id

        x = self.xforo.send_post_request('threads/', payload)
        j = x.json()

        if "errors" in j.keys():
            xen_raise_error(error_key=j['errors'][0]['code'], message={j['errors'][0]['message']})

        new_thread = XenThread(xforo=self.xforo, thread_id=j['thread']['thread_id'], title=title)
        return new_thread


class XenForo(object):

    def __init__(self, url: str, api_key: str, http_auth=None):
        if url.endswith('/'):
            self.url = url
        else:
            self.url = url + '/'
        self.api_key = api_key
        self.header = {
            'Content-type': 'application/x-www-form-urlencoded',
            'XF-Api-Key': self.api_key
        }
        self.http_auth = HTTPBasicAuth(http_auth['user'], http_auth['password']) if http_auth is not None else None

    def send_get_request(self, endpoint, payload=None):
        if payload is None:
            payload = {}
        return requests.get(self.url + endpoint, data=payload, headers=self.header, auth=self.http_auth)

    def send_post_request(self, endpoint, payload=None):
        if payload is None:
            payload = {}
        u = self.url + endpoint
        return requests.post(u, data=payload, headers=self.header, auth=self.http_auth)

    def send_delete_request(self, endpoint, payload=None):
        if payload is None:
            payload = {}
        return requests.delete(self.url + endpoint, data=payload, headers=self.header, auth=self.http_auth)

    def get_node(self, node_id) -> XenNode:
        xf = self
        xn = XenNode(xf, node_id=node_id)
        return xn

    def get_thread(self, thread_id):
        return XenThread(xforo=self, thread_id=thread_id)

    def get_nodes(self):
        j = self.send_get_request('nodes/')
        j = j.json()
        return j        # TODO in procress

    def get_stats(self) -> dict:
        """
        Return data as dict from the Api-Stats endpoint
        @return:
        """
        r = self.send_get_request('stats/')
        if r.status_code == 200:
            j = r.json()
            return j
        else:
            raise XenApiException(error_key=r.status_code, message="Can't load Stats from XenForo", response=r)

