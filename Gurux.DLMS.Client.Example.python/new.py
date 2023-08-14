import os
import sys
import traceback
from gurux_dlms.enums import InterfaceType, Authentication, Security, Standard
from gurux_serial import GXSerial
from gurux_net import GXNet
from gurux_dlms.enums import ObjectType
from gurux_dlms.objects.GXDLMSObjectCollection import GXDLMSObjectCollection
from GXSettings import GXSettings
from GXDLMSReader import GXDLMSReader
from gurux_dlms.GXDLMSClient import GXDLMSClient
from gurux_common.GXCommon import GXCommon
from gurux_dlms.enums.DataType import DataType
import locale
from gurux_dlms.GXDateTime import GXDateTime
from gurux_dlms.internal._GXCommon import _GXCommon
from gurux_dlms import GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError, GXDLMSTranslator
from gurux_dlms import GXByteBuffer, GXDLMSTranslatorMessage, GXReplyData
from gurux_dlms.enums import RequestTypes, Security, InterfaceType
from gurux_dlms.secure.GXDLMSSecureClient import GXDLMSSecureClient
from GXSettings import GXSettings


x =  GXDLMSSecureClient(True)
y= GXSerial(None)
settings = GXSettings()

x.password = "ABCDEFGH"
x.standard = Standard.INDIA
x.authentication = Authentication.LOW
x.clientAddress = 32
y.port = "COM3"

reader = GXDLMSReader(settings.client, y, settings.trace, settings.invocationCounter)
y.open()
if settings.readObjects:
    read = False
    reader.initializeConnection()
    if settings.outputFile and os.path.exists(settings.outputFile):
        try:
            c = GXDLMSObjectCollection.load(settings.outputFile)
            settings.client.objects.extend(c)
            if settings.client.objects:
                read = True
        except Exception:
            read = False
            if not read:
                reader.getAssociationView()
            for k, v in settings.readObjects:
                obj = settings.client.objects.findByLN(ObjectType.NONE, k)
                if obj is None:
                    raise Exception("Unknown logical name:" + k)
                val = reader.read(obj, v)
                reader.showValue(v, val)
            if settings.outputFile:
                settings.client.objects.save(settings.outputFile)
        else:
                reader.readAll(settings.outputFile)