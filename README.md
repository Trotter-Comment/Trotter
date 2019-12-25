# Trotter

一个基于阿里云函数计算与对象存储的零成本无服务器评论系统.

## 服务端

无论你是想本地调试 Trotter 的服务端, 还是直接部署到阿里云函数计算上, 都需要在克隆下来的项目的根目录下建立 `.env` 文件, 写入如下内容:

```bash
WEBSITE = '你的网站根目录, 例如: https://abersheeran.com'
OSS_BUCKET = 'OSS-BUCKET 名称'
OSS_KEYID = '有权限访问的 OSS 的 RAM 用户 KEY'
OSS_SECRET = '上述用户名对应的密钥'
OSS_LINK = '阿里云提供的用以访问 OSS 的链接, 例如: https://oss-cn-hongkong.aliyuncs.com'
ADMIN_EMAIL = '你自己的邮箱'
EMAIL_SERVER_HOST = '类似于: smtp.qq.com'
EMAIL_SERVER_PORT = 587
EMAIL_USERNAME = '用于发送邮件的邮箱'
EMAIL_PASSWORD = '上述邮箱的密码或者授权码'
```

### 调试服务端

运行 `pipenv install` 安装所有需要的依赖.

Trotter 使用 flask 作为 WSGI 接口供给与阿里云函数计算使用. 所以, 在本地调试时, 你既可以使用阿里云的方案去调试, 也可以使用 flask 的方式去调试.

我更推荐使用 flask 的方法去调试, app 入口在 `comment.app` 中.

### 部署服务端

部署服务端需要一个 template.yml, 用以指挥 [`fun`](https://github.com/alibaba/funcraft) 该如何去部署服务.

在克隆下来的 Trotter 根目录下运行 `pipenv run python script/create-template.py` 脚本, 一个完整的 `template.yml` 将被创建.

运行 `fun config` 配置阿里云函数计算的相关账号密码等信息.

最后, 只需要通过 `fun install; fun deploy` 部署服务到阿里云的函数计算即可.

## 客户端

to be continue......
