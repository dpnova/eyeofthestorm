# Eye of the Storm

A REST framework built on top of Cyclone.

## Rationale

Cyclone provides a lot of nice functionality out of the box, but there
is a consistently required layer on top of it to turn it into a nice
tool for building out REST applications. This library aims to be that
pluggable layer.

One of the key things here is full support for Resource methods returning
deferreds.


By defining a set of resources with the currect interface, the framework
can serve them from an accepted set of urls.

You can override the handler for the resource by providing your own subclass.

You can create your own serializer, or just use the default one (just calls
`serialize()` on your resource).

Things still to consider:

* versioning
* rate limiting
* content negotiation
* HATEOS




## Example


```python

from eots import RESTHandler, RESTResource, OwnerCanModify


class ProfileHandler(RESTHandler):
    pass


class V1ProfileResource(Resource):
    permissions = [OwnerCanModify]
    serializer = ProfileSerializer


    def retrieve(self, id):
        pass

    def list(self):
        pass

    def update(self, id):
        pass

    def create(self):
        pass

    def delete(self, id):
        pass



class ProfileResourceSet(ResourceSet):
    handler = ProfileHandler
    versions = {"v1": V1ProfileResource}

```

# License

NOTE: Significant portions of this code are lifted directly from DRF:
    https://github.com/tomchristie/django-rest-framework

The DRF License:

    Copyright (c) 2011-2014, Tom Christie All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
