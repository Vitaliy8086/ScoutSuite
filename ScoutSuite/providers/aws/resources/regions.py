from ScoutSuite.providers.aws.aws import get_aws_account_id
from ScoutSuite.providers.aws.resources.resources import AWSCompositeResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
import abc

class Regions(AWSCompositeResources, metaclass=abc.ABCMeta):
    def __init__(self, service):
        self.service = service
        # TODO: Should be injected
        self.facade = AWSFacade()

    async def fetch_all(self, credentials, regions=None, partition_name='aws'):

        self['regions'] = {}
        for region in await self.facade.build_region_list(self.service, regions, partition_name):
            self['regions'][region] = {
                'id': region,
                'region': region,
                'name': region
            }

            await self._fetch_children(self['regions'][region], {'region': region, 'owner_id': get_aws_account_id(credentials)})

        self._set_counts()

    def _set_counts(self):
        self['regions_count'] = len(self['regions'])
        for _, key in self._children:
            self[key + '_count'] = sum([region[key + '_count'] for region in self['regions'].values()])