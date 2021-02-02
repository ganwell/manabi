Manabi
======

Install
-------

Make sure libsodium exists on the system, for example execute:

```bash
apk add --no-cache libsodium
apt-get install -y libsodium23
```

Config
------

Call `manabi-keygen` and add the key to `config["manabi"]["key"]`. The key is
shared between the caluma/alexandria backend and the WebDAV server.

Dev
===

When changing dependencies or the build image, ie any of these files:

* c/build
* c/install
* c/pipinstall
* Dockerfile
* Pipfile
* Pipfile.lock
* setup.cfg
* setup.py
* MANIFEST.in

You need to merge the changes to master first, because the container can only be
published by a master build.

!! Do not forget to increment MANABI_IMAGE_VERSION in ./c/config


TODO later
----------

* use has_a instead of is_a when extending wsgi-dav classes to harden against
  implementation changes

Config
------

mount_path
: prefix that gets passed to wsgidav, if URL rewrites remove any prefixes use
`"/"`

lock_manager
: The ManabiLockLockStorage forces the WebDav log-timeout to 
`token-refresh-time / 2`

provider_mapping
: Extends the FilesystemProvider any will only serve files if the token is valid

middleware_stack
: based on the default middleware_stack but HTTPAuthenticator is replace by
ManabiAuthenticator, which validates the tokens.

manabi.key
: shared-key between the server that creates tokens to grant access and wsgi-dav

manabi.refresh
: how often tokens are refreshed in seconds, we recommend 10 minutes: `600`

manabi.initial
: the time from the token being generated till it has to be refreshed the first
time, we recommend 1 minues: `60`. In case tokens leak, for example via cache on
a computer, tokens should be expired by the time an adversary gets them.

```python
config = {
    "mount_path": "/dav",
    "lock_manager": ManabiLockLockStorage(refresh),
    "provider_mapping": {
        "/": ManabiProvider(settings.MEDIA_ROOT),
    },
    "middleware_stack": [
        WsgiDavDebugFilter,
        ErrorPrinter,
        ManabiAuthenticator,
        WsgiDavDirBrowser,
        RequestResolver,
    ],
    "manabi": {
        "key": key,
        "refresh": refresh,
        "initial": settings.MANABI_TOKEN_ACTIVATE_TIMEOUT,
    },
}
```

Release notes
=============

0.2
---

* Users should add

```python
    "hotfixes": {
        "re_encode_path_info": False,
    },
```

to their config, as this workaround is not correct on webservers that work
correctly. I we have tested this extensively with cherrypy.
