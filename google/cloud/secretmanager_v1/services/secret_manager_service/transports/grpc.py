# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.secretmanager_v1.types import resources
from google.cloud.secretmanager_v1.types import service
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import SecretManagerServiceTransport, DEFAULT_CLIENT_INFO


class SecretManagerServiceGrpcTransport(SecretManagerServiceTransport):
    """gRPC backend transport for SecretManagerService.

    Secret Manager Service

    Manages secrets and operations using those secrets. Implements a
    REST model with the following objects:

    -  [Secret][google.cloud.secretmanager.v1.Secret]
    -  [SecretVersion][google.cloud.secretmanager.v1.SecretVersion]

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "secretmanager.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._ssl_channel_credentials = ssl_channel_credentials

        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        elif api_mtls_endpoint:
            warnings.warn(
                "api_mtls_endpoint and client_cert_source are deprecated",
                DeprecationWarning,
            )

            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            self._ssl_channel_credentials = ssl_credentials
        else:
            host = host if ":" in host else host + ":443"

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_channel_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        self._stubs = {}  # type: Dict[str, Callable]

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
            client_info=client_info,
        )

    @classmethod
    def create_channel(
        cls,
        host: str = "secretmanager.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def list_secrets(
        self,
    ) -> Callable[[service.ListSecretsRequest], service.ListSecretsResponse]:
        r"""Return a callable for the list secrets method over gRPC.

        Lists [Secrets][google.cloud.secretmanager.v1.Secret].

        Returns:
            Callable[[~.ListSecretsRequest],
                    ~.ListSecretsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_secrets" not in self._stubs:
            self._stubs["list_secrets"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/ListSecrets",
                request_serializer=service.ListSecretsRequest.serialize,
                response_deserializer=service.ListSecretsResponse.deserialize,
            )
        return self._stubs["list_secrets"]

    @property
    def create_secret(
        self,
    ) -> Callable[[service.CreateSecretRequest], resources.Secret]:
        r"""Return a callable for the create secret method over gRPC.

        Creates a new [Secret][google.cloud.secretmanager.v1.Secret]
        containing no
        [SecretVersions][google.cloud.secretmanager.v1.SecretVersion].

        Returns:
            Callable[[~.CreateSecretRequest],
                    ~.Secret]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_secret" not in self._stubs:
            self._stubs["create_secret"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/CreateSecret",
                request_serializer=service.CreateSecretRequest.serialize,
                response_deserializer=resources.Secret.deserialize,
            )
        return self._stubs["create_secret"]

    @property
    def add_secret_version(
        self,
    ) -> Callable[[service.AddSecretVersionRequest], resources.SecretVersion]:
        r"""Return a callable for the add secret version method over gRPC.

        Creates a new
        [SecretVersion][google.cloud.secretmanager.v1.SecretVersion]
        containing secret data and attaches it to an existing
        [Secret][google.cloud.secretmanager.v1.Secret].

        Returns:
            Callable[[~.AddSecretVersionRequest],
                    ~.SecretVersion]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "add_secret_version" not in self._stubs:
            self._stubs["add_secret_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/AddSecretVersion",
                request_serializer=service.AddSecretVersionRequest.serialize,
                response_deserializer=resources.SecretVersion.deserialize,
            )
        return self._stubs["add_secret_version"]

    @property
    def get_secret(self) -> Callable[[service.GetSecretRequest], resources.Secret]:
        r"""Return a callable for the get secret method over gRPC.

        Gets metadata for a given
        [Secret][google.cloud.secretmanager.v1.Secret].

        Returns:
            Callable[[~.GetSecretRequest],
                    ~.Secret]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_secret" not in self._stubs:
            self._stubs["get_secret"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/GetSecret",
                request_serializer=service.GetSecretRequest.serialize,
                response_deserializer=resources.Secret.deserialize,
            )
        return self._stubs["get_secret"]

    @property
    def update_secret(
        self,
    ) -> Callable[[service.UpdateSecretRequest], resources.Secret]:
        r"""Return a callable for the update secret method over gRPC.

        Updates metadata of an existing
        [Secret][google.cloud.secretmanager.v1.Secret].

        Returns:
            Callable[[~.UpdateSecretRequest],
                    ~.Secret]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_secret" not in self._stubs:
            self._stubs["update_secret"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/UpdateSecret",
                request_serializer=service.UpdateSecretRequest.serialize,
                response_deserializer=resources.Secret.deserialize,
            )
        return self._stubs["update_secret"]

    @property
    def delete_secret(self) -> Callable[[service.DeleteSecretRequest], empty.Empty]:
        r"""Return a callable for the delete secret method over gRPC.

        Deletes a [Secret][google.cloud.secretmanager.v1.Secret].

        Returns:
            Callable[[~.DeleteSecretRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_secret" not in self._stubs:
            self._stubs["delete_secret"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/DeleteSecret",
                request_serializer=service.DeleteSecretRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_secret"]

    @property
    def list_secret_versions(
        self,
    ) -> Callable[
        [service.ListSecretVersionsRequest], service.ListSecretVersionsResponse
    ]:
        r"""Return a callable for the list secret versions method over gRPC.

        Lists
        [SecretVersions][google.cloud.secretmanager.v1.SecretVersion].
        This call does not return secret data.

        Returns:
            Callable[[~.ListSecretVersionsRequest],
                    ~.ListSecretVersionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_secret_versions" not in self._stubs:
            self._stubs["list_secret_versions"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/ListSecretVersions",
                request_serializer=service.ListSecretVersionsRequest.serialize,
                response_deserializer=service.ListSecretVersionsResponse.deserialize,
            )
        return self._stubs["list_secret_versions"]

    @property
    def get_secret_version(
        self,
    ) -> Callable[[service.GetSecretVersionRequest], resources.SecretVersion]:
        r"""Return a callable for the get secret version method over gRPC.

        Gets metadata for a
        [SecretVersion][google.cloud.secretmanager.v1.SecretVersion].

        ``projects/*/secrets/*/versions/latest`` is an alias to the
        ``latest``
        [SecretVersion][google.cloud.secretmanager.v1.SecretVersion].

        Returns:
            Callable[[~.GetSecretVersionRequest],
                    ~.SecretVersion]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_secret_version" not in self._stubs:
            self._stubs["get_secret_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/GetSecretVersion",
                request_serializer=service.GetSecretVersionRequest.serialize,
                response_deserializer=resources.SecretVersion.deserialize,
            )
        return self._stubs["get_secret_version"]

    @property
    def access_secret_version(
        self,
    ) -> Callable[
        [service.AccessSecretVersionRequest], service.AccessSecretVersionResponse
    ]:
        r"""Return a callable for the access secret version method over gRPC.

        Accesses a
        [SecretVersion][google.cloud.secretmanager.v1.SecretVersion].
        This call returns the secret data.

        ``projects/*/secrets/*/versions/latest`` is an alias to the
        ``latest``
        [SecretVersion][google.cloud.secretmanager.v1.SecretVersion].

        Returns:
            Callable[[~.AccessSecretVersionRequest],
                    ~.AccessSecretVersionResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "access_secret_version" not in self._stubs:
            self._stubs["access_secret_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/AccessSecretVersion",
                request_serializer=service.AccessSecretVersionRequest.serialize,
                response_deserializer=service.AccessSecretVersionResponse.deserialize,
            )
        return self._stubs["access_secret_version"]

    @property
    def disable_secret_version(
        self,
    ) -> Callable[[service.DisableSecretVersionRequest], resources.SecretVersion]:
        r"""Return a callable for the disable secret version method over gRPC.

        Disables a
        [SecretVersion][google.cloud.secretmanager.v1.SecretVersion].

        Sets the
        [state][google.cloud.secretmanager.v1.SecretVersion.state] of
        the [SecretVersion][google.cloud.secretmanager.v1.SecretVersion]
        to
        [DISABLED][google.cloud.secretmanager.v1.SecretVersion.State.DISABLED].

        Returns:
            Callable[[~.DisableSecretVersionRequest],
                    ~.SecretVersion]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "disable_secret_version" not in self._stubs:
            self._stubs["disable_secret_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/DisableSecretVersion",
                request_serializer=service.DisableSecretVersionRequest.serialize,
                response_deserializer=resources.SecretVersion.deserialize,
            )
        return self._stubs["disable_secret_version"]

    @property
    def enable_secret_version(
        self,
    ) -> Callable[[service.EnableSecretVersionRequest], resources.SecretVersion]:
        r"""Return a callable for the enable secret version method over gRPC.

        Enables a
        [SecretVersion][google.cloud.secretmanager.v1.SecretVersion].

        Sets the
        [state][google.cloud.secretmanager.v1.SecretVersion.state] of
        the [SecretVersion][google.cloud.secretmanager.v1.SecretVersion]
        to
        [ENABLED][google.cloud.secretmanager.v1.SecretVersion.State.ENABLED].

        Returns:
            Callable[[~.EnableSecretVersionRequest],
                    ~.SecretVersion]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "enable_secret_version" not in self._stubs:
            self._stubs["enable_secret_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/EnableSecretVersion",
                request_serializer=service.EnableSecretVersionRequest.serialize,
                response_deserializer=resources.SecretVersion.deserialize,
            )
        return self._stubs["enable_secret_version"]

    @property
    def destroy_secret_version(
        self,
    ) -> Callable[[service.DestroySecretVersionRequest], resources.SecretVersion]:
        r"""Return a callable for the destroy secret version method over gRPC.

        Destroys a
        [SecretVersion][google.cloud.secretmanager.v1.SecretVersion].

        Sets the
        [state][google.cloud.secretmanager.v1.SecretVersion.state] of
        the [SecretVersion][google.cloud.secretmanager.v1.SecretVersion]
        to
        [DESTROYED][google.cloud.secretmanager.v1.SecretVersion.State.DESTROYED]
        and irrevocably destroys the secret data.

        Returns:
            Callable[[~.DestroySecretVersionRequest],
                    ~.SecretVersion]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "destroy_secret_version" not in self._stubs:
            self._stubs["destroy_secret_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/DestroySecretVersion",
                request_serializer=service.DestroySecretVersionRequest.serialize,
                response_deserializer=resources.SecretVersion.deserialize,
            )
        return self._stubs["destroy_secret_version"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy.SetIamPolicyRequest], policy.Policy]:
        r"""Return a callable for the set iam policy method over gRPC.

        Sets the access control policy on the specified secret. Replaces
        any existing policy.

        Permissions on
        [SecretVersions][google.cloud.secretmanager.v1.SecretVersion]
        are enforced according to the policy set on the associated
        [Secret][google.cloud.secretmanager.v1.Secret].

        Returns:
            Callable[[~.SetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_iam_policy" not in self._stubs:
            self._stubs["set_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/SetIamPolicy",
                request_serializer=iam_policy.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy.GetIamPolicyRequest], policy.Policy]:
        r"""Return a callable for the get iam policy method over gRPC.

        Gets the access control policy for a secret.
        Returns empty policy if the secret exists and does not
        have a policy set.

        Returns:
            Callable[[~.GetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_iam_policy" not in self._stubs:
            self._stubs["get_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/GetIamPolicy",
                request_serializer=iam_policy.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy.TestIamPermissionsRequest], iam_policy.TestIamPermissionsResponse
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.

        Returns permissions that a caller has for the specified secret.
        If the secret does not exist, this call returns an empty set of
        permissions, not a NOT_FOUND error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for
        authorization checking. This operation may "fail open" without
        warning.

        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    ~.TestIamPermissionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "test_iam_permissions" not in self._stubs:
            self._stubs["test_iam_permissions"] = self.grpc_channel.unary_unary(
                "/google.cloud.secretmanager.v1.SecretManagerService/TestIamPermissions",
                request_serializer=iam_policy.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]


__all__ = ("SecretManagerServiceGrpcTransport",)
