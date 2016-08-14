# -*- coding: utf-8 -*-
"""
"""

cimport cython

from enum import IntEnum, Enum


cdef extern from "Python.h":
    object PyBytes_FromStringAndSize(char *s, int len)


cdef extern from "wbxml.h":
    ctypedef unsigned char      WB_BOOL
    ctypedef unsigned char      WB_UTINY
    ctypedef char               WB_TINY
    ctypedef unsigned int       WB_ULONG
    ctypedef int                WB_LONG
    ctypedef unsigned int  WBXMLError
    cdef int WBXML_OK = WBXMLError.WBXML_OK

    ctypedef enum WBXMLVersion:
        WBXML_VERSION_UNKNOWN = -1
        WBXML_VERSION_10 = 0x00
        WBXML_VERSION_11 = 0x01
        WBXML_VERSION_12 = 0x02
        WBXML_VERSION_13 = 0x03

    ctypedef struct WBXMLConvXML2WBXML:
        WBXMLGenXMLType        gen_type
        WBXMLLanguage        lang
        WBXMLCharsetMIBEnum        charset
        WB_UTINY        indent
        WB_BOOL  keep_ignorable_ws

    ctypedef struct WBXMLConvWBXML2XML:
        WBXMLVersion wbxml_version
        WB_BOOL keep_ignorable_ws
        WB_BOOL use_strtbl
        WB_BOOL produce_anonymous

    ctypedef enum WBXMLLanguage:
        WBXML_LANG_UNKNOWN = 0  #   Unknown / Not Specified
        #   WAP
        WBXML_LANG_WML10 = 1101          #   WML 1.0
        WBXML_LANG_WML11 = 1102          #   WML 1.1
        WBXML_LANG_WML12 = 1103          #   WML 1.2
        WBXML_LANG_WML13 = 1104          #   WML 1.3
        WBXML_LANG_WTA10     = 1201      #   WTA 1.0
        WBXML_LANG_WTAWML12  = 1202      #   WTAWML 1.2
        WBXML_LANG_CHANNEL11 = 1203      #   CHANNEL 1.1
        WBXML_LANG_CHANNEL12 = 1204      #   CHANNEL 1.2
        WBXML_LANG_SI10 = 1301           #   SI 1.0
        WBXML_LANG_SL10 = 1401           #   SL 1.0
        WBXML_LANG_CO10 = 1501           #   CO 1.0
        WBXML_LANG_PROV10 = 1601         #   PROV 1.0
        WBXML_LANG_EMN10 = 1701          #   EMN 1.0
        WBXML_LANG_DRMREL10 = 1801       #   DRMREL 1.0
        #   Ericsson / Nokia OTA Settings v7.0
        WBXML_LANG_OTA_SETTINGS = 1901   #   OTA Settings
        #   SyncML
        WBXML_LANG_SYNCML_SYNCML10 = 2001  #   SYNCML 1.0
        WBXML_LANG_SYNCML_DEVINF10 = 2002  #   DEVINF 1.0
        WBXML_LANG_SYNCML_METINF10 = 2003  #   METINF 1.0
        WBXML_LANG_SYNCML_SYNCML11 = 2101  #    SYNCML 1.1
        WBXML_LANG_SYNCML_DEVINF11 = 2102  #   DEVINF 1.1
        WBXML_LANG_SYNCML_METINF11 = 2103  #   METINF 1.1
        WBXML_LANG_SYNCML_SYNCML12 = 2201  #   SYNCML 1.2
        WBXML_LANG_SYNCML_DEVINF12 = 2202  #   DEVINF 1.2
        WBXML_LANG_SYNCML_METINF12 = 2203  #   METINF 1.2
        WBXML_LANG_SYNCML_DMDDF12  = 2204  #   DMDDF  1.2
        #   Wireless-Village
        WBXML_LANG_WV_CSP11 = 2301       #   WV CSP 1.1
        WBXML_LANG_WV_CSP12 = 2302       #   WV CSP 1.2
        #   Microsoft AirSync
        WBXML_LANG_AIRSYNC    = 2401     #   AirSync
        WBXML_LANG_ACTIVESYNC = 2402     #   ActiveSync
        #   Nokia ConML
        WBXML_LANG_CONML = 2501            #   ConML

    ctypedef enum WBXMLGenXMLType:
        WBXML_GEN_XML_COMPACT = 0
        WBXML_GEN_XML_INDENT = 1
        WBXML_GEN_XML_CANONICAL = 2

    ctypedef enum WBXMLCharsetMIBEnum:
        WBXML_CHARSET_UNKNOWN = 0
        WBXML_CHARSET_US_ASCII = 3
        WBXML_CHARSET_ISO_8859_1 = 4
        WBXML_CHARSET_ISO_8859_2 = 5
        WBXML_CHARSET_ISO_8859_3 = 6
        WBXML_CHARSET_ISO_8859_4 = 7
        WBXML_CHARSET_ISO_8859_5 = 8
        WBXML_CHARSET_ISO_8859_6 = 9
        WBXML_CHARSET_ISO_8859_7 = 10
        WBXML_CHARSET_ISO_8859_8 = 11
        WBXML_CHARSET_ISO_8859_9 = 12
        WBXML_CHARSET_SHIFT_JIS = 17
        WBXML_CHARSET_UTF_8 = 106
        WBXML_CHARSET_ISO_10646_UCS_2 = 1000
        WBXML_CHARSET_UTF_16 = 1015
        WBXML_CHARSET_BIG5 = 2026

    void wbxml_conv_wbxml2xml_set_charset(WBXMLConvWBXML2XML *conv,
                                          WBXMLCharsetMIBEnum charset)
    void wbxml_conv_wbxml2xml_set_language(WBXMLConvWBXML2XML *conv,
                                           WBXMLLanguage lang)
    WBXMLError wbxml_conv_xml2wbxml_create(WBXMLConvXML2WBXML **conv)
    WBXMLError wbxml_conv_wbxml2xml_create(WBXMLConvWBXML2XML **conv)


    void wbxml_conv_xml2wbxml_set_version(WBXMLConvXML2WBXML *conv,
                                          WBXMLVersion wbxml_version)
    void wbxml_conv_xml2wbxml_disable_string_table(WBXMLConvXML2WBXML *conv)
    void wbxml_conv_xml2wbxml_enable_preserve_whitespaces(WBXMLConvXML2WBXML *conv)
    void wbxml_conv_xml2wbxml_disable_public_id(WBXMLConvXML2WBXML *conv)
    void wbxml_conv_wbxml2xml_enable_preserve_whitespaces(WBXMLConvWBXML2XML *conv)
    void wbxml_conv_wbxml2xml_set_indent(WBXMLConvWBXML2XML *conv,
                                         WB_UTINY indent)
    void wbxml_conv_wbxml2xml_set_gen_type(WBXMLConvWBXML2XML *conv,
                                           WBXMLGenXMLType gen_type)

    WBXMLError wbxml_conv_xml2wbxml_run(WBXMLConvXML2WBXML *conv,
                                                   WB_UTINY  *xml,
                                                   WB_ULONG   xml_len,
                                                   WB_UTINY **wbxml,
                                                   WB_ULONG  *wbxml_len)

    WBXMLError wbxml_conv_wbxml2xml_run(WBXMLConvWBXML2XML *conv,
                                                   WB_UTINY  *xml,
                                                   WB_ULONG   xml_len,
                                                   WB_UTINY **wbxml,
                                                   WB_ULONG  *wbxml_len)

    const WB_UTINY * wbxml_errors_string(WBXMLError error_code)


