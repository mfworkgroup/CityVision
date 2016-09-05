from controllers import weibo_oauth
from controllers.common import weibo_services

oauth_service = weibo_oauth.WeiboOauthClient()
weibo_client = weibo_services.WeiboBatchUserService(access_tokens=set())
