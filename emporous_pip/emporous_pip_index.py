#!/usr/bin/env python
# -*- coding: utf8 -*-
# emporous_pip_index.py

import html
import http.server
import pathlib
import signal
import subprocess
import sys
import os
import asyncio
import textwrap
import urllib.parse
# from google.protobuf.internal.well_known_types import Struct
from google.protobuf.struct_pb2 import Struct
from google.protobuf import json_format

from docker import auth
import xml.etree.ElementTree as ET
import re

# https://github.com/protocolbuffers/protobuf/issues/881#issuecomment-336811686
from generated import manager_pb2

import grpc

from generated import manager_pb2_grpc
from generated.manager_pb2_grpc import CollectionManagerStub

reference = "localhost:5000/demo/pyindex:latest"

# os.getenv("EXTRA_INDEX_URL")
# os.getenv("INDEX_URL")

# os.environ['EMPOROUS_SOCKET_ADDRESS'] = '/home/d10n/code/emporous-pip/emporous.sock'
# https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch03s15.html
# os.environ['EMPOROUS_SOCKET_ADDRESS'] = '/run/emporous.sock'
os.environ['EMPOROUS_SOCKET_ADDRESS'] = '/tmp/emporous.sock'

print(sys.argv)

pip_args = sys.argv[1:]


# pip.main(sys.argv)

def create_auth_config(reference: str) -> manager_pb2.AuthConfig:
    """
    Create an authentication configuration based on given
    reference and default configuration locations.
    This loads from ~/.docker/config.json.
    """
    auth_configs = auth.load_config()
    registry, _ = auth.resolve_repository_name(reference)
    creds = auth.resolve_authconfig(auth_configs, registry)
    if creds is not None:
        auth_config = manager_pb2.AuthConfig(
            registry_host=f"http://{registry}",
            username=creds["username"],
            password=creds["password"],
        )
        return auth_config


class EmporousPipHttpServer(http.server.HTTPServer):
    pass


package_links_path = re.compile('/simple/([^/]+)/')
package_file_path = re.compile('/simple/([^/]+/.+)')


class EmporousPipHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    Expose a PEP503-compliant pip index

    reference : string
        The registry image path (e.g. localhost:5000/image:latest)
        for the source collection.
    attributes : dict
        A dictionary of key,value pairs to filter
        collection content when pulling.
    """

    def do_GET(self):
        print(self.path)
        path_parsed = urllib.parse.urlparse(self.path)

        auth_config = create_auth_config(reference)

        # render web root redirect
        if not self.path.startswith('/simple/'):
            if self.path.startswith('/'):
                redirect = '/simple/' + self.path[1:]
            else:
                redirect = '/simple/' + self.path
            self.send_response(http.HTTPStatus.TEMPORARY_REDIRECT)
            self.send_header('Location', redirect)
            self.end_headers()
            return
        # if self.path == '/' or self.path == '':
        #     self.send_response(http.HTTPStatus.TEMPORARY_REDIRECT)
        #     self.send_header('Location', '/simple/')
        #     self.end_headers()
        #     return

        # render index root
        if self.path == '/simple/':
            links = []

            # render listing
            req = manager_pb2.List.Request(
                source=reference,
                filter=None,
                auth=auth_config
            )
            with grpc.insecure_channel(f"unix://{os.environ['EMPOROUS_SOCKET_ADDRESS']}") as channel:
                print(channel)
                # stub = manager_pb2_grpc.RouteGuideStub(channel)
                stub: CollectionManagerStub = manager_pb2_grpc.CollectionManagerStub(channel)
                resp = stub.ListContent(req)
                # resp = json_format.MessageToDict(resp)

                files = resp.collection.files

                # <!DOCTYPE html>
                # <html>
                # <head>
                # <title>Emporous Simple Index</title>
                # </head>
                # <body>
                # <a href="/simple/bottle/">bottle</a>
                # <a href="/simple/isodate/">isodate</a>
                # </body>
                # </html>

                packages = set()
                for file in files:
                    attributes = json_format.MessageToDict(file.attributes)
                    if 'unknown' in attributes and 'package' in attributes['unknown']:
                        packages.add(attributes['unknown']['package'])

                for package in packages:
                    link = ET.Element('a', {'href': f'/simple/{package}/'})
                    link.text = package
                    links += [ET.tostring(link, encoding='unicode', method='html')]

                    pass
                print(files)
                pass

            rendered = textwrap.dedent("""
            <!DOCTYPE html>
            <html>
             <head><title>Emporous Simple Index</title></head>
             <body>
              {}
             </body>
            </html>
            """).format('\n  '.join(links))

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(rendered.encode('utf8'))
            return

        # render package links
        package_links_route = package_links_path.fullmatch(self.path)
        if package_links_route:
            package = package_links_route.group(1)
            links = []

            attributes = {
                'package': package,
                'pyindex': True,
            }
            attribute_struct = Struct()
            attribute_struct.update(attributes)

            # render listing
            req = manager_pb2.List.Request(
                source=reference,
                filter=attribute_struct,
                auth=auth_config
            )
            with grpc.insecure_channel(f"unix://{os.environ['EMPOROUS_SOCKET_ADDRESS']}") as channel:
                print(channel)
                stub: CollectionManagerStub = manager_pb2_grpc.CollectionManagerStub(channel)
                resp = stub.ListContent(req)
                # resp = json_format.MessageToDict(resp)

                files = resp.collection.files

                for file in files:
                    attributes = json_format.MessageToDict(file.attributes)
                    if 'unknown' not in attributes:
                        continue
                    if 'package' not in attributes['unknown']:
                        continue
                    title = attributes['converted']['org.opencontainers.image.title']
                    package = attributes['unknown']['package']
                    digest = file.file
                    digest = digest.replace(':', '=')
                    print(file.attributes)

                    basename = os.path.basename(title)

                    link = ET.Element('a', {'href': f'/simple/{title}#{digest}'})
                    link.text = basename
                    links += [ET.tostring(link, encoding='unicode', method='html')]

                package_html = html.escape(package)
                rendered = textwrap.dedent("""
                <!DOCTYPE html>
                <html>
                 <head><title>Links for {}</title></head>
                 <body>
                  <h1>Links for {}</h1>
                  {}
                 </body>
                </html>
                """).format(package_html, package_html, '<br />\n  '.join(links))

                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(rendered.encode('utf8'))
                return

        # render file download
        package_file_route = package_file_path.fullmatch(path_parsed.path)
        if package_file_route:
            file_name = package_file_route.group(1)

            req = manager_pb2.ReadLayer.Request(
                source=reference,
                layer_title=file_name,
                auth=auth_config,
            )
            options = [('grpc.max_receive_message_length', 1024 * 1024 * 1024)]  # 1 GiB
            with grpc.insecure_channel(f"unix://{os.environ['EMPOROUS_SOCKET_ADDRESS']}", options=options) as channel:
                stub = manager_pb2_grpc.CollectionManagerStub(channel)
                resp = stub.ReadLayer(req)
                result = resp.binary
                self.send_response(200)
                self.end_headers()
                self.wfile.write(result)
                return
            pass

        self.send_response(404)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><head><title>Not Found</title></head><body>Not Found</body></html>')
        pass

    pass


# https://peps.python.org/pep-0503/#normalized-names
def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


async def open_grpc_server():
    # grpc_server = subprocess.Popen(["emporous", "serve", "--plain-http", os.environ['EMPOROUS_SOCKET_ADDRESS']], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(["emporous", "serve", "--plain-http", os.environ['EMPOROUS_SOCKET_ADDRESS']])
    grpc_server = subprocess.Popen(["emporous", "serve", "--plain-http", os.environ['EMPOROUS_SOCKET_ADDRESS']],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)
    print("grpc server started")
    stdout, stderr = grpc_server.communicate()
    rc = grpc_server.wait()
    print("grpc server finished")


def main():
    print("emporous pip index starting")
    httpd = EmporousPipHttpServer(('localhost', 8089), EmporousPipHttpRequestHandler)
    print(httpd.server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    # asyncio.run(main())
    main()
