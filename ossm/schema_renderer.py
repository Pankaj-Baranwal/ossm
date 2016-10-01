from rest_framework_swagger.renderers import OpenAPIRenderer


class MyAPIRenderer(OpenAPIRenderer):
    API_BASE_PATH = '/api/v1/'
    APP_HOSTNAME = ''

    def _get_url_splitted(self, url):
        splitted_url = url.replace(self.API_BASE_PATH, '').split('/')
        url_parts = [x for x in splitted_url if '{' not in x]
        return list(filter(None, url_parts))

    def add_customizations(self, data, renderer_context):
        super().add_customizations(data, renderer_context)
        data['host'] = self.APP_HOSTNAME

        tags = []
        for url, values in data['paths'].items():
            methods = values.keys()
            for method in methods:
                splitted_url = self._get_url_splitted(url)
                if not len(splitted_url) > 1:
                    continue
                data['paths'][url][method]['tags'] = [splitted_url[0], ]
                _operation_id = "{}_{}".format(method, '_'.join(splitted_url))

                data['paths'][url][method]['operationId'] = _operation_id
                if splitted_url[0] not in tags:
                    tags.append(splitted_url[0])
        return tags
