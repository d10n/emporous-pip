from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthConfig(_message.Message):
    __slots__ = ["access_token", "password", "refresh_token", "registry_host", "username"]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REGISTRY_HOST_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    password: str
    refresh_token: str
    registry_host: str
    username: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ..., registry_host: _Optional[str] = ..., access_token: _Optional[str] = ..., refresh_token: _Optional[str] = ...) -> None: ...

class Collection(_message.Message):
    __slots__ = ["files", "linked_collections", "schema_address"]
    FILES_FIELD_NUMBER: _ClassVar[int]
    LINKED_COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[File]
    linked_collections: _containers.RepeatedScalarFieldContainer[str]
    schema_address: str
    def __init__(self, schema_address: _Optional[str] = ..., linked_collections: _Optional[_Iterable[str]] = ..., files: _Optional[_Iterable[_Union[File, _Mapping]]] = ...) -> None: ...

class Diagnostic(_message.Message):
    __slots__ = ["detail", "severity", "summary"]
    class Severity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_ERROR: Diagnostic.Severity
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_UNSPECIFIED: Diagnostic.Severity
    SEVERITY_WARNING: Diagnostic.Severity
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    detail: str
    severity: Diagnostic.Severity
    summary: str
    def __init__(self, severity: _Optional[_Union[Diagnostic.Severity, str]] = ..., summary: _Optional[str] = ..., detail: _Optional[str] = ...) -> None: ...

class File(_message.Message):
    __slots__ = ["attributes", "file"]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    attributes: _struct_pb2.Struct
    file: str
    def __init__(self, file: _Optional[str] = ..., attributes: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class List(_message.Message):
    __slots__ = []
    class Request(_message.Message):
        __slots__ = ["auth", "filter", "source"]
        AUTH_FIELD_NUMBER: _ClassVar[int]
        FILTER_FIELD_NUMBER: _ClassVar[int]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        auth: AuthConfig
        filter: _struct_pb2.Struct
        source: str
        def __init__(self, source: _Optional[str] = ..., filter: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., auth: _Optional[_Union[AuthConfig, _Mapping]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["collection", "diagnostics"]
        COLLECTION_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        collection: Collection
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        def __init__(self, collection: _Optional[_Union[Collection, _Mapping]] = ..., diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping]]] = ...) -> None: ...
    def __init__(self) -> None: ...

class Publish(_message.Message):
    __slots__ = []
    class Request(_message.Message):
        __slots__ = ["auth", "collection", "destination", "source"]
        AUTH_FIELD_NUMBER: _ClassVar[int]
        COLLECTION_FIELD_NUMBER: _ClassVar[int]
        DESTINATION_FIELD_NUMBER: _ClassVar[int]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        auth: AuthConfig
        collection: Collection
        destination: str
        source: str
        def __init__(self, source: _Optional[str] = ..., destination: _Optional[str] = ..., collection: _Optional[_Union[Collection, _Mapping]] = ..., auth: _Optional[_Union[AuthConfig, _Mapping]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["diagnostics", "digest"]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        DIGEST_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        digest: str
        def __init__(self, digest: _Optional[str] = ..., diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping]]] = ...) -> None: ...
    def __init__(self) -> None: ...

class ReadLayer(_message.Message):
    __slots__ = []
    class Request(_message.Message):
        __slots__ = ["auth", "layer_title", "source"]
        AUTH_FIELD_NUMBER: _ClassVar[int]
        LAYER_TITLE_FIELD_NUMBER: _ClassVar[int]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        auth: AuthConfig
        layer_title: str
        source: str
        def __init__(self, source: _Optional[str] = ..., layer_title: _Optional[str] = ..., auth: _Optional[_Union[AuthConfig, _Mapping]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["binary", "diagnostic"]
        BINARY_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTIC_FIELD_NUMBER: _ClassVar[int]
        binary: bytes
        diagnostic: Diagnostic
        def __init__(self, diagnostic: _Optional[_Union[Diagnostic, _Mapping]] = ..., binary: _Optional[bytes] = ...) -> None: ...
    def __init__(self) -> None: ...

class ReadLayerStream(_message.Message):
    __slots__ = []
    class Request(_message.Message):
        __slots__ = ["auth", "destination", "filter", "source"]
        AUTH_FIELD_NUMBER: _ClassVar[int]
        DESTINATION_FIELD_NUMBER: _ClassVar[int]
        FILTER_FIELD_NUMBER: _ClassVar[int]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        auth: AuthConfig
        destination: str
        filter: _struct_pb2.Struct
        source: str
        def __init__(self, source: _Optional[str] = ..., destination: _Optional[str] = ..., filter: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., auth: _Optional[_Union[AuthConfig, _Mapping]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["chunk", "diagnostic"]
        CHUNK_FIELD_NUMBER: _ClassVar[int]
        DIAGNOSTIC_FIELD_NUMBER: _ClassVar[int]
        chunk: bytes
        diagnostic: Diagnostic
        def __init__(self, diagnostic: _Optional[_Union[Diagnostic, _Mapping]] = ..., chunk: _Optional[bytes] = ...) -> None: ...
    def __init__(self) -> None: ...

class Retrieve(_message.Message):
    __slots__ = []
    class Request(_message.Message):
        __slots__ = ["auth", "destination", "filter", "source"]
        AUTH_FIELD_NUMBER: _ClassVar[int]
        DESTINATION_FIELD_NUMBER: _ClassVar[int]
        FILTER_FIELD_NUMBER: _ClassVar[int]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        auth: AuthConfig
        destination: str
        filter: _struct_pb2.Struct
        source: str
        def __init__(self, source: _Optional[str] = ..., destination: _Optional[str] = ..., filter: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., auth: _Optional[_Union[AuthConfig, _Mapping]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ["diagnostics", "digests"]
        DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
        DIGESTS_FIELD_NUMBER: _ClassVar[int]
        diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
        digests: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, digests: _Optional[_Iterable[str]] = ..., diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping]]] = ...) -> None: ...
    def __init__(self) -> None: ...