cdef extern from "stdlib.h":
    void free(void *ptr)


class Lang(IntEnum):
    UNKNOWN = WBXMLLanguage.WBXML_LANG_UNKNOWN #   Unknown / Not Specified
    WML10 = WBXMLLanguage.WBXML_LANG_WML10 #   WML 1.0
    WML11 = WBXMLLanguage.WBXML_LANG_WML11 #   WML 1.1
    WML12 = WBXMLLanguage.WBXML_LANG_WML12 #   WML 1.2
    WML13 = WBXMLLanguage.WBXML_LANG_WML13 #   WML 1.3
    WTA10     = WBXMLLanguage.WBXML_LANG_WTA10     #   WTA 1.0
    WTAWML12  = WBXMLLanguage.WBXML_LANG_WTAWML12  #   WTAWML 1.2
    CHANNEL11 = WBXMLLanguage.WBXML_LANG_CHANNEL11 #   CHANNEL 1.1
    CHANNEL12 = WBXMLLanguage.WBXML_LANG_CHANNEL12 #   CHANNEL 1.2
    SI10 = WBXMLLanguage.WBXML_LANG_SI10 #   SI 1.0
    SL10 = WBXMLLanguage.WBXML_LANG_SL10 #   SL 1.0
    CO10 = WBXMLLanguage.WBXML_LANG_CO10 #   CO 1.0
    PROV10 = WBXMLLanguage.WBXML_LANG_PROV10 #   PROV 1.0
    EMN10 = WBXMLLanguage.WBXML_LANG_EMN10 #   EMN 1.0
    DRMREL10 = WBXMLLanguage.WBXML_LANG_DRMREL10 #   DRMREL 1.0
    OTA_SETTINGS = WBXMLLanguage.WBXML_LANG_OTA_SETTINGS #   OTA Settings
    SYNCML_SYNCML10 = WBXMLLanguage.WBXML_LANG_SYNCML_SYNCML10 #   SYNCML 1.0
    SYNCML_DEVINF10 = WBXMLLanguage.WBXML_LANG_SYNCML_DEVINF10 #   DEVINF 1.0
    SYNCML_METINF10 = WBXMLLanguage.WBXML_LANG_SYNCML_METINF10 #   METINF 1.0
    SYNCML_SYNCML11 = WBXMLLanguage.WBXML_LANG_SYNCML_SYNCML11 #   SYNCML 1.1
    SYNCML_DEVINF11 = WBXMLLanguage.WBXML_LANG_SYNCML_DEVINF11 #   DEVINF 1.1
    SYNCML_METINF11 = WBXMLLanguage.WBXML_LANG_SYNCML_METINF11 #   METINF 1.1
    SYNCML_SYNCML12 = WBXMLLanguage.WBXML_LANG_SYNCML_SYNCML12 #   SYNCML 1.2
    SYNCML_DEVINF12 = WBXMLLanguage.WBXML_LANG_SYNCML_DEVINF12 #   DEVINF 1.2
    SYNCML_METINF12 = WBXMLLanguage.WBXML_LANG_SYNCML_METINF12 #   METINF 1.2
    SYNCML_DMDDF12  = WBXMLLanguage.WBXML_LANG_SYNCML_DMDDF12  #   DMDDF  1.2
    WV_CSP11 = WBXMLLanguage.WBXML_LANG_WV_CSP11 #   WV CSP 1.1
    WV_CSP12 = WBXMLLanguage.WBXML_LANG_WV_CSP12 #   WV CSP 1.2
    AIRSYNC    = WBXMLLanguage.WBXML_LANG_AIRSYNC    #   AirSync
    ACTIVESYNC = WBXMLLanguage.WBXML_LANG_ACTIVESYNC #   ActiveSync


