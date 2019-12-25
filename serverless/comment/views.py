import pickle
import datetime

from flask import (
    jsonify,
    request,
    render_template
)
import oss2

from .settings import OSS_BUCKET, OSS_KEYID, OSS_SECRET, OSS_LINK, WEBSITE, ADMIN_EMAIL
from .utils import route, View, ranstr, get_avatar


bucket = None


def init(context):
    global bucket
    bucket = oss2.Bucket(
        oss2.Auth(OSS_KEYID, OSS_SECRET),
        OSS_LINK,
        OSS_BUCKET
    )


@route("/comment")
class Comment(View):

    def get(self):
        page_uri = request.args["page-uri"]
        marker = request.args.get('marker', '')
        count = request.args.get("count", 10)

        result = bucket.list_objects(f"comment/{page_uri}/", max_keys=count, marker=marker)
        comments = []
        for obj in result.object_list:
            comment = pickle.loads(bucket.get_object(obj.key).read())
            del comment['email']
            comments.append(comment)
        return jsonify({
            "comments": comments,
            "has_more": result.is_truncated,
            "next_marker": result.next_marker,
        })


    def post(self):
        page_uri = request.form['page-uri']
        nickname = request.form['nickname']
        email = request.form['email']
        content = request.form['content']

        key = ranstr()
        comment = {
            "key": key,
            "page-uri": page_uri,
            "nickname": nickname,
            "email": email,
            "avatar": get_avatar(email),
            "content": content,
            "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }

        bucket.put_object(f'comment/{page_uri}/{key}', pickle.dumps(comment))
        bucket.put_object(f'mail/admin-{key}.task', pickle.dumps({
            "nickname": nickname,
            "to_email": ADMIN_EMAIL,
            "subject": "你的网站在 Trotter 上有一条新评论",
            "content": render_template(
                'new-comment.html',
                message=content,
                page_uri=page_uri,
                website=WEBSITE
            )
        }))

        return jsonify({
            "comment": comment
        })
