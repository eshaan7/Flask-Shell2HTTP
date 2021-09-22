# Changelog

**[Get it on PyPi](https://pypi.org/project/Flask-Shell2HTTP/)**

## [v1.8.0](https://github.com/eshaan7/Flask-Shell2HTTP/releases/tag/v1.8.0)

- Allow `&wait=[false|true]` query parameter in `GET` request. Use `wait=true` when you don't wish to HTTP poll and want the result in a single request only.


## [v1.7.0](https://github.com/eshaan7/Flask-Shell2HTTP/releases/tag/v1.7.0)

**For you:**
- Deps: Support for both Flask version 1.x and 2.x.
- Feature: The `key` and `result_url` attributes are returned in response even if error is raised (if and when applicable) (See [#25](https://github.com/eshaan7/Flask-Shell2HTTP/issues/25)).
- Docs: Add info about `force_unique_key` option to quickstart guide.

**Internal:**
- Much better and improved test cases via tox matrix for both major flask versions, 1.x and 2.x.
- Much better overall type hinting.


## [v1.6.0](https://github.com/eshaan7/Flask-Shell2HTTP/releases/tag/v1.6.0)

Added support for a new parameter `force_unique_key` in the POST request. 

```json
    "force_unique_key": {
      "type": "boolean",
      "title": "Flag to enable/disable internal rate limiting mechanism",
      "description": "By default, the key is the SHA1 sum of the command + args POSTed to the API. This is done as a rate limiting measure so as to prevent multiple jobs with same parameters, if one such job is already running. If force_unique_key is set to true, the API will bypass this default behaviour and a psuedorandom key will be returned instead",
      "default": false
    }
```

See [post-request-options configuration](https://flask-shell2http.readthedocs.io/en/latest/Configuration.html#post-request-options) in docs for more info.


_For prior versions, see directly [here](https://github.com/eshaan7/Flask-Shell2HTTP/releases/tag/)._ 