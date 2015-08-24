from OLiMS.dependencies.dependency import ClassSecurityInfo
from OLiMS.dependencies.dependency import schemata
from OLiMS.dependencies.dependency import getToolByName
from OLiMS.dependencies.dependency import atapi
from OLiMS.dependencies.dependency import registerType
from OLiMS.dependencies.dependency import getToolByName
from OLiMS.lims.browser.bika_listing import BikaListingView
from OLiMS.lims.config import PROJECTNAME
from OLiMS.lims import bikaMessageFactory as _
from OLiMS.lims.utils import t
from OLiMS.lims.content.bikaschema import BikaFolderSchema
from OLiMS.dependencies.dependency import IViewView
from OLiMS.lims.interfaces import IAttachmentTypes
from OLiMS.dependencies.dependency import IFolderContentsView
from OLiMS.dependencies.dependency import ATFolder, ATFolderSchema
from OLiMS.dependencies.dependency import implements

class AttachmentTypesView(BikaListingView):
    implements(IFolderContentsView, IViewView)
    def __init__(self, context, request):
        super(AttachmentTypesView, self).__init__(context, request)
        self.catalog = 'bika_setup_catalog'
        self.contentFilter = {'portal_type': 'AttachmentType',
                              'sort_on': 'sortable_title'}
        self.context_actions = {_('Add'):
                                {'url':'createObject?type_name=AttachmentType',
                                 'icon': '++resource++bika.lims.images/add.png'}}
        self.icon = self.portal_url + "/++resource++bika.lims.images/attachment_big.png"
        self.title = self.context.translate(_("Attachment Types"))
        self.show_sort_column = False
        self.show_select_row = False
        self.show_select_column = True
        self.pagesize = 25

        self.columns = {
            'Title': {'title': _('Attachment Type'),
                      'index': 'sortable_title'},
            'Description': {'title': _('Description'),
                            'index': 'description',
                            'toggle': True},
        }
        self.review_states = [
            {'id':'default',
             'title': _('All'),
             'contentFilter':{},
             'columns': ['Title',
                         'Description']},
        ]

    def folderitems(self):
        items = BikaListingView.folderitems(self)
        for x in range(len(items)):
            if not items[x].has_key('obj'): continue
            obj = items[x]['obj']
            items[x]['replace']['Title'] = "<a href='%s'>%s</a>" % \
                 (items[x]['url'], items[x]['Title'])
            items[x]['Description'] = obj.Description()

        return items

schema = ATFolderSchema.copy()
class AttachmentTypes(ATFolder):
    implements(IAttachmentTypes)
    displayContentsTab = False
    schema = schema

schemata.finalizeATCTSchema(schema, folderish = True, moveDiscussion = False)
atapi.registerType(AttachmentTypes, PROJECTNAME)