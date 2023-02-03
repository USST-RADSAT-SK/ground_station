# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: RProtocol.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='RProtocol.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0fRProtocol.proto\"I\n\x10protocol_message\x12\x13\n\x03\x41\x63k\x18\x01 \x01(\x0b\x32\x04.ackH\x00\x12\x15\n\x04Nack\x18\x02 \x01(\x0b\x32\x05.nackH\x00\x42\t\n\x07message\"\x13\n\x03\x61\x63k\x12\x0c\n\x04resp\x18\x01 \x01(\r\"\x14\n\x04nack\x12\x0c\n\x04resp\x18\x01 \x01(\rb\x06proto3'
)




_PROTOCOL_MESSAGE = _descriptor.Descriptor(
  name='protocol_message',
  full_name='protocol_message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Ack', full_name='protocol_message.Ack', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Nack', full_name='protocol_message.Nack', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='message', full_name='protocol_message.message',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=19,
  serialized_end=92,
)


_ACK = _descriptor.Descriptor(
  name='ack',
  full_name='ack',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resp', full_name='ack.resp', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=94,
  serialized_end=113,
)


_NACK = _descriptor.Descriptor(
  name='nack',
  full_name='nack',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resp', full_name='nack.resp', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=115,
  serialized_end=135,
)

_PROTOCOL_MESSAGE.fields_by_name['Ack'].message_type = _ACK
_PROTOCOL_MESSAGE.fields_by_name['Nack'].message_type = _NACK
_PROTOCOL_MESSAGE.oneofs_by_name['message'].fields.append(
  _PROTOCOL_MESSAGE.fields_by_name['Ack'])
_PROTOCOL_MESSAGE.fields_by_name['Ack'].containing_oneof = _PROTOCOL_MESSAGE.oneofs_by_name['message']
_PROTOCOL_MESSAGE.oneofs_by_name['message'].fields.append(
  _PROTOCOL_MESSAGE.fields_by_name['Nack'])
_PROTOCOL_MESSAGE.fields_by_name['Nack'].containing_oneof = _PROTOCOL_MESSAGE.oneofs_by_name['message']
DESCRIPTOR.message_types_by_name['protocol_message'] = _PROTOCOL_MESSAGE
DESCRIPTOR.message_types_by_name['ack'] = _ACK
DESCRIPTOR.message_types_by_name['nack'] = _NACK
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

protocol_message = _reflection.GeneratedProtocolMessageType('protocol_message', (_message.Message,), {
  'DESCRIPTOR' : _PROTOCOL_MESSAGE,
  '__module__' : 'RProtocol_pb2'
  # @@protoc_insertion_point(class_scope:protocol_message)
  })
_sym_db.RegisterMessage(protocol_message)

ack = _reflection.GeneratedProtocolMessageType('ack', (_message.Message,), {
  'DESCRIPTOR' : _ACK,
  '__module__' : 'RProtocol_pb2'
  # @@protoc_insertion_point(class_scope:ack)
  })
_sym_db.RegisterMessage(ack)

nack = _reflection.GeneratedProtocolMessageType('nack', (_message.Message,), {
  'DESCRIPTOR' : _NACK,
  '__module__' : 'RProtocol_pb2'
  # @@protoc_insertion_point(class_scope:nack)
  })
_sym_db.RegisterMessage(nack)


# @@protoc_insertion_point(module_scope)