class WBXMLCharset(IntEnum):
    UNKNOWN = WBXMLCharsetMIBEnum.WBXML_CHARSET_UNKNOWN
    US_ASCII = WBXMLCharsetMIBEnum.WBXML_CHARSET_US_ASCII
    ISO_8859_1 = WBXMLCharsetMIBEnum.WBXML_CHARSET_ISO_8859_1
    ISO_8859_2 = WBXMLCharsetMIBEnum.WBXML_CHARSET_ISO_8859_2
    ISO_8859_3 = WBXMLCharsetMIBEnum.WBXML_CHARSET_ISO_8859_3
    ISO_8859_4 = WBXMLCharsetMIBEnum.WBXML_CHARSET_ISO_8859_4
    ISO_8859_5 = WBXMLCharsetMIBEnum.WBXML_CHARSET_ISO_8859_5
    ISO_8859_6 = WBXMLCharsetMIBEnum.WBXML_CHARSET_ISO_8859_6
    ISO_8859_7 = WBXMLCharsetMIBEnum.WBXML_CHARSET_ISO_8859_7
    ISO_8859_8 = WBXMLCharsetMIBEnum.WBXML_CHARSET_ISO_8859_8
    ISO_8859_9 = WBXMLCharsetMIBEnum.WBXML_CHARSET_ISO_8859_9
    SHIFT_JIS = WBXMLCharsetMIBEnum.WBXML_CHARSET_SHIFT_JIS
    UTF_8 = WBXMLCharsetMIBEnum.WBXML_CHARSET_UTF_8
    ISO_10646_UCS_2 = WBXMLCharsetMIBEnum.WBXML_CHARSET_ISO_10646_UCS_2
    UTF_16 = WBXMLCharsetMIBEnum.WBXML_CHARSET_UTF_16
    BIG5 = WBXMLCharsetMIBEnum.WBXML_CHARSET_BIG5


