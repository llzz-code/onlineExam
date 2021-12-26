from xadmin.plugins.utils import get_context_dict
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader
import xadmin


class ListExcelImportPlugins(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context=get_context_dict(context)))


xadmin.site.register_plugin(ListExcelImportPlugins, ListAdminView)
