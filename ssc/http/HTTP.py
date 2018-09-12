MIME_JSON = 'application/json'
MIME_CSS = 'text/css'
MIME_TEXT = 'text/plain'
MIME_HTML = 'text/html'
MIME_IMAGE_JPEG = 'image/jpeg'
MIME_IMAGE_PNG = 'image/png'
MIME_JSON = 'application/json'
MIME_BINARY = 'application/octet-stream'
MIME_SVG = 'image/svg+xml'
MIME_XML = 'text/xml'

HDR_CONTENT_TYPE = 'Content-type'
HDR_CONTENT_LENGTH = 'Content-length'
HDR_ACCEPT = 'Accept'
HDR_USER_AGENT = 'User-Agent'
HDR_TRANSFER_ENCODING = 'Transfer-Encoding'
HDR_CONNECTION = 'Connection'
HDR_LOCATION = 'Location'
HDR_SET_COOKIE = 'Set-Cookie'
HDR_COOKIE = 'Cookie'

TRANSFER_ENCODING_CHUNKED = 'chunked'

CONNECTION_KEEP_ALIVE = 'keep-alive'
CONNECTION_CLOSE = 'close'

CODE_OK = 200
CODE_BAD_REQUEST = 400
CODE_NOT_FOUND = 404
CODE_INTERNAL_SERVER_ERROR = 500
CODE_NOT_IMPLEMENTED = 501
CODE_REDIRECT = 301

PROTOCOL_VERSION_1_0 = 'HTTP/1.0'
PROTOCOL_VERSION_1_1 = 'HTTP/1.1'

EXT_TO_CONTENT_TYPE = {
 (
    '.css',
 ) : MIME_CSS,

 (
    '.txt',
    '.py',
    '.c',
    '.cpp',
    '.h',
    '.java',
    '.js',
    '.html'
 ) : MIME_TEXT,

 (
    '.jpg',
    '.jpeg',
 ) : MIME_IMAGE_JPEG,

 (
    '.png',
 ) : MIME_IMAGE_PNG,

 (
    '.json',
    '.map',
 ) : MIME_JSON,

 (
    '.svg',
 ) : MIME_SVG

}