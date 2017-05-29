import config
import vk


api_version = 5.63
vkapi = vk.API(vk.Session(access_token=config.vk_access_token), v=api_version)
