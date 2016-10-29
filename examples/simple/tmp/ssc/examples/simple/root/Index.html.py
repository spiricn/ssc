# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1477748111.992618
_enable_loop = True
_template_filename = 'Y:\\ssc\\examples\\simple\\root\\Index.html'
_template_uri = '/ssc/examples/simple/root/Index.html'
_source_encoding = 'ascii'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        range = context.get('range', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('<html>\n\n<head>\n\n<title>Simple Page</title>\n\n</head>\n\n<body>\n\n')
        for i in range(10):
            __M_writer('\n\t<p>Hello world ')
            __M_writer(str(i))
            __M_writer(' !</p>\n\n')
        __M_writer('\n</body>\n\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "Y:\\ssc\\examples\\simple\\root\\Index.html", "source_encoding": "ascii", "uri": "/ssc/examples/simple/root/Index.html", "line_map": {"16": 0, "33": 27, "22": 1, "23": 11, "24": 12, "25": 13, "26": 13, "27": 16}}
__M_END_METADATA
"""
