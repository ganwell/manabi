from wsgidav.dc.simple_dc import SimpleDomainController
from wsgidav.fs_dav_provider import FilesystemProvider
from wsgidav.middleware import BaseMiddleware


class CamacAuthenticator(BaseMiddleware):
    def __call__(self, environ, start_response):
        print("hello middleware")
        return self.next_app(environ, start_response)


class CamacDomainCotroller(SimpleDomainController):
    def require_authentication(self, realm, environ):
        print("hello controller")
        return False


class CamacProvider(FilesystemProvider):
    def get_resource_inst(self, path, environ):
        print("hello provider")
        return super().get_resource_inst(path, environ)