class XMLType(IntEnum):

    COMPACT = WBXMLGenXMLType.WBXML_GEN_XML_COMPACT
    INDENT = WBXMLGenXMLType.WBXML_GEN_XML_INDENT
    CANONICAL = WBXMLGenXMLType.WBXML_GEN_XML_CANONICAL


class WbxmlVersion(Enum):
    UNKNOWN = WBXMLVersion.WBXML_VERSION_UNKNOWN
    V_10 = WBXMLVersion.WBXML_VERSION_10
    V_11 = WBXMLVersion.WBXML_VERSION_11
    V_12 = WBXMLVersion.WBXML_VERSION_12
    V_13 = WBXMLVersion.WBXML_VERSION_13


class WBXMLParseError(Exception):
    def __init__(self, code):
        self.code = code
        self.description = <char *> wbxml_errors_string(code)

    def __str__(self):
        return "%s (%d)" % (self.description, self.code)

    def __repr__(self):
        return self.__str__()


@cython.boundscheck(False)
def wbxml2xml(wbxml, lang=Lang.ACTIVESYNC, preserve_whitesaces=True,
              charset=WBXMLCharset.UTF_8, indent=4, xml_type=XMLType.INDENT):
    cdef WB_UTINY *xml
    cdef WB_ULONG xml_len
    cdef WBXMLError ret
    cdef WBXMLConvWBXML2XML *conv = NULL

    if not isinstance(lang, Lang):
        raise WBXMLParseError('Lang param is not enum')
    if not isinstance(charset, WBXMLCharset):
        raise WBXMLParseError('Charset param is not enum')
    if not isinstance(xml_type, XMLType):
        raise WBXMLParseError('xml_type param is not enum')

    retval = wbxml_conv_wbxml2xml_create(&conv)
    if retval != WBXML_OK:
        raise WBXMLParseError(retval)

    wbxml_conv_wbxml2xml_set_charset(conv, charset.value)
    wbxml_conv_wbxml2xml_set_language(conv, lang.value)
    if preserve_whitesaces:
        wbxml_conv_wbxml2xml_enable_preserve_whitespaces(conv)
    wbxml_conv_wbxml2xml_set_indent(conv, int(indent))

    wbxml_conv_wbxml2xml_set_gen_type(conv, xml_type.value)
    retval = wbxml_conv_wbxml2xml_run(conv, wbxml, len(wbxml), &xml, &xml_len)
    if retval != WBXML_OK:
        raise WBXMLParseError(retval)
    res =  PyBytes_FromStringAndSize(<char *>xml, xml_len)
    free(xml)
    del wbxml
    return res


@cython.boundscheck(False)
def xml2wbxml(xml, disable_string_table=True, preserve_whitespaces=True,
              remove_public_id=True, version=WbxmlVersion.V_13):
    cdef  WBXMLError ret = WBXML_OK
    cdef WBXMLConvXML2WBXML *conv = NULL
    cdef WB_UTINY * wbxml = NULL
    cdef WB_ULONG wbxml_len = 0

    if not isinstance(version, WbxmlVersion):
        raise WBXMLParseError('version param is not enum')

    ret = wbxml_conv_xml2wbxml_create(&conv)
    if ret != WBXML_OK:
        raise WBXMLParseError(ret)

    wbxml_conv_xml2wbxml_set_version(conv, version.value)
    if disable_string_table:
        wbxml_conv_xml2wbxml_disable_string_table(conv)
    if preserve_whitespaces:
        wbxml_conv_xml2wbxml_enable_preserve_whitespaces(conv)
    if remove_public_id:
        wbxml_conv_xml2wbxml_disable_public_id(conv)
    retval = wbxml_conv_xml2wbxml_run(conv, <WB_UTINY *> xml, len(xml),
                                &wbxml, &wbxml_len)
    if retval != 0:
        raise WBXMLParseError(retval)
    res = PyBytes_FromStringAndSize(<char *>wbxml, wbxml_len)
    free(wbxml)
    del xml
    return res
